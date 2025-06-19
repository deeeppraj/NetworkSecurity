import yaml
import dill
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle








def read_yaml_file(file_path):
    try:
        with open (file_path , 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path , content , replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path , "w") as file:
            return yaml.dump(content ,file)
    
    except Exception as e:
        raise CustomException(e,sys)