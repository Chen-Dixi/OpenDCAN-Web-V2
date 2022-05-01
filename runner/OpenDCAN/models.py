#VGG 和 Alexnet
from torchvision import models
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Function
from .gradien_reverse import GradReverseLayer #调用了dixitool
import torch
import math
"""
class VGGBase(nn.Module):
    # Model VGG
    def __init__(self):
        super(VGGBase, self).__init__()
        model_ft = models.vgg19(pretrained=True)
        print(model_ft)
        mod = list(model_ft.features.children())
        self.lower = nn.Sequential(*mod)
        mod = list(model_ft.classifier.children())
        mod.pop()
        print(mod)
        self.upper = nn.Sequential(*mod)
        self.linear1 = nn.Linear(4096, 100)
        self.bn1 = nn.BatchNorm1d(100, affine=True)
        self.linear2 = nn.Linear(100, 100)
        self.bn2 = nn.BatchNorm1d(100, affine=True)

    def forward(self, x, target=False):
        x = self.lower(x)
        x = x.view(x.size(0), 512 * 7 * 7)
        x = self.upper(x)
        x = F.dropout(F.leaky_relu(self.bn1(self.linear1(x))), training=False)
        x = F.dropout(F.leaky_relu(self.bn2(self.linear2(x))), training=False)
        if target:
            return x
        else:
            return x
        return x
"""

ALLOWED_VGG_TYPE = ['vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn']

class VGGBase(nn.Module):
    #有很多种VGG
    def __init__(self, vgg_type='vgg19', pretrained=True, print_structure=False):
        super(VGGBase, self).__init__()
        if not vgg_type in ALLOWED_VGG_TYPE:
            raise NotImplementedError
        # get official vgg initialize function through getattr
        vgg_method = getattr(models, vgg_type)
        model_ft = vgg_method(pretrained=pretrained)

        # whethere printing the structure of vgg
        if print_structure:
            print(model_ft)

        mod = list(model_ft.features.children()) #features 特征提取部分 children()只返回模块，named_children和named_modules才返回名字. named_children无递归。modules()有递归，named_modules是递归的
        self.lower = nn.Sequential(*mod)
        mod = list(model_ft.classifier.children())
        mod.pop()

        if print_structure:
            print(mod)
        
        self.upper = nn.Sequential(*mod)
        self.linear1 = nn.Linear(4096, 100)
        self.bn1 = nn.BatchNorm1d(100, affine=True)
        self.linear2 = nn.Linear(100, 100)
        self.bn2 = nn.BatchNorm1d(100, affine=True)

    def forward(self, x, target=False):
        x = self.lower(x)
        x = x.view(x.size(0), 512 * 7 * 7)
        x = self.upper(x)
        x = F.dropout(F.leaky_relu(self.bn1(self.linear1(x))), training=False)
        x = F.dropout(F.leaky_relu(self.bn2(self.linear2(x))), training=False)
        if target:
            return x
        else:
            return x
        return x

    
    #这个函数，filename是.pth文件，我做实验严一般是
    # map_location写在torch.load里面，strict写在load_state_dict里面。我保存的一般是checkpoint文件，是pth.tar格式，而一个单独的模型一般是保存.pt或者.pth文件中
    # 这个函数看起来多此一举没有什么必要，基本不用
    def load_parameters(self, state_dict, map_location=None, strict=True):
        self.load_state_dict(torch.load(filename, map_location=map_location),
                             strict=strict)

