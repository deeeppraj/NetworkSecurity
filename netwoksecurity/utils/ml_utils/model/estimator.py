from netwoksecurity.constants.training_pipeline import MODEL_PICKLE_FILE , SAVED_MODEL_DIR  
import os,sys
from netwoksecurity.exception.exception import  CustomException
from netwoksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,processor,model):
        try:
            self.processor = processor
            self.model =  model
        except Exception as e:
            raise CustomException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.processor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)
        