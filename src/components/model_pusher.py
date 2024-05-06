from src.entity.config import ModelPusherConfig
from src.entity.artifact import ModelEvaluationArtifact, ModelPusherArtifact
from src.entity.s3_estimator import S3Predictor
from src.aws.s3 import SimpleStorageService


class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact, model_pusher_config: ModelPusherConfig=ModelPusherConfig()):
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.s3 = SimpleStorageService()
        self.s3_predictor = S3Predictor(model_pusher_config.bucket_name, model_pusher_config.s3_model_file_path)
    
    def run(self) -> ModelPusherArtifact:
        self.s3_predictor.save_model(self.model_evaluation_artifact.trained_model_path)

        artifact = ModelPusherArtifact(self.model_pusher_config.bucket_name, self.model_pusher_config.s3_model_file_path)
        return artifact
