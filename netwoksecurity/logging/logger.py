import os
import sys
import logging
from datetime import datetime

LOG_FILE = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"
log = os.path.join(os.getcwd(),'Logs') 
folder = os.makedirs(log, exist_ok= True)
LOG_FILE_PATH = os.path.join(log, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO

)