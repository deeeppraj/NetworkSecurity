import os
import sys
from dotenv import load_dotenv
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

load_dotenv()

url = os.getenv("mongo_db_url")
print(url)

ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            output_file = json.loads(data.to_json(orient='records'))
            return output_file
        except Exception as e:
            raise CustomException(e,sys)
        

    def insert_db(self,database,collection,output_file):
        try:
            self.database = database
            self.collection = collection
            self.output_file = output_file

            self.db = pymongo.MongoClient(url)
            self.database = self.db[self.database]
            self.collection = self.database[self.collection]
            
            self.collection.insert_many(self.output_file)

        except Exception as e:
            raise CustomException(e,sys)


if __name__ == "__main__":
    file = "Network_Data/phisingData.csv"
    database = "network"
    collection = "phising"
    extract = NetworkDataExtract()
    json_file = extract.csv_to_json_converter(file_path=file)
    extract.insert_db(database= database, collection=collection,output_file=json_file)