class AlexBase(nn.Module):
    def __init__(self, pretrained=True, print_structure=False):
        super(AlexBase, self).__init__()
        model_ft = models.alexnet(pretrained=pretrained)
        
        mod = []
        
        for i in range(18):
            if i < 13:
                mod.append(model_ft.features[i])
        mod_upper = list(model_ft.classifier.children())
        mod_upper.pop()#去掉Alex的分类器最后一个nn.Linear(4096, 1000),
        # print(mod)
        self.upper = nn.Sequential(*mod_upper)#分类器去掉Alex最后一层nn.Linear(4096, 1000)
        self.lower = nn.Sequential(*mod)#特征提取器
        self.linear1 = nn.Linear(4096, 100)
        self.bn1 = nn.BatchNorm1d(100, affine=True)# 默认就是True。a boolean value that when set to True, this module has learnable affine parameters
        self.linear2 = nn.Linear(100, 100)
        self.bn2 = nn.BatchNorm1d(100, affine=True)
        if print_structure:
            print(self)

    def forward(self, x, target=False, feat_return=False):
        x = self.lower(x)#特征提取器
        x = x.view(x.size(0), 256*6*6)#9216
        x = self.upper(x)
        feat = x #做实验时，我们就返回feat这个地方。在调用模型时，传入feat_return=True就行
        x = F.dropout(F.leaky_relu(self.bn1(self.linear1(x))))
        # if self.training:
        #     x.mul_(math.sqrt(1 - 0.5))
        x = F.dropout(F.leaky_relu(self.bn2(self.linear2(x)))) #在原本的AlexNet上面加了Bn1d+Linear(100,100)+Bn1d的分类器
        # if self.training:
        #     x.mul_(math.sqrt(1 - 0.5))

        if feat_return:
            return feat
        if target:
            return x
        else:
            return x

    #这个函数，filename是.pth文件，我做实验严一般是
    # map_location写在torch.load里面，strict写在load_state_dict里面。我保存的一般是checkpoint文件，是pth.tar格式，而一个单独的模型一般是保存.pt或者.pth文件中
    # 这个函数看起来多此一举没有什么必要，基本不用
    def load_parameters(self, state_dict, map_location=None, strict=True):
        self.load_state_dict(torch.load(filename, map_location=map_location),
                             strict=strict)

# AlexNet是4096维的，这个classifier没有nn.Linear(4096,100),所以注意一下
class Classifier(nn.Module):
    def __init__(self, num_classes=12):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(100, 100)
        self.bn1 = nn.BatchNorm1d(100, affine=True)
        self.fc2 = nn.Linear(100, 100)
        self.bn2 = nn.BatchNorm1d(100, affine=True)
        self.fc3 = nn.Linear(100, num_classes)  # nn.Linear(100, num_classes)
        self.grad_reverse_layer = GradReverseLayer()
        self.lambd=1.0
    def set_lambda(self, lambd):
        self.lambd = lambd

    def set_num_classes(self, num_classes):
        self.fc3 = None
        self.fc3 = nn.Linear(100,num_classes)
        

    def forward(self, x, dropout=False, return_feat=False, reverse=False):
        if reverse:
            x = self.grad_reverse_layer(x, self.lambd)
            feat = x
            x = self.fc3(x)
        else:
            feat = x
            x = self.fc3(x)
        if return_feat:
            return x, feat
        return x



class ResBase(nn.Module):
    def __init__(self, option='resnet18', pret=True, unit_size=100, print_structure=False):
        super(ResBase, self).__init__()
        self.dim = 2048
        if option == 'resnet18':
            model_ft = models.resnet18(pretrained=pret)
            self.dim = 512
        if option == 'resnet50':
            model_ft = models.resnet50(pretrained=pret)
        if option == 'resnet101':
            model_ft = models.resnet101(pretrained=pret)
        if option == 'resnet152':
            model_ft = models.resnet152(pretrained=pret)
        mod = list(model_ft.children())
        mod.pop()
        self.features = nn.Sequential(*mod)
        # default unit size 100
        self.linear1 = nn.Linear(2048, unit_size)
        self.bn1 = nn.BatchNorm1d(unit_size, affine=True)
        self.linear2 = nn.Linear(unit_size, unit_size)
        self.bn2 = nn.BatchNorm1d(unit_size, affine=True)
        self.linear3 = nn.Linear(unit_size, unit_size)
        self.bn3 = nn.BatchNorm1d(unit_size, affine=True)
        self.linear4 = nn.Linear(unit_size, unit_size)
        self.bn4 = nn.BatchNorm1d(unit_size, affine=True)
        if print_structure:
            print(self)

    def forward(self, x,reverse=False):

        x = self.features(x)
        x = x.view(x.size(0), self.dim)
        # best with dropout
        if reverse:
            x = x.detach()

        x = F.dropout(F.relu(self.bn1(self.linear1(x))), training=self.training)
        x = F.dropout(F.relu(self.bn2(self.linear2(x))), training=self.training)

        return x


class ResClassifier(nn.Module):
    def __init__(self, num_classes=12, unit_size=100):
        super(ResClassifier, self).__init__()
        self.classifier = nn.Sequential(
            nn.Linear(unit_size, num_classes)
        )
        self.grad_reverse_layer = GradReverseLayer()
        self.lambd=1.0
        
    def set_lambda(self, lambd):
        self.lambd = lambd

    def forward(self, x, dropout=False, return_feat=False, reverse=False):
        if reverse:
            x = self.grad_reverse_layer(x, self.lambd)
        x = self.classifier(x)
        return x
