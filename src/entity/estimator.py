from sklearn.pipeline import Pipeline
from pandas import DataFrame


class TargetValueMapping:
    def __init__(self):
        self.Certified = 0
        self.Denied = 1
    
    def reverse_mapping(self):
        mapping = self.__dict__
        return dict(zip(mapping.values(), mapping.keys()))


class Predictor:
    def __init__(self, preprocessor: Pipeline, model: object):
        self.preprocessor = preprocessor
        self.model = model
    
    def predict(self, data: DataFrame) -> DataFrame:
        transformed_data = self.preprocessor.transform(data)
        return self.model.predict(transformed_data)
