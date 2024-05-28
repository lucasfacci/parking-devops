from mongomock import MongoClient
import os


class DevConfig:

    MONGODB_SETTINGS = {
        "db": os.getenv("MONGODB_DB"),
        "host": os.getenv("MONGODB_HOST"),
        "username": os.getenv("MONGODB_USER"),
        "password": os.getenv("MONGODB_PASSWORD"),
    }


class ProdConfig:

    MONGODB_DB = os.getenv("MONGODB_DB")
    MONGODB_HOST = os.getenv("MONGODB_HOST")
    MONGODB_USER = os.getenv("MONGODB_USER")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

    URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}/{MONGODB_DB}"
    MONGODB_SETTINGS = {"host": URI}


class MockConfig:

    MONGODB_SETTINGS = {
        "db": "parkingdb",
        "host": "mongodb://localhost",
        "mongo_client_class": MongoClient,
    }
