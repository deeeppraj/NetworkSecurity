import os,sys
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.components.data_transformation import DataTransformation
from netwoksecurity.components.data_validation import Datavalidation
from netwoksecurity.components.model_trainer import ModelTrainer

from netwoksecurity.entity.config_entity import(
    training_pipeline_config,
    DataIngestionconfig,
    DataTransformationConfig,
    DataValidationconfig,
    ModelTrainerconfig

)

from netwoksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,DataTransformartifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = training_pipeline_config()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionconfig(self.training_pipeline_config)
            logging.info("initiate data ingestion")
            ingestor = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = ingestor.initiate_ingestion()
            logging.info(f"data ingestion completed . generated data ingestion artifact ->{data_ingestion_artifact}")
            return data_ingestion_artifact
        

        except  Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_vlidation_config = DataValidationconfig(self.training_pipeline_config)
            logging.info("starting data validation")
            validator = Datavalidation(data_ingestion_artifact=self.data_ingestion_artifact, data_validation_config=self.data_vlidation_config)
            data_validation_artifact = validator.initiate_data_validation()
            logging.info(f"completed with {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            transformer = DataTransformation(data_validation_artifact=self.data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = transformer.initiate_data_transformation()
            logging.info(f"completed data transformation {data_transformation_artifact}")
            return data_transformation_artifact

        except CustomException as e:
            raise CustomException(e,sys)
        
    def model_trainer(self,data_transformation_artifact:DataTransformartifact):
        try:

            self.data_transformation_artifact  = data_transformation_artifact
            self.model_trainer_config = ModelTrainerconfig(self.training_pipeline_config)
            trainer = ModelTrainer(model_trainer_config=self.model_trainer_config , data_transform_artifact=self.data_transformation_artifact)
            trainer_artifact = trainer.initiate_model_training()
            logging.info(f"completed model training {trainer_artifact}")
            return trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifat = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.data_transformation(data_validation_artifact=data_validation_artifat)
            model_trainer_artifact = self.model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        