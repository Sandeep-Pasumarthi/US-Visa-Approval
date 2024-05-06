from src.configuration.aws_connector import S3Client

from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError

from io import StringIO
from typing import Union, List
from pandas import DataFrame

import boto3
import pickle
import os


class SimpleStorageService:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client
    
    def get_bucket(self, name: str) -> Bucket:
        return self.s3_resource.Bucket(name)
    
    def is_s3key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        bucket = self.get_bucket(bucket_name)
        file_objs = [file for file in bucket.objects.filter(Prefix=s3_key)]
        return len(file_objs) > 0
    
    def upload_file(self, from_path: str, to_path: str, bucket_name: str, remove: bool=True):
        self.s3_resource.meta.client.upload_file(from_path, bucket_name, to_path)

        if remove:
            os.remove(from_path)
    
    def get_file_obj(self, filename: str, bucket_name: str) -> Union[List[object], object]:
        bucket = self.get_bucket(bucket_name)
        file_objs = [file for file in bucket.objects.filter(Prefix=filename)]
        
        func = lambda x: x[0] if len(x) == 1 else x
        file_objs = func(file_objs)
        return file_objs
    
    def load_pkl_file(self, model_name: str, bucket_name: str, model_dir: str) -> object:
        func = lambda: model_name if model_dir is None else model_dir + "/" + model_name
        model_path = func()
        file_obj = self.get_file_obj(model_path, bucket_name)
        model_obj = self.read_object(file_obj)
        model = pickle.loads(model_obj)
        return model

    @staticmethod
    def read_object(object, decode: bool=True, make_readable: bool=False) -> Union[StringIO, str]:
        body = object.get()["Body"].read()

        if decode:
            body = body.decode()
        
        if make_readable:
            return StringIO(body)
        return body
