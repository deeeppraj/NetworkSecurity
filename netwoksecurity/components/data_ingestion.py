import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os,sys
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

from netwoksecurity.entity.config_entity import DataIngestionconfig
from netwoksecurity.entity.artifact_entity import DataIngestionArtifact
import pymongo

from dotenv import load_dotenv
load_dotenv()

url=  os.getenv("mongo_db_url")

class DataIngestion():
    def __init__(self, data_ingestion_config:DataIngestionconfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_collecction_as_dataframe(self):

        '''
        The function is meant to read my data from mongo db
        
        '''
        try:
            database = self.data_ingestion_config.database_name
            collection = self.data_ingestion_config.collection_name

            self.db = pymongo.MongoClient(url)
            self.dbs = self.db[database]
            self.cls = self.dbs[collection]

            output = list(self.cls.find())
            data = pd.DataFrame(output)
            if "_id" in data.columns:
                data.drop("_id" , axis = 1 , inplace=True)
            else:
                pass
            return data

        except Exception as e:
            raise CustomException(e,sys)
        


    def export_data_to_feature_store(self, data:pd.DataFrame):
        try:
            feat_store_file_path = self.data_ingestion_config.feat_store_filepath
            dir_path = os.path.dirname(feat_store_file_path)
            os.makedirs(dir_path , exist_ok=True)
            data.to_csv(feat_store_file_path,header= True ,index=False)
            return data
        
        except Exception as e:
            raise CustomException(e,sys)


    def split_train_test(self,data:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(data, test_size=self.data_ingestion_config.train_test_spplit_ratio , random_state= 42)
            logging.info("performed train test split")
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path ,exist_ok= True)
            logging.info("Exporting train and test .csv")
            train_set.to_csv(self.data_ingestion_config.train_file_path, index= False ,header = True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index= False ,header = True)
            logging.info("Created my train test.csv")


        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_ingestion(self):
        try:
            my_data = self.export_collecction_as_dataframe()
            data = self.export_data_to_feature_store(my_data)
            self.split_train_test(data=data)
            data_ingestion_artifact = DataIngestionArtifact(self.data_ingestion_config.train_file_path,
                                                            self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact


        except Exception as e:
            raise CustomException(e,sys)



