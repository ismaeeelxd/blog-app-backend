from flask import Blueprint, request,g
from flaskr.controllers.blog_controller import BlogController
from flaskr.utils.auth_utils import role_required

blog_bp = Blueprint('blog', __name__, url_prefix='/api/blogs')

@blog_bp.route('/', methods=['GET'])
@role_required(['reader', 'author', 'admin'])
def get_all_blogs():
    return BlogController.get_all_blogs()

@blog_bp.route('/<int:blog_id>', methods=['GET'])
@role_required(['reader', 'author', 'admin'])
def get_blog_by_id(blog_id):
    return BlogController.get_blog_by_id(blog_id)

@blog_bp.route('/', methods=['POST'])
@role_required(['author', 'admin'])
def create_blog():
    return BlogController.create_blog(request,g.current_user.user_id)

@blog_bp.route('/<int:blog_id>', methods=['PUT'])
@role_required(['author', 'admin'])
def update_blog(blog_id):
    return BlogController.update_blog(blog_id, g.current_user,request)

@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
@role_required(['author', 'admin'])
def delete_blog(blog_id):
    return BlogController.delete_blog(blog_id, g.current_user)
