import functools
import jwt
from flask import request, jsonify, g
from flaskr.db import get_db
import datetime

SECRET_KEY = 'your_secret_key_here'

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None  

def login_required(f):
    @functools.wraps(f)
    def wrapped_view(**kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({"error": "Authorization token required"}), 401
        
        user_id = verify_jwt(token)
        if user_id is None:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.user_id = user_id
        return f(**kwargs)
    
    return wrapped_view
