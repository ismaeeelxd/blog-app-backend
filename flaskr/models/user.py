from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from flaskr.db.sql_db import db
from flask_login import UserMixin


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum('admin', 'reader', 'author', name='user_roles'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    blogs = db.relationship('Blog', backref='author', lazy=True)
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}', role='{self.role}')>"

    def get_id(self):
        return self.user_id


