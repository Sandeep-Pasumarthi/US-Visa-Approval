from src.entity.config import DataValidationConfig
from src.entity.artifact import DataIngestionArtifact, DataValidationArtifact
from src.constants import SCHEMA_FILE
from src.utils.file import read_yaml_file, write_yaml_file

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from pandas import DataFrame

import json
import pandas as pd


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig = DataValidationConfig()):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self.__schema = read_yaml_file(SCHEMA_FILE)
    
    def validate_num_columns(self, df: DataFrame) -> bool:
        status = df.shape[-1] == len(self.__schema["columns"])
        return status
    
    def is_columns_exists(self, df: DataFrame) -> bool:
        columns = df.columns

        missing_num_columns = [col for col in self.__schema["numerical_columns"] if col not in columns]
        missing_cat_columns = [col for col in self.__schema["categorical_columns"] if col not in columns]

        if len(missing_num_columns) > 0 or len(missing_cat_columns) > 0:
            return False
        return True
    
    def detect_data_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        profile = Profile(sections=[DataDriftProfileSection()])
        profile.calculate(reference_df, current_df)

        report = profile.json()
        json_report = json.loads(report)

        write_yaml_file(self.data_validation_config.drift_report_file_path, json_report)

        n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
        n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

        status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
        return status
    
    def run(self) -> DataValidationArtifact:
        train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
        test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
        
        message = ""
        status = self.validate_num_columns(train_df)
        if not status:
            message += "Columns are missing in train data"
        
        status = self.validate_num_columns(test_df)
        if not status:
            message += "Columns are missing in test data"
        
        status = self.is_columns_exists(train_df)
        if not status:
            message += "Columns are missing in train data"
        
        status = self.is_columns_exists(test_df)
        if not status:
            message += "Columns are missing in test data"
        
        validation_status = message == ""

        if validation_status:
            status = self.detect_data_drift(train_df, test_df)
            if not status:
                message += "Data drift detected"
            else:
                message += "Data drift not detected"
        
        artifact = DataValidationArtifact(validation_status, message, self.data_validation_config.drift_report_file_path)
        return artifact
