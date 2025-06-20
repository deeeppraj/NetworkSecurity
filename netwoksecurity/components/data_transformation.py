import os,sys
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from netwoksecurity.constants.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATIO_IN_PARAMS
from netwoksecurity.entity.artifact_entity import DataValidationArtifact , DataTransformartifact
from netwoksecurity.entity.config_entity import DataTransformationConfig
from netwoksecurity.utils.main_utils.utils import save_numpy_array, save_pikle


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
        

    def readData(self , file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_null_values_pipeline(self):
        logging.info("Entered to get null values")
        try:
            null_pipeline:Pipeline = Pipeline([
                ("KNN Imputer", KNNImputer(**DATA_TRANSFORMATIO_IN_PARAMS))
            ]

            )
            logging.info(f"created my imputer pipeline with values as {DATA_TRANSFORMATIO_IN_PARAMS}")

            return null_pipeline
        
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self):
        logging.info("Initiating my data transformation processs")
        try:
            logging.info("starting.....")
            # reading my dataset
            train_path = self.data_validation_artifact.validated_train_file_path
            test_path= self.data_validation_artifact.validated_test_file_path
            train_data:pd.DataFrame = self.readData(train_path)
            test_data:pd.DataFrame = self.readData(test_path)
            logging.info("read my train and test data as pandas dataframe")
            
            #training dataframe
            input_feat_train_df = train_data.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_data[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #testing dataframe
            input_feat_test_df = test_data.drop(TARGET_COLUMN,axis=1)
            target_feat_test_df = test_data[TARGET_COLUMN]
            target_feat_test_df = target_feat_test_df.replace(-1,0)

            # Handling my null values:
            preprocessor:Pipeline = self.get_null_values_pipeline()
            transformed_input_feat_train_df = preprocessor.fit_transform(input_feat_train_df)
            transformed_input_feat_test_df = preprocessor.transform(input_feat_test_df)

            # combining this with my output to get a numpy array
            # Convert to numpy arrays
            train_y = np.array(target_feature_train_df)
            test_y = np.array(target_feat_test_df)

            # Filter out rows where target is NaN
            train_mask = ~np.isnan(train_y)
            test_mask = ~np.isnan(test_y)

            transformed_input_feat_train_df = transformed_input_feat_train_df[train_mask]
            train_y = train_y[train_mask]

            transformed_input_feat_test_df = transformed_input_feat_test_df[test_mask]
            test_y = test_y[test_mask]

            # Combine features and target
            train_array = np.c_[transformed_input_feat_train_df, train_y]
            test_array = np.c_[transformed_input_feat_test_df, test_y]


            

            save_numpy_array(file_path=self.data_transformation_config.transformed_train_file_path , array=train_array)
            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path , array=test_array)
            save_pikle(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor)
            logging.info("saved my numpy array and my preprocessor.pkl file")

            data_transformation_artifact = DataTransformartifact(
                transformed_obj_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path

            )
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)
        

        