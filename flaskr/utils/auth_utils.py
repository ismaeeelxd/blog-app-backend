from flask import g, jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from functools import wraps
from flaskr.models.user import User

def generate_jwt(user_id):
    return create_access_token(identity=user_id)

def role_required(roles):
    def wrapper(f):
        @wraps(f)
        @jwt_required()
        def wrapped(*args, **kwargs):
            try:
               
                user_id = get_jwt_identity()

                if not user_id:
                    return jsonify({'error': 'Invalid or expired token'}), 401

                db = current_app.config['DATABASE']
                user = db.fetch_one(User, filters={'user_id': user_id})

                if not user:
                    return jsonify({'error': 'User not found'}), 404

                if user.role not in roles:
                    return jsonify({'error': 'Access forbidden: insufficient role'}), 403

                g.current_user = user

                return f(*args, **kwargs)

            except Exception as e:
                return jsonify({'error': str(e)}), 401

        return wrapped
    return wrapper
