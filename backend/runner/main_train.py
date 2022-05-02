from aifc import Error
import argparse
import os
from asyncio.log import logger

import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as torch_f
from torch.optim import SGD, Adam

from OpenDCAN.config import yaml_config # yaml配置文件 包含 训练超参数相关的东西
import OpenDCAN.functions as _f
from OpenDCAN.models import ResBase, ResClassifier
from OpenDCAN.loss import LGMLoss_v0

from dixitool.common.utils import CompleteLogger
from dixitool.pytorch.datasets import DIXIImageFolder, ImageNoneLabelDataset, ForeverDataIterator


DATASET_BASE_PATH = '../'

def main():
    
    parser = argparse.ArgumentParser(description='Code for *Universal Domain Adaptation*',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--source_path',type=str,default='_data/source_dataset/45a2bef4c2d111ecb8eaacde48001122_amazon_office2',metavar='N',help='source directory')
    parser.add_argument('--target_path',type=str,default='_data/target_dataset/8c733062c24e11ecbe1eacde48001122',metavar='N',help='target directory')
    parser.add_argument('--task_id', type=int)
    parser.add_argument('--record_id', type=int)

    args = parser.parse_args()
    train_args = yaml_config.train

    completeLogger = CompleteLogger('./logs', phase='train')
    # device-> train_args;  dir2save-> args
    train_args, args = _f.post_config(train_args, args)

    _f.print_config(train_args)
    _f.print_config(args)

    data_transforms = {
        'source': transforms.Compose([
            transforms.Resize(256),#改大小
            transforms.RandomHorizontalFlip(),#随即水平翻转
            transforms.RandomCrop(224),#随机裁剪
            transforms.ToTensor(),#转为torch的tensor
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])#白化，这是ImageNet
        ]),
        'target': transforms.Compose([
            transforms.Resize(256),
            transforms.RandomHorizontalFlip(),
            transforms.RandomCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    }

    source_path = os.path.join(DATASET_BASE_PATH, args.source_path)
    target_path = os.path.join(DATASET_BASE_PATH, args.target_path)

    ## 去掉 '__MACOSX' 目录
    source_dataset = DIXIImageFolder(source_path, transform=data_transforms['source'], folder_filter=(lambda x: x not in ['__MACOSX']))
    # TBD 目标域数据集
    target_dataset = ImageNoneLabelDataset(target_path, transform=data_transforms['target'])
    
    source_dataloader = DataLoader(source_dataset, train_args.batch_size, shuffle=True)
    target_dataloader = DataLoader(target_dataset, train_args.batch_size, shuffle=True)

    # define data iterator, used with train_args.iters_per_epoch
    train_source_iter = ForeverDataIterator(source_dataloader, device = train_args.device)
    train_target_iter = ForeverDataIterator(target_dataloader, device = train_args.device)

    cross_entropy = nn.CrossEntropyLoss()
    # 源域 标签类别数量
    train_args.source_classes_num = len(source_dataset.classes)

    # 特征提取器，分类器
    generator = ResBase(option='resnet50', pret=True, print_structure=False).to(train_args.device)

    # [Attention!!] 注意分类器的 输出维度，先试试 额外一个纬度
    classifier = ResClassifier(
        num_classes = len(source_dataset.classes) + 1
        ).to(train_args.device)
    
    src_lgm_loss = LGMLoss_v0(len(source_dataset.classes), 100, train_args.alpha) # num_classes, feat_dim, lgm alpha parameter
    src_lgm_loss = src_lgm_loss.to(train_args.device) #lgm有这个loss，要用起来
    
    # define optimizer for lgm, generator and classifier
    optimizer4center = SGD(src_lgm_loss.parameters(), momentum=0.9, lr=train_args.lr_center,
                          weight_decay=1e-6, nesterov=True)
    params = [{'params':generator.linear1.parameters()},{'params':generator.linear2.parameters()},
                  {'params':generator.bn1.parameters()},{'params':generator.bn2.parameters()}]

    optim_g = Adam(params, lr = train_args.lr, weight_decay=1e-6)
    optim_c = SGD(classifier.parameters(), momentum=0.9, lr=train_args.lr,
                          weight_decay=1e-6, nesterov=True)

    # train_args.epochs 循环
    for epoch in range(args.epochs):
        train(train_source_iter, train_target_iter, generator, classifier, optim_g, optim_c, src_lgm_loss, epoch, train_args)

        _f.save_checkpoint({
            'G_state_dict': generator.state_dict(),
            'C_state_dict': classifier.state_dict(),
        }, False, args.dir2save, filename = 'lates.pth.tar')
    # exit process
    completeLogger.close()

def train(train_source_iter, train_target_iter,
          generator, classifier, optimizer_g: Adam, optimizer_c: SGD,
          src_lgm_loss, epoch, args):
    generator.train()
    classifier.train()
    train_loss = 0.0

    for i in range(args.iters_per_epoch):
        input_s, target_s = next(train_source_iter)
        input_t = next(train_target_iter)
        
        # 
        optimizer_g.zero_grad()
        optimizer_c.zero_grad()

        feat_s = generator(input_s)
        out_s = classifier(feat_s)

        loss_s = torch_f.cross_entropy(out_s, target_s)
        # 给源域数据增加l-gm loss。likelihood增加 分布约束，0.1的scalar权重
        _, margin_logits, likelihood = src_lgm_loss(feat_s, target_s)
        # 源域的 l-gm loss
        loss_lm_s =  0.1 * likelihood + torch_f.cross_entropy(margin_logits, target_s)

        feat_t = generator(input_t) # 就只需要feature
        out_t = classifier(feat_t, reverse=True)

        loss_adv_t = _f.openBP_bce_loss(out_t, args.source_classes_num + 1)

        target_weights = _f.target_weight(out_t) #size(batch,1).detach()

        # 挑选出被认为是known类别的东西
        pseudo_label = torch.argmax(out_t, dim=1)
        mask = pseudo_label != args.source_classes_num
        pseudo_label = pseudo_label[mask]
        known_pseudo_feat_t = feat_t[mask] # 这个梯度是可以传回去的
        target_weights = target_weights[mask] # 去掉被认为是unknown类别的权重 # ( batch_size - unknown_size )
        
        s_L2norm_loss = _f.get_L2norm_loss_self_driven(feat_s,args.weight_L2norm)
        t_L2norm_loss = (target_weights * _f.get_L2norm_loss_self_driven(known_pseudo_feat_t, args.weight_L2norm, keepdim=True)).mean()

        loss = loss_s + args.weight_lgm * loss_lm_s + args.weight_adv * loss_adv_t + args.weight_L2norm_lambd*(s_L2norm_loss + t_L2norm_loss) #+ loss_lm_t #+ loss_lm_t #+ 0.1*center_similarity_loss # 这里还是把源域的这个loss_s留着

        loss.backward()
        train_loss += loss.item()
        
        optimizer_g.step()
        optimizer_c.step()

    print("Epoch: [{}]  train loss {}".format(epoch, train_loss))

    
if __name__ == '__main__':
    try:
        main()
        os._exit(0)
    except Exception:
        os._exit(1)