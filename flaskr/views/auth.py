
from flask import Blueprint, request, jsonify
from flaskr.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    return AuthController.register(request)

@bp.route('/login', methods=['POST'])
def login():
    return AuthController.login(request)




