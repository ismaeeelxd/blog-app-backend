from flask import current_app
from flaskr.db.sql_db import SQLDatabase
from flaskr.db.nosql_db import NoSQLDatabase

def get_db():
    db = current_app.config['DATABASE']
    if isinstance(db, SQLDatabase):
        return db
    elif isinstance(db, NoSQLDatabase):
        return db
    else:
        raise TypeError("Unsupported database type")
