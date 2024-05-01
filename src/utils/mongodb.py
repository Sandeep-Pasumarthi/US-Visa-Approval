from src.configuration.mongodb_connector import MongoDBclient

import pandas as pd
import numpy as np


def collection_as_dataframe(database, collection) -> pd.DataFrame:
    mongo_client = MongoDBclient(database)
    mongo_collection = mongo_client.get_collection(collection)

    documents = mongo_collection.find({}, {"_id": 0})
    df = pd.DataFrame(list(documents))
    df.replace({"np": np.nan}, inplace=True)
    return df
