from src.constants import MONGODB_URL_KEY
from pymongo import MongoClient
from pymongo.collection import Collection

import os
import certifi


class MongoDBclient:
    def __init__(self, database: str) -> None:
        self.client = MongoClient(os.getenv(MONGODB_URL_KEY), tlsCAFile=certifi.where())
        self.database = self.client[database]
        self.database_name = database
    
    def get_collection(self, collection: str) -> Collection:
        return self.database[collection]
