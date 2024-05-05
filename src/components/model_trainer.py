from src.entity.config import ModelTrainerConfig
from src.entity.artifact import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from src.entity.estimator import Predictor
from src.utils.file import read_npy_file, read_yaml_file, load_obj_file, save_obj_file

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

from typing import Tuple

import numpy as np


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig = ModelTrainerConfig()):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    
    def train(self, train: np.array, test: np.array) -> Tuple[object, object]:
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]
        
        model_params = read_yaml_file(self.model_trainer_config.model_config_file_path)
        model_params = model_params["model_params"]

        model = KNeighborsClassifier(**model_params)
        model.fit(train_X, train_y)
        pred_test_y = model.predict(test_X)

        f1 = f1_score(pred_test_y, test_y)
        precision = precision_score(pred_test_y, test_y)
        recall = recall_score(pred_test_y, test_y)
        metric_artifact = ClassificationMetricArtifact(f1, precision, recall)
        return model, metric_artifact
    
    def run(self) -> ModelTrainerArtifact:
        train = read_npy_file(self.data_transformation_artifact.transformed_train_path)
        test = read_npy_file(self.data_transformation_artifact.transformed_test_path)
        
        model, metric_artifact = self.train(train, test)

        preprocessor = load_obj_file(self.data_transformation_artifact.preprocessing_file_path)
        predictor = Predictor(preprocessor, model)
        save_obj_file(self.model_trainer_config.trained_model_file_path, predictor)
        
        artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path, metric_artifact)
        return artifact
