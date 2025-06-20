from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.components.data_validation import Datavalidation
from netwoksecurity.components.data_transformation import DataTransformation
from netwoksecurity.components.model_trainer import ModelTrainer
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionconfig , DataValidationconfig, DataTransformationConfig,ModelTrainerconfig
from netwoksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact , DataTransformartifact
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
        transform = DataTransformation(dv_artifact,DataTransformationConfig(tpg))
        dt_artifacts = transform.initiate_data_transformation()
        print(dt_artifacts)
        logging.info("starting model training ....")
        trainer = ModelTrainer(ModelTrainerconfig(tpg), dt_artifacts)
        mt_artifact = trainer.initiate_model_training()
        logging.info("model trainer artifact created")
        print(mt_artifact)







        

        
    except Exception as e:
        raise CustomException(e,sys)
 
