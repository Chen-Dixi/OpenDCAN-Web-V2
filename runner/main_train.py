import argparse
import os
from asyncio.log import logger

from OpenDCAN.config import yaml_config
from OpenDCAN.functions import print_config

from dixitool.common.utils import CompleteLogger

def main():
    
    parser = argparse.ArgumentParser(description='Code for *Universal Domain Adaptation*',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--source-path',type=str,default='_data/source_dataset/45a2bef4c2d111ecb8eaacde48001122_amazon_office2',metavar='N',help='source directory')
    parser.add_argument('--target-path',type=str,default='_data/target_dataset/8c733062c24e11ecbe1eacde48001122',metavar='N',help='target directory')
    args = parser.parse_args()
    completeLogger = CompleteLogger('./', phase='train')

    print_config(yaml_config.train)
    print_config(args)
    completeLogger.close()
    os._exit(0)
if __name__ == '__main__':
    main()