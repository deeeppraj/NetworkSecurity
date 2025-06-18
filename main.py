from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionconfig
import sys
from netwoksecurity.entity.config_entity import training_pipeline_config

if __name__ == "__main__":
    try:
        tpg = training_pipeline_config()
        config = DataIngestionconfig(tpg)
        ingest= DataIngestion(config)
        logging.info("Initiating my ingestion process")
        artifact = ingest.initiate_ingestion()
        print(artifact)

        
    except Exception as e:
        raise CustomException(e,sys)
 
