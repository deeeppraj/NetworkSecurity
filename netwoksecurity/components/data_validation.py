import os,sys
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataValidationconfig
from netwoksecurity.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from netwoksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
from netwoksecurity.utils.main_utils.utils import read_yaml_file ,write_yaml_file


class Datavalidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact
                 , data_validation_config:DataValidationconfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.scheme_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise CustomException(e,sys)
        
    def readDataFunction(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_columns(self,data:pd.DataFrame):
        try:
            no_of_columns = len(self.scheme_config)
            logging.info(f"required no. of columns {no_of_columns}")
            logging.info(f"data frame has no. of columns {len(data.columns)}")
            if((len(data.columns)) == no_of_columns):
                return True
            else:
                return False


        except Exception as e:
            raise CustomException(e,sys)

    def detect_data_drift(self, base_df:pd.DataFrame, curr_df:pd.DataFrame , threshold = 0.5):
        try:
            status = True
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = curr_df[col]

                is_samp_dist = ks_2samp(d1,d2)
                if threshold<= is_samp_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({col:{
                    "p_value" : float(is_samp_dist.pvalue),
                    "drift_status":is_found
                }})
            
            drift_report_filepath = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_filepath)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path = drift_report_filepath, content=report)
            return status

        except Exception as e:
            raise CustomException(e,sys)
                
    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## read the data from train and test paths:
            train_data:pd.DataFrame = self.readDataFunction(train_file_path)
            test_data:pd.DataFrame = self.readDataFunction(test_file_path)

            ## validate the no.of columns
            train_status = self.validate_columns(data=train_data)
            if(train_status == False):
                error_message = "Train Dataframe has not all columns"
            
            test_status = self.validate_columns(data=test_data)
            if not test_status:
                error_message_t = "test dataframe has not all columns"

            ## check for data drift
            status = self.detect_data_drift(base_df=train_data, curr_df= test_data)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path , exist_ok=True)


            train_data.to_csv(self.data_validation_config.valid_train_file_path , index = False,  header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path , index= False , header= True)

            datavalidationartifact = DataValidationArtifact(
                validation_status= status,
                validated_train_file_path= self.data_ingestion_artifact.trained_file_path,
                validated_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return datavalidationartifact


        except Exception as e:
            raise CustomException(e,sys)