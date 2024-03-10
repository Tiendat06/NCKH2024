import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
class DataBaseUtils:
    __CLIENT = ''
    __MONGO_URL = os.getenv('MONGO_URI')
    __DB_NAME = os.getenv('DATABASE_NAME')
    
    def __init__(self):
        self.__CLIENT = MongoClient(self.__MONGO_URL)
        self.__DB_NAME = self.__CLIENT.get_database(self.__DB_NAME)
    
    def get_collection(self, collection_name):
        return self.__DB_NAME.get_collection(collection_name)
    
    def get_connection():
        return DataBaseUtils()
    
    def close_connection(self):
        return self.__CLIENT.close()
    