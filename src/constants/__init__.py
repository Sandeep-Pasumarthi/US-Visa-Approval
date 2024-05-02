from datetime import date

import os

DATABASE="US_VISA"
RAW_DATA_COLLECTION="raw"
MONGODB_URL_KEY="MONGO_URL"
PIPELINE="usvisa"
ARTIFACT_DIR="artifact"
MODEL_FILE="model.pkl"
TARGET_COLUMN="case_status"
CURRENT_YEAR=date.today().year
PREPROCESSING_FILE="preprocessing.pkl"
RAW_DATA_FILE="raw.csv"
TRAIN_DATA_FILE="train.csv"
TEST_DATA_FILE="test.csv"
SCHEMA_FILE=os.path.join("config", "schema.yaml")

DATA_INGESTION_DIR="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2

DATA_VALIDATION_DIR="data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE="report.yaml"