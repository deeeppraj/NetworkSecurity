from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.components.data_validation import Datavalidation
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionconfig , DataValidationconfig
from netwoksecurity.entity.artifact_entity import DataIngestionArtifact
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
        logging.info("Ingestion completed . starting data validation")
        valid = Datavalidation(DataIngestionArtifact(artifact.trained_file_path, artifact.test_file_path),DataValidationconfig(tpg))
        dv_artifact = valid.initiate_data_validation()
        logging.info("data validation completed")
        print(dv_artifact)



        

        
    except Exception as e:
        raise CustomException(e,sys)
 
