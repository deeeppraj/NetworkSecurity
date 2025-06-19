from datetime import datetime
import os
from netwoksecurity.constants import training_pipeline
from dataclasses import dataclass


class training_pipeline_config:
    def __init__(self,timestamp =datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name= training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp:str = timestamp
        

class DataIngestionconfig:
    def __init__(self,train_pipe_config:training_pipeline_config):
        self.data_ingestion_dir = os.path.join(
            train_pipe_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR)
        self.feat_store_filepath = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEAT,training_pipeline.FILE_NAME)
        self.train_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED,training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED,training_pipeline.TEST_FILE_NAME)
        self.train_test_spplit_ratio : float=  training_pipeline.TRAIN_TEST_SPLIT
        self.database_name:str = training_pipeline.DATA_INGESTION_DATABASE
        self.collection_name:str = training_pipeline.DATA_INGESTION_COLLECTION

    

class DataValidationconfig:
    def __init__(self,train_pipe_config:training_pipeline_config):
        self.data_validation_dir:str = os.path.join(
            train_pipe_config.artifact_dir , training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INIVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )
        
