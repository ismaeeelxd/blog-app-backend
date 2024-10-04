from flask import Blueprint, request,g
from flaskr.controllers.user_controller import UserController
from flaskr.utils.auth_utils import role_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@role_required(['reader', 'author', 'admin'])
def get_all_users():
    return UserController.get_all_users()

@user_bp.route('/<int:user_id>', methods=['GET'])
@role_required(['reader', 'author', 'admin'])
def get_user_by_id(user_id):
    return UserController.get_user_by_id(user_id)

@user_bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_user():
    return UserController.create_user(request)

@user_bp.route('/<int:user_id>', methods=['PUT'])
@role_required(['reader','author','admin'])
def update_user(user_id):
    return UserController.update_user(user_id, g.current_user,request)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required(['reader','author','admin'])
def delete_user(user_id):
    return UserController.delete_user(user_id, g.current_user)
