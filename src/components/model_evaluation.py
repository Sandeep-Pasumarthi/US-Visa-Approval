from src.entity.config import ModelEvaluationConfig
from src.entity.artifact import DataIngestionArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from src.entity.s3_estimator import S3Predictor
from src.entity.estimator import Predictor, TargetValueMapping
from src.constants import TARGET_COLUMN, CURRENT_YEAR

from sklearn.metrics import f1_score
from typing import Optional
from dataclasses import dataclass

import pandas as pd


@dataclass
class EvaluateModelResponse:
    new_model_f1_Score: float
    s3_model_f1_Score: float
    is_model_accepted: bool
    difference_score: float


class ModelEvaluation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact, model_evaluation_config: ModelEvaluationConfig = ModelEvaluationConfig()):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_evaluation_config = model_evaluation_config
    
    def get_s3_model(self) -> Optional[S3Predictor]:
        bucket_name = self.model_evaluation_config.bucket_name
        model_path = self.model_evaluation_config.s3_model_file_path
        
        s3_predictor = S3Predictor(bucket_name, model_path)
        if s3_predictor.is_model_present():
            return s3_predictor
        return None
    
    def evaluate_models(self) -> EvaluateModelResponse:
        test = pd.read_csv(self.data_ingestion_artifact.test_file_path)
        test["company_age"] = CURRENT_YEAR - test["yr_of_estab"]
        
        test_X = test.drop([TARGET_COLUMN], axis=1)
        test_y = test[TARGET_COLUMN]
        test_y = test_y.replace(TargetValueMapping().__dict__)

        new_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
        s3_model_f1_score = 0
        
        s3_model = self.get_s3_model()
        if s3_model is not None:
            predict_y = s3_model.predict(test_X)
            s3_model_f1_score = f1_score(predict_y, test_y)

        response = EvaluateModelResponse(new_model_f1_score, s3_model_f1_score, new_model_f1_score > s3_model_f1_score, new_model_f1_score - s3_model_f1_score)        
        return response
    
    def run(self) -> ModelEvaluationArtifact:
        model_evaluation_response = self.evaluate_models()
        model_evaluation_artifact = ModelEvaluationArtifact(
            model_evaluation_response.is_model_accepted,
            model_evaluation_response.difference_score,
            self.model_evaluation_config.s3_model_file_path,
            self.model_trainer_artifact.model_file_path)
        return model_evaluation_artifact
