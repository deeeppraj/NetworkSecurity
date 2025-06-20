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
SAVED_MODEL_DIR:str = os.path.join("saved_models")
MODEL_PICKLE_FILE = "model.pkl"


'''
Some common constant variables
'''

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = 'phisingData.csv'

TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'

'''
DATA VALIDATION CONFIG
'''
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INIVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"
SCHEMA_FILE_PATH =  os.path.join("data_schema" , "schema.yaml")
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

'''
DATA TTRANSFORMATION CONFIG:

'''

DATA_TRANSFORMATION_DIR_NAME:str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR :str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str =  'transformed_object'
DATA_TRANSFORMATIO_IN_PARAMS:dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
} ## for my knn imputer
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"


"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05
