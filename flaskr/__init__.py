import os
from flask import Flask
from flaskr.db.sql_db import SQLDatabase
from flaskr.db.nosql_db import NoSQLDatabase
from dotenv import load_dotenv
from flaskr.models.user import User  
from flaskr.models.blog import Blog
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
SWAGGER_URL = '/api/docs'
API_URL = "/static/swagger.json"

load_dotenv()



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    db_type = os.getenv('DATABASE_TYPE')
    app.secret_key = os.environ.get('SECRET_KEY', 'dev')

    jwt = JWTManager(app)

    def load_user(user_id):
        return User.query.get(int(user_id))

    if db_type == 'sql':
        db = SQLDatabase()
        app.config['DATABASE'] = db
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)

        
        with app.app_context():
            db.create_tables(app)



    elif db_type == 'nosql':
        db = NoSQLDatabase()
        app.config['DATABASE'] = db
        app.config['NOSQL_DATABASE_URI'] = os.getenv('NOSQL_DATABASE_URI')

    else:
        raise ValueError("Unsupported DATABASE_TYPE")


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .views.auth import auth_bp
    from .views.blog import blog_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
