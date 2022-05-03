import torch
import torch.nn as nn
from torch.autograd.function import Function
import torch.nn.functional as F
from torch.autograd import Variable

class LGMLoss(nn.Module):

    """
    Refer to paper:
    Weitao Wan, Yuanyi Zhong,Tianpeng Li, Jiansheng Chen
    Rethinking Feature Distribution for Loss Functions in Image Classification. CVPR 2018
    re-implement by yirong mao
    2018 07/02
    """
    def __init__(self, num_classes, feat_dim, alpha):
        super(LGMLoss, self).__init__()
        self.feat_dim = feat_dim
        self.num_classes = num_classes
        self.alpha = alpha

        self.centers = nn.Parameter(torch.randn(num_classes, feat_dim)) #各个类别中心
        self.log_covs = nn.Parameter(torch.zeros(num_classes, feat_dim)) #这是什么？应该是协方差对角矩阵

    def forward(self, feat, label):
        batch_size = feat.shape[0]
        log_covs = torch.unsqueeze(self.log_covs, dim=0) # 1*c*d  (1*classes*dim)


        covs = torch.exp(log_covs) # 1*c*d log符号里面的值
        tcovs = covs.repeat(batch_size, 1, 1) # n*c*d 
        diff = torch.unsqueeze(feat, dim=1) - torch.unsqueeze(self.centers, dim=0) # n*c*d,每个样本和每个class的差
        wdiff = torch.div(diff, tcovs) # 在算dist的时候，diff乘了两次
        diff = torch.mul(diff, wdiff)
        dist = torch.sum(diff, dim=-1) #eq.(18) 假设协方差矩阵是对角矩阵  n*c


        y_onehot = torch.FloatTensor(batch_size, self.num_classes)
        y_onehot.zero_()
        y_onehot = Variable(y_onehot).cuda()
        y_onehot.scatter_(1, torch.unsqueeze(label, dim=-1), self.alpha)
        y_onehot = y_onehot + 1.0
        margin_dist = torch.mul(dist, y_onehot) # n*c

        slog_covs = torch.sum(log_covs, dim=-1) #1*c
        tslog_covs = slog_covs.repeat(batch_size, 1) # n*c
        margin_logits = -0.5*(tslog_covs + margin_dist) # eq.(17) 
        logits = -0.5 * (tslog_covs + dist)

        cdiff = feat - torch.index_select(self.centers, dim=0, index=label.long())
        cdist = cdiff.pow(2).sum(1).sum(0) / 2.0

        slog_covs = torch.squeeze(slog_covs)
        reg = 0.5*torch.sum(torch.index_select(slog_covs, dim=0, index=label.long()))
        likelihood = (1.0/batch_size) * (cdist + reg)

        return logits, margin_logits, likelihood


class LGMLoss_v0(nn.Module):
    """
    LGMLoss whose covariance is fixed as Identity matrix
    """
    def __init__(self, num_classes, feat_dim, alpha):
        super(LGMLoss_v0, self).__init__()
        self.feat_dim = feat_dim
        self.num_classes = num_classes
        self.alpha = alpha

        self.centers = nn.Parameter(torch.randn(num_classes, feat_dim)) # lgm_loss.cuda()的时候，这个center就被放在GPU里面了

        nn.init.kaiming_normal_(self.centers, mode='fan_out',  nonlinearity='leaky_relu')
        
    def forward(self, feat, label , only_likelihood=False, keepdim=False):
        batch_size = feat.shape[0]

        if only_likelihood:
            cdiff = feat - torch.index_select(self.centers, dim=0, index=label.long())  #Size([batch,2])
            if keepdim:
                likelihood = (1.0/batch_size) * cdiff.pow(2).sum(1) / 2.0
            else:
                likelihood = (1.0/batch_size) * cdiff.pow(2).sum(1).sum(0) / 2.0
            return likelihood

        # Size([batch, 1,2]) - Size([1, 10, 2])  纬度不符合的，只有维度是1的时候，约定可以相减
        diff = torch.unsqueeze(feat, dim=1) - torch.unsqueeze(self.centers, dim=0)
        # diff.size() = Size([batch,10,2])
        diff = torch.mul(diff, diff)#平方？ size=Size([4,10,2]) 代表么每个样本和每个class中心之间的距离平方
        dist = torch.sum(diff, dim=-1)#size = Size([batch, 10]) 求和后就是样本和每个class之间L2 距离，

        y_onehot = torch.FloatTensor(batch_size, self.num_classes) #[batch,10]
        y_onehot.zero_()#置零0
        y_onehot = y_onehot.to(torch.device('cuda:0')) # cuda-lize
        y_onehot.scatter_(1, torch.unsqueeze(label, dim=-1), self.alpha) #在y_onehot的label的位置里面放alpha
        y_onehot = y_onehot + 1.0
        margin_dist = torch.mul(dist, y_onehot) #size = [batch,10]
        margin_logits = -0.5 * margin_dist #margin_logit包含样本和每个类别中心的距离，且带监督信号
        logits = -0.5 * dist# size = [batch,10]  样本和每个类别中心的距离，没有监督信号

        # Size([batch, 2]) - Size([batch,2]) 
        cdiff = feat - torch.index_select(self.centers, dim=0, index=label.long())  #Size([batch,2])
        if keepdim:
            likelihood = (1.0/batch_size) * cdiff.pow(2).sum(1) / 2.0
        else:
            likelihood = (1.0/batch_size) * cdiff.pow(2).sum(1).sum(0) / 2.0 #sum(1)L2距离，sum(0)所有样本计算相加，除以2再除以batch_size，不知道是什么意思
        return logits, margin_logits, likelihood  #margin_logits是带标签监督信息的

