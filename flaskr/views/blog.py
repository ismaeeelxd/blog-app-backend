from flask import Blueprint, request, jsonify
# from flaskr.controllers.blog_controller import BlogController
from flaskr.utils.auth_utils import role_required
from flask import current_app
from flaskr.models.blog import Blog
blog_bp = Blueprint('blog', __name__, url_prefix='/api/blogs')


@blog_bp.route('/', methods=['GET'])
@role_required('reader') 
def get_all_blogs():
        db = current_app.config['DATABASE']
        blogs = db.fetch_all(Blog)  
        blogs_list = [{'id': blog.id, 'title': blog.title, 'content': blog.content} for blog in blogs]
        return jsonify(blogs_list), 200



