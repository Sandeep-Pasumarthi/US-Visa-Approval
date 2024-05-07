from src.entity.config import PredictorConfig
from src.entity.s3_estimator import S3Predictor

from pandas import DataFrame


class Data:
    def __init__(self, continent, education_of_employee, has_job_experience, requires_job_training, no_of_employees, region_of_employment, prevailing_wage, unit_of_wage, full_time_position, company_age):
        self.continent = continent
        self.education_of_employee = education_of_employee
        self.has_job_experience = has_job_experience
        self.requires_job_training = requires_job_training
        self.no_of_employees = no_of_employees
        self.region_of_employment = region_of_employment
        self.prevailing_wage = prevailing_wage
        self.unit_of_wage = unit_of_wage
        self.full_time_position = full_time_position
        self.company_age = company_age
    
    def as_dict(self) -> dict:
        data = {
            "continent": [self.continent],
            "education_of_employee": [self.education_of_employee],
            "has_job_experience": [self.has_job_experience],
            "requires_job_training": [self.requires_job_training],
            "no_of_employees": [self.no_of_employees],
            "region_of_employment": [self.region_of_employment],
            "prevailing_wage": [self.prevailing_wage],
            "unit_of_wage": [self.unit_of_wage],
            "full_time_position": [self.full_time_position],
            "company_age": [self.company_age]
        }
        return data
    
    def as_dataframe(self) -> DataFrame:
        return DataFrame(self.as_dict())


class Classifier:
    def __init__(self, predictor_config: PredictorConfig = PredictorConfig()):
        self.predictor_config = predictor_config
    
    def predict(self, data: DataFrame) -> DataFrame:
        model = S3Predictor(self.predictor_config.bucket_name, self.predictor_config.model_file_path)
        return model.predict(data)
