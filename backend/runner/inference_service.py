import os
import shutil
import uuid
import zipfile

import torch
import torchvision.transforms as transforms

from OpenDCAN.models import ResNetInferenceModel
from dixitool.pytorch.datasets import ImageNoneLabelDataset
from settings import DATASET_BASE_PATH

IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')

def generateUUID():
    uid = str(uuid.uuid1()).replace('-','')
    return uid

def inference_sample(model_path, sample_path, classes):
    # 添加一个位置类的判断
    classes.append('unknown')
    idx_to_classes = {i : cls_name for i, cls_name in enumerate(classes)}

    model = ResNetInferenceModel(len(classes))
    model.load_parameter(model_path)

    with open(sample_path, 'rb') as f:
        pred, likelihood = model.predict(f)
    
    predict_class = idx_to_classes[pred]
    likelihood = round((100-likelihood*100),3)

    return predict_class, likelihood

def inference_dataset(model_path, target_path, classes, save_dir) -> str:
    classes.append('unknown')
    idx_to_classes = {}
    idx_to_classes = {i : cls_name for i, cls_name in enumerate(classes)}
    wait_to_zip_dir = []
    # 1 在target_path下面新建所有类别的目录, 补充idx_to_classes
    for idx, cls_name in enumerate(classes):
        idx_to_classes[idx]= cls_name
        os.makedirs(os.path.join(target_path, cls_name), exist_ok=True)
        wait_to_zip_dir.append(os.path.join(target_path, cls_name))
    
    model = ResNetInferenceModel(len(classes))
    model.load_parameter(model_path)
    

    transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),#center crop，传入224，因为正好可以在lower之后得到6*6大小的feature map
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    dataset = ImageNoneLabelDataset(target_path, transform = transform, get_path = True)
    
    # 2 拷贝样本到它该去的目录
    
    
    # 3 压缩这几个目录
    uuid = generateUUID()
    zip_filename = uuid + '.zip'
    zip_file_path = os.path.join(save_dir, zip_filename)
    # 4 压缩文件移动到save_dir下面
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        with torch.no_grad():
            for idx in range(len(dataset)):
                input_tensor, path = dataset[idx]
                input_tensor = input_tensor.unsqueeze(0) # add batch dimension

                pred_label, likelihood = model.predict2(input_tensor)
                predict_class = idx_to_classes[pred_label]
                
                dst = os.path.join(target_path, predict_class)
                zf.write(path, os.path.join(predict_class, os.path.basename(path)))
                        
    return zip_filename
