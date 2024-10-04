from flask_sqlalchemy import SQLAlchemy
from flaskr.db.abstract_db import AbstractDatabase
import logging
db = SQLAlchemy()

class SQLDatabase(AbstractDatabase):
    
    def __init__(self):
        self.session = db.session
    
    def init_app(self, app):
        db.init_app(app)

    def connect(self):
        return self.session

    def close(self):
        self.session.close()

    def execute_query(self, query, params=None):
        pass

    def fetch_all(self, model, filters=None):
        session = self.connect()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
                print(query)
            return query.all()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_one(self, model, filters=None):
        session = self.connect()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
            return query.first()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_record(self, model, **kwargs):
        session = self.connect()
        try:
            record = model(**kwargs)
            session.add(record)
            session.commit() 
            logging.info(f"Record created with ID: {record.id}")
            return record
        except Exception as e:
            session.rollback() 
            logging.error(f"Error creating record: {e}")
 
            raise e
        finally:
            session.close()

    def update_record(self, model, filters=None, **kwargs):
        session = self.connect()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
            record = query.first()
            if record:
                for key, value in kwargs.items():
                    if value == None or key == None:
                        continue
                    setattr(record, key, value)
                session.commit()
                logging.info(f"Record updated with ID: {record.id}")
                return record
            return None
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating record: {e}")

            raise e
        finally:
            session.close()

    def delete_record(self, model,filters=None):
        session = self.connect()
        try:
            query = session.query(model)
            if filters:
                query = query.filter_by(**filters)
            record = query.first()
            if record:
                session.delete(record)
                session.commit()
                logging.info(f"Record deleted with ID: {record.id}")
                return True
            return False
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting record: {e}")
            raise e
        finally:
            session.close()

    def create_tables(self, app):
        with app.app_context():
            db.create_all()
