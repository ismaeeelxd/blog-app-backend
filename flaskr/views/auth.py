
from flask import Blueprint, request, jsonify
from flaskr.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register(request)

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login(request)




