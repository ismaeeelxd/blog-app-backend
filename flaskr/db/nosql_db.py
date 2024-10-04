from flask import current_app
from flaskr.db.abstract_db import AbstractDatabase
from pymongo import MongoClient

class NoSQLDatabase(AbstractDatabase):
    
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        if self.client is None:
            self.client = MongoClient(current_app.config['NOSQL_DATABASE_URI'])
            self.db = self.client.get_database()
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def execute_query(self, query, params=None):
        pass

    def fetch_all(self, query, params=None):
        collection = self.db.get_collection('my_collection')
        return list(collection.find(query, params))

    def fetch_one(self, query, params=None):
        collection = self.db.get_collection('my_collection')
        return collection.find_one(query, params)
