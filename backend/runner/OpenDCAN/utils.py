import torch
from .models import *
import torch.optim as optim


def get_model(net_option,device, num_classes,imagenet_pretrained=True, print_structure=True):
    if net_option is None:
        raise ValueError

    if net_option.startswith('vgg'):
        model_g = VGGBase(vgg_type=net_option,pretrained=imagenet_pretrained,print_structure=print_structure)
        model_c = Classifier(num_classes)
    elif net_option == 'alex':
        model_g = AlexBase(pretrained=imagenet_pretrained,print_structure=print_structure)
        model_c = Classifier(num_classes)
    elif net_option.startswith('resnet'):
        model_g = ResBase(option=net_option, pret = imagenet_pretrained,print_structure=print_structure)
        model_c = ResClassifier(num_classes)
    return model_g.to(device), model_c.to(device)

def get_optimizer_office31(model_g, model_c,lr=1e-3, weight_decay=1e-6,update_lower=False):

    if not update_lower:
        params = [{'params':model_g.linear1.parameters()},{'params':model_g.linear2.parameters()},
                  {'params':model_g.bn1.parameters()},{'params':model_g.bn2.parameters()}]

    else:
        params = model_g.parameters()

    optim_g = optim.Adam(params, lr = lr, weight_decay=weight_decay)

    optim_c = optim.SGD(model_c.parameters(), momentum=0.9, lr=lr,
                          weight_decay=weight_decay, nesterov=True)

    return optim_g, optim_c
    
