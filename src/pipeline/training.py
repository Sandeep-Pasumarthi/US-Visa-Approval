from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher


class TrainingPipeline:
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        ingestion = DataIngestion()
        ingestion_artifact = ingestion.run()

        validation = DataValidation(ingestion_artifact)
        validation_artifact = validation.run()

        transformation = DataTransformation(ingestion_artifact, validation_artifact)
        transformation_artifact = transformation.run()

        trainer = ModelTrainer(transformation_artifact)
        trainer_artifact = trainer.run()

        evaluation = ModelEvaluation(ingestion_artifact, trainer_artifact)
        evaluation_artifact = evaluation.run()

        if not evaluation_artifact.is_model_accepted:
            return None

        pusher = ModelPusher(evaluation_artifact)
        pusher_artifact = pusher.run()
