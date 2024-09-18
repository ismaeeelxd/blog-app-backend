from flask import request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.utils.auth_utils import generate_jwt
from flaskr.models.user import User


class AuthController:

    @staticmethod
    def register(request):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        error = None
        db = current_app.config['DATABASE']
        if db.fetch_one(User, filters={'username': username}):
            error = f'User {username} is already registered.'
        if role == None:
            role = "reader"
        if error is None:
            password_hash = generate_password_hash(password)
            new_user = User(username=username, password_hash=password_hash, role=role)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully"}), 201
        else:
            return jsonify({"error": error}), 400

    @staticmethod
    def login(request):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        error = None
        db = current_app.config['DATABASE']

        user = db.fetch_one(User, filters={'username': username})

        if user is None or not check_password_hash(user.password_hash, password):
            error = 'Invalid credentials'

        if error is None:
            token = generate_jwt(user.id)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": error}), 401
        
