from src.entity.estimator import Predictor
from src.aws.s3 import SimpleStorageService

from pandas import DataFrame


class S3Predictor:
    def __init__(self, bucket_name: str, model_path: str):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.s3 = SimpleStorageService()
    
    def is_model_present(self):
        return self.s3.is_s3key_path_available(self.bucket_name, self.model_path)
    
    def load_model(self) -> Predictor:
        return self.s3.load_pkl_file(self.model_path, self.bucket_name)
    
    def save_model(self, from_path: str, remove: bool=False):
        self.s3.upload_file(from_path, self.model_path, self.bucket_name, remove)
    
    def predict(self, data: DataFrame) -> DataFrame:
        model = self.load_model()
        return model.predict(data)
