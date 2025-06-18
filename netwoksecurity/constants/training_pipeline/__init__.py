import os,sys
import pandas as pd
import numpy as np

'''
all the constants
'''

DATA_INGESTION_COLLECTION:str = 'phising'
DATA_INGESTION_DATABASE:str =  'network'
DATA_INGESTION_DIR:str = "data_ingestion"
DATA_INGESTION_FEAT:str = 'feature_stor'
DATA_INGESTION_INGESTED:str = 'ingested'
TRAIN_TEST_SPLIT :float = 0.2


'''
Some common constant variables
'''

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = 'phisingData.csv'

TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'