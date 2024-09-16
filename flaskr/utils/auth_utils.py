import jwt
from flask import request, jsonify
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from flaskr.models.user import User

def get_secret_key():
    return current_app.config.get('SECRET_KEY', 'your_default_secret_key')

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now() + datetime.timedelta(days=10),
        'iat': datetime.datetime.now()
    }
    return jwt.encode(payload, get_secret_key(), algorithm='HS256')

def verify_jwt(token):
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None 
    except jwt.InvalidTokenError:
        print("Token is invalid")
        return None  

def role_required(role):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                auth_header = request.headers.get('Authorization', None)
                
                if not auth_header or not auth_header.startswith('Bearer '):
                    return jsonify({'error': 'Missing or invalid JWT token'}), 401

                token = auth_header.split(' ')[1]
                print(token)
                user_id = verify_jwt(token)
                print(user_id)
                
                if user_id is None:
                    return jsonify({'error': 'Invalid or expired token'}), 401

                db = current_app.config['DATABASE']
                user = db.fetch_one(User, filters={'user_id': user_id})

                if user is None or user.role != role:
                    return jsonify({'error': 'Access forbidden: insufficient role'}), 403
                
                current_user = user
                
                return f(*args, **kwargs)

            return wrapped
        return wrapper
