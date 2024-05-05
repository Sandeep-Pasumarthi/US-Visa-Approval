from src.constants import TARGET_COLUMN, SCHEMA_FILE, CURRENT_YEAR
from src.entity.config import DataTransformationConfig
from src.entity.artifact import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from src.entity.estimator import TargetValueMapping
from src.utils.file import save_obj_file, write_npy_file, read_yaml_file

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from imblearn.combine import SMOTEENN

import pandas as pd
import numpy as np


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig=DataTransformationConfig()):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config
        self.__schema = read_yaml_file(SCHEMA_FILE)
    
    def get_transformer_obj(self) -> Pipeline:
        oh_columns = self.__schema["oh_columns"]
        or_columns = self.__schema["or_columns"]
        transform_columns = self.__schema["transform_columns"]
        num_features = self.__schema["num_features"]

        transformer_obj = ColumnTransformer([
            ("OneHotEncoder", OneHotEncoder(), oh_columns),
            ("OrdinalEncoder", OrdinalEncoder(), or_columns),
            ("PowerTransformer", PowerTransformer(method="yeo-johnson"), transform_columns),
            ("StandardScaler", StandardScaler(), num_features)
        ])
        return transformer_obj
    
    def run(self) -> DataTransformationArtifact:
        preprocessor = self.get_transformer_obj()
        drop_columns = self.__schema["drop_columns"]
        train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
        test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

        train_X = train_df.drop([TARGET_COLUMN], axis=1)
        train_y = train_df[TARGET_COLUMN]

        train_X["company_age"] = CURRENT_YEAR - train_X["yr_of_estab"]

        train_X = train_X.drop(drop_columns, axis=1)
        train_y = train_y.replace(TargetValueMapping().__dict__)

        test_X = test_df.drop([TARGET_COLUMN], axis=1)
        test_y = test_df[TARGET_COLUMN]

        test_X["company_age"] = CURRENT_YEAR - test_X["yr_of_estab"]

        test_X = test_X.drop(drop_columns, axis=1)
        test_y = test_y.replace(TargetValueMapping().__dict__)

        train_X = preprocessor.fit_transform(train_X)
        test_X = preprocessor.transform(test_X)

        smt = SMOTEENN(sampling_strategy="minority")
        train_X, train_y = smt.fit_resample(train_X, train_y)
        test_X, test_y = smt.fit_resample(test_X, test_y)

        train = np.c_[train_X, np.array(train_y)]
        test = np.c_[test_X, np.array(test_y)]

        save_obj_file(self.data_transformation_config.transformed_object_file_path, preprocessor)
        write_npy_file(self.data_transformation_config.transformed_train_file_path, train)
        write_npy_file(self.data_transformation_config.transformed_test_file_path, test)

        artifact = DataTransformationArtifact(self.data_transformation_config.transformed_object_file_path,
                                              self.data_transformation_config.transformed_train_file_path,
                                              self.data_transformation_config.transformed_test_file_path)
        return artifact
