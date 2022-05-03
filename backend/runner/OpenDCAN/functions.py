import torch
import random
import numpy as np 
import torch.nn.functional as F
import os
import shutil

def print_config(args):
    print("==========================================")
    print("==========       CONFIG      =============")
    print("==========================================")
    for arg, content in args.__dict__.items():
        print("{}: {}".format(arg, content))
    print("\n")

 
def post_config(train_args, args):
    train_args.device = torch.device('cuda:%s'%(train_args.cuda) if torch.cuda.is_available() else "cpu")
    if train_args.seed is None:
        train_args.seed = random.randint(1, 10000)
    

    #random.seed(opt.seed)
    torch.manual_seed(train_args.seed)
    torch.cuda.manual_seed_all(train_args.seed)
    np.random.seed(train_args.seed)
    
    args.dir2save = "../_model/task_%d/" % (args.task_id)
    os.makedirs(args.dir2save, exist_ok=True)

    return  train_args, args


def generate_dir2save(args):
    dir2save = "../_model/task_%d/" % (args.task_id)
    os.makedirs(dir2save, exist_ok=True)
    return dir2save

def generate_dir2output(opt):
    if not opt.openBP:
        dir2output = "ConsoleOutput/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
    else:
        dir2output = "ConsoleOutput/openBP/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
    return dir2output

def generate_dir2plotimage(opt):
    if not opt.openBP:
        dir2plot = "plot/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
    else:
        dir2plot = "plot/openBP/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
    return dir2plot

    
def num_classes_of(opt):
    if opt.dataset=='office31':
        return 11
    elif opt.dataset=='digits':
        return 6
    else:
        raise NotImplementedError

def class_names(opt):
    if opt.dataset=='office31':
        return ["back_pack","calculator","keyboard","monitor","mug","bike","headphones","laptop_computer","mouse","projector","unknown"]
    elif opt.dataset=='digits':
        return ['0 - zero', '1 - one', '2 - two', '3 - three', '4 - four','unknown']
    else:
        raise NotImplementedError

def bce_loss(output, target):
    output_neg = 1 - output
    target_neg = 1 - target
    result = torch.mean(target * torch.log(output + 1e-6))
    result += torch.mean(target_neg * torch.log(output_neg + 1e-6))
    return -torch.mean(result)

def openBP_bce_loss(out_t, num_classes):
    out_t = F.softmax(out_t, dim=1)
    prob1 = torch.sum(out_t[:,:num_classes-1],1).view(-1,1)
    prob2 = out_t[:, num_classes-1].contiguous().view(-1,1)
    prob = torch.cat((prob1,prob2), 1)
    target_funk = torch.FloatTensor(out_t.size()[0], 2).fill_(0.5).to(out_t.device)
    loss_adv_t = bce_loss(prob,target_funk)
    return loss_adv_t

def generate_folder(folder: str):
    if (os.path.exists(folder)):
        print('Folder already exist')
    else:
        try:
            os.makedirs(folder)
        except OSError:
            pass

def batch2data(batch, device):

    data, target = batch
    return data.to(device), target.to(device)

def load_from_checkpoint(checkpoint_file, *keys):

    if not os.path.exists(checkpoint_file):
        raise FileNotFoundError("{} not found".format(checkpoint_file))

    results = []
    checkpoint = torch.load(checkpoint_file)
    for key in keys:
        results.append(checkpoint[key])
    return results

def save_checkpoint( state, is_best, root, filename='checkpoint.pth.tar'):
    if not os.path.exists(root):
        os.makedirs(root)
    best_name = os.path.join(root, 'best_model_'+filename)
    filename = os.path.join(root, filename)
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, best_name)

import logging

def normalize_weight(x):
    min_val = x.min()
    max_val = x.max()
    x = (x - min_val) / (max_val - min_val)
    x = x / torch.mean(x)
    return x.detach()

def target_weight(output_t):
    after_softmax = F.softmax(output_t,dim=1) #这个包含未知类
    entropy = torch.sum(- after_softmax * torch.log(after_softmax + 1e-10), dim=1) # size = (batch_size, 1)
    entropy_norm = entropy / np.log(after_softmax.size(1)) #熵越大，置信度越小
    weight = - entropy_norm
    weight = weight.detach()
    return normalize_weight(weight)

"""
according to the equation in our paper, the value of this loss would only relate to the hyper-parameter \Delta r. 
As a result, since we use 1.0 for \Delta r, the loss value will actually be 1 and not change through training procedure. 
Though the loss value will not change, the gradient has been backward to update our model. And that is actually what we want. 
Please refer to the section 3.5 in our paper for more details.
"""
def get_L2norm_loss_self_driven(x, weight_L2norm, keepdim=False):
    radius = x.norm(p=2, dim=1).detach()
    assert radius.requires_grad == False
    radius = radius + 1.0 # 这个delta r是那个
    if keepdim:
        l = ((x.norm(p=2, dim=1) - radius) ** 2)
    else:    
        l = ((x.norm(p=2, dim=1) - radius) ** 2).mean()

    return weight_L2norm * l

def get_logger(filename, verbosity=1, name=None):
    level_dict = {0: logging.DEBUG, 1: logging.INFO, 2: logging.WARNING}
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(name)
    logger.setLevel(level_dict[verbosity])

    fh = logging.FileHandler(filename, "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger