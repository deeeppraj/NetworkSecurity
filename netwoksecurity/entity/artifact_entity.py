from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    validated_train_file_path : str
    validated_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformartifact:
    transformed_obj_file_path :str
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class ClassificationArtifact:
    f1_score:float
    precission_score:float
    recall_score:float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    trained_metric_artifact:ClassificationArtifact
    test_metric_artifact:ClassificationArtifact