# class CrossDomainCenterLoss(nn.Module):
    
#     def __init__(self, num_classes, feat_dim):
#         super(CrossDomainCenterLoss, self).__init__()
#         self.num_classes = num_classes
#         self.feat_dim = feat_dim
#         self.src_centers = nn.Parameter(torch.randn(num_classes, feat_dim))
#         self.tgt_centers = nn.Parameter(torch.randn(num_classes, feat_dim))

#         self.crossCenterlossFunction = CrossDomainlossFunction.apply

#         nn.init.kaiming_normal_(self.src_centers, mode='fan_out',  nonlinearity='leaky_relu')
#         nn.init.kaiming_normal_(self.tgt_centers, mode='fan_out',  nonlinearity='leaky_relu')

#     def forward(self, feat, y):
#         # feat‘s size is size(batch_size, -1)        
#         if feat.size(1) != self.feat_dim:
#             raise ValueError("Center's dim: {0} should be equal to input feature's dim: {1}".format(self.feat_dim,feat.size(1)))

#         return self.crossCenterlossFunction(feat, y, self.src_centers, self.tgt_centers)

# class CrossDomainlossFunction(Function):

#     @staticmethod
#     def forward(ctx, feature, target, src_centers, tgt_centers):
        
#         pass

#     @staticmethod
#     def backward(ctx, grad_output):

#         pass


class CenterLoss(nn.Module):
    def __init__(self, num_classes, feat_dim):
        super(CenterLoss, self).__init__()
        self.num_classes = num_classes
        self.feat_dim = feat_dim
        self.centers = nn.Parameter(torch.randn(num_classes, feat_dim))
        self.centerlossfunction = CenterlossFunction.apply

        nn.init.kaiming_normal_(self.centers, mode='fan_out',  nonlinearity='leaky_relu')

    def forward(self, y, feat):
        # To squeeze the Tenosr
        batch_size = feat.size(0)
        feat = feat.view(batch_size, 1, 1, -1).squeeze()
        # To check the dim of centers and features
        if feat.size(1) != self.feat_dim:
            raise ValueError("Center's dim: {0} should be equal to input feature's dim: {1}".format(self.feat_dim,feat.size(1)))
        return self.centerlossfunction(feat, y, self.centers)


class CenterlossFunction(Function):

    @staticmethod
    def forward(ctx, feature, label, centers):
        ctx.save_for_backward(feature, label, centers)
        centers_pred = centers.index_select(0, label.long())
        return (feature - centers_pred).pow(2).sum(1).sum(0) / 2.0  # Eq. 2


    @staticmethod
    def backward(ctx, grad_output):
        feature, label, centers = ctx.saved_variables
        grad_feature = feature - centers.index_select(0, label.long()) # Eq. 3

        # init every iteration
        counts = torch.ones(centers.size(0))
        grad_centers = torch.zeros(centers.size())
        if feature.is_cuda:
            counts = counts.cuda()
            grad_centers = grad_centers.cuda()
        # print counts, grad_centers

        # Eq. 4 || need optimization !! To be vectorized, but how?
        for i in range(feature.size(0)):
            j = int(label[i].item())
            counts[j] += 1
            grad_centers[j] += (centers.data[j] - feature.data[i])
        # print counts
        #grad_centers = Variable(grad_centers/counts.view(-1, 1))
        grad_centers = grad_centers/counts.view(-1, 1) # Eq. 4

        # grad_feature*grad_output用来更新 之前网络参数的， grad_centers用来更新self.center的参数
        return grad_feature * grad_output, None, grad_centers

