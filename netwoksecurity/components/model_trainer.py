import os,sys
from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging

from netwoksecurity.entity.artifact_entity import DataTransformartifact,ModelTrainerArtifact
from netwoksecurity.entity.config_entity import ModelTrainerconfig
from netwoksecurity.constants.training_pipeline import TARGET_COLUMN

from netwoksecurity.utils.main_utils.utils import load_numpy_array,save_obj,load_obj,eval_model
from netwoksecurity.utils.ml_utils.metric import classification
from netwoksecurity.utils.ml_utils.model import estimator
import numpy as np
import pandas as pd
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import dagshub
dagshub.init(repo_owner='deeeppraj', repo_name='NetworkSecurity', mlflow=True)



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerconfig,
                 data_transform_artifact:DataTransformartifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact= data_transform_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def mlfow_track(self, best_model, classificationMetric):
        with mlflow.start_run():
            f1_score = classificationMetric.f1_score
            precisson_score = classificationMetric.precission_score
            recall_score = classificationMetric.recall_score
            
            mlflow.log_metric("f1_score",  f1_score)
            mlflow.log_metric("precission" , precisson_score)
            mlflow.log_metric("recall" , recall_score)
            #mlflow.sklearn.log_model(sk_model=best_model, artifact_path="bestmodel")




        
    
    def train_model(self , x_train,y_train,x_test,y_test):
         models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
         params={
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
         
         try:
             report,trained_model  = eval_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)
             best_model_score = max(list(report.values()))
             best_model = list(report.keys())[list(report.values()).index(best_model_score)]
             model = trained_model[best_model]
             y_train_pred = model.predict(x_train)
             classification_train_metric = classification.get_classification_score(y_train=y_train,y_pred=y_train_pred)
             ## track with ml flow
             self.mlfow_track(best_model=model,classificationMetric=classification_train_metric)




             y_test_pred = model.predict(x_test)
             classification_test_metric = classification.get_classification_score(y_train=y_test,y_pred=y_test_pred)
             self.mlfow_track(best_model=model,classificationMetric=classification_test_metric)


             

            

             preprocessor = load_obj(file_path=self.data_transformation_artifact.transformed_obj_file_path)
             dir_path = os.path.dirname(self.model_trainer_config.trained_model_file)
             os.makedirs(dir_path,exist_ok=True)
             
             network_model = estimator.NetworkModel(processor=preprocessor,model=model)
             save_obj(file_path=self.model_trainer_config.trained_model_file , obj= network_model)

             save_obj(file_path="final_model/model.pkl" , obj = model)
            
             model_trainer_artifact = ModelTrainerArtifact(
                 trained_model_file_path=self.model_trainer_config.trained_model_file,
                 trained_metric_artifact= classification_train_metric,
                 test_metric_artifact= classification_test_metric

                
             )
             logging.info(f"model trainer artifact {model_trainer_artifact}")
             return model_trainer_artifact

        

         except Exception as e:
             raise CustomException(e,sys)
         
       
        







    def initiate_model_training(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array: np.array = load_numpy_array(train_file_path)
            test_array: np.array = load_numpy_array(test_file_path)

            

            x_train = train_array[:,:-1]
            y_train = train_array[:,-1]

            x_test = test_array[:,:-1]
            y_test = test_array[:,-1]
            
            train = self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return train

        except Exception as e:
            raise CustomException(e,sys) 