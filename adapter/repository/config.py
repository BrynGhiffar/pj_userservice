import os
from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("MONGO_DB_NAME")

    client = MongoClient(CONNECTION_STRING)
    if not DB_NAME:
        DB_NAME = "mongodb://localhost:27017/"

    return client[DB_NAME]