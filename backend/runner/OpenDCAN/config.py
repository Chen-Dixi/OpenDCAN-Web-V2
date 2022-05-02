import yaml
from easydict import EasyDict as edict
CONFIG_FILE = './train_setting.yml'
# 从配置文件中读取
yaml_config = yaml.load(open(CONFIG_FILE), Loader=yaml.FullLoader)
yaml_config = edict(yaml_config)