import yaml
from easydict import EasyDict as edict
CONFIG_FILE = './train_setting.yml'

yaml_config = yaml.load(open(CONFIG_FILE), Loader=yaml.FullLoader)
yaml_config = edict(yaml_config)