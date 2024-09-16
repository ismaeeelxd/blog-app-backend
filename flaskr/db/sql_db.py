from flask_sqlalchemy import SQLAlchemy
from flaskr.db.abstract_db import AbstractDatabase

db = SQLAlchemy()

class SQLDatabase(AbstractDatabase):
    
    def __init__(self):
        self.session = db.session
    
    def init_app(self, app):
        db.init_app(app)

    def connect(self):
        return self.session

    def close(self):
        pass

    def execute_query(self, model, filters=None):
        session = self.connect()
        query = session.query(model)
        if filters:
            query = query.filter_by(**filters)
        result = query.all()
        return result

    def fetch_all(self, model, filters=None):
        session = self.connect()
        query = session.query(model)
        if filters:
            query = query.filter_by(**filters)
        return query.all()

    def fetch_one(self, model, filters=None):
        session = self.connect()
        query = session.query(model)
        if filters:
            query = query.filter_by(**filters)
        return query.first()

    def create_tables(self, app):
        with app.app_context():
            db.create_all()
