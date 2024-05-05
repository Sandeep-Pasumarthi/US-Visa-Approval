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
    data_ingestion_dir = os.path.join(training_pipeline_config_obj.artifact_dir, DATA_INGESTION_DIR)
    feature_store_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, RAW_DATA_FILE)
    train_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_DATA_FILE)
    test_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_DATA_FILE)
    train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    raw_data_collection = RAW_DATA_COLLECTION


@dataclass
class DataValidationConfig:
    data_validation_dir = os.path.join(training_pipeline_config_obj.artifact_dir, DATA_VALIDATION_DIR)
    drift_report_file_path = os.path.join(data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE)


@dataclass
class DataTransformationConfig:
    data_transformation_dir = os.path.join(training_pipeline_config_obj.artifact_dir, DATA_TRANSFORMATION_DIR)
    transformed_train_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TRAIN_DATA_FILE.replace("csv", "npy"))
    transformed_test_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TEST_DATA_FILE.replace("csv", "npy"))
    transformed_object_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_FILE)
