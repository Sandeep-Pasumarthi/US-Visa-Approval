from src.constants import *
from dataclasses import dataclass
from datetime import datetime

import os

TIME_STAMP = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline = PIPELINE
    artifact_dir = ARTIFACT_DIR
    timestamp = TIME_STAMP


training_pipeline_config_obj = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir=os.path.join(training_pipeline_config_obj.artifact_dir, DATA_INGESTION_DIR)
    feature_store_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, RAW_DATA_FILE)
    train_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, TRAIN_DATA_FILE)
    test_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, TEST_DATA_FILE)
    train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    raw_data_collection = RAW_DATA_COLLECTION
