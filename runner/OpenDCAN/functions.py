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

 
def post_config(opt):
    opt.device = torch.device('cuda:%s'%(opt.cuda) if torch.cuda.is_available() else "cpu")
    if opt.seed is None:
        opt.seed = random.randint(1, 10000)
    

    #random.seed(opt.seed)
    torch.manual_seed(opt.seed)
    torch.cuda.manual_seed_all(opt.seed)
    np.random.seed(opt.seed)
    if torch.cuda.is_available() and opt.not_cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    
    #输出文件
    opt.dir2save = generate_dir2save(opt)
    opt.num_classes = num_classes_of(opt)
    opt.class_names = class_names(opt)

    return opt


def generate_dir2save(opt):
    if not opt.openBP:
        dir2save = "checkpoints/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
    else:
        dir2save = "checkpoints/openBP/%s/%s/%d" % (opt.dataset, opt.net, opt.build)
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