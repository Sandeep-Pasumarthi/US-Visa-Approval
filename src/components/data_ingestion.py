from src.entity.config import DataIngestionConfig
from src.entity.artifact import DataIngestionArtifact
from src.utils.mongodb import collection_as_dataframe
from src.constants import DATABASE, RAW_DATA_COLLECTION

from sklearn.model_selection import train_test_split
from pandas import DataFrame
from typing import List

import os


class DataIngestion:
    def __init__(self, config: DataIngestionConfig = DataIngestionConfig()):
        self.config = config
    
    def __data_to_feature_store(self) -> DataFrame:
        df = collection_as_dataframe(DATABASE, RAW_DATA_COLLECTION)
        feature_store_file_path = self.config.feature_store_file_path
        feature_store_dir = os.path.dirname(feature_store_file_path)
        os.makedirs(feature_store_dir, exist_ok=True)
        df.to_csv(feature_store_file_path, index=False, header=True)
        return df
    
    def __train_test_split(self, df: DataFrame, split_ratio: float) -> List[DataFrame]:
        train_df, test_df = train_test_split(df, test_size=split_ratio, random_state=17)
        return [train_df, test_df]
    
    def run(self) -> DataIngestionArtifact:
        df = self.__data_to_feature_store()
        train_df, test_df = self.__train_test_split(df, self.config.train_test_split_ratio)
        os.makedirs(os.path.dirname(self.config.train_file_path), exist_ok=True)
        train_df.to_csv(self.config.train_file_path, index=False, header=True)
        test_df.to_csv(self.config.test_file_path, index=False, header=True)
        artifact = DataIngestionArtifact(self.config.train_file_path, self.config.test_file_path)
        return artifact
