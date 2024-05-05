from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    preprocessing_file_path: str
    transformed_train_path: str
    transformed_test_path: str
