from netwoksecurity.entity.artifact_entity import ClassificationArtifact
from netwoksecurity.exception.exception import CustomException
from sklearn.metrics import f1_score,recall_score,precision_score
import os,sys


def get_classification_score(y_train,y_pred):
    try:
        model_f1_score = f1_score(y_train,y_pred)
        model_recall_score = recall_score(y_train,y_pred)
        model_precission_score = precision_score(y_train,y_pred)

        classification_metric = ClassificationArtifact(
            f1_score= model_f1_score,
            precission_score= model_precission_score,
            recall_score=model_recall_score,
            
        )
        return classification_metric


    except Exception as e:
        raise CustomException(e,sys)