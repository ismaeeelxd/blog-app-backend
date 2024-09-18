from flask import jsonify, current_app
from flaskr.models.blog import Blog
from flaskr.models.user import User
class BlogController:

    @staticmethod
    def get_all_blogs():
        db = current_app.config['DATABASE']
        blogs = db.fetch_all(Blog)  
        blogs_list = [{'id': blog.id, 'title': blog.title, 'content': blog.content, 'author_id' : blog.author_id} for blog in blogs]
        return jsonify(blogs_list), 200
    
    @staticmethod 
    def get_blog_by_id(blog_id):
        db = current_app.config['DATABASE']
        blog_by_id = db.fetch_one(Blog, filters={'id': blog_id})
        author = db.fetch_one(User,filters = {'user_id' : blog_by_id.author_id})
        if blog_by_id:
            blog = {
                'id': blog_by_id.id,
                'title': blog_by_id.title,
                'content': blog_by_id.content,
                'author': {
                    'id': author.user_id,
                    'username': author.username,
                    'email': author.email, 
                }
            }
            return jsonify(blog), 200
        
        return jsonify({"error": "Blog not found"}), 404
    
    @staticmethod
    def create_blog(request, current_user_id):
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        db = current_app.config['DATABASE']

        new_blog = db.create_record(Blog, title=title, content=content, author_id=current_user_id)

        return jsonify({
            "id": new_blog.id,
            "title": new_blog.title,
            "content": new_blog.content,
            "author_id": new_blog.author_id
        }), 201

    @staticmethod
    def update_blog(blog_id, current_user, request):
        db = current_app.config['DATABASE']
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        blog = db.fetch_one(Blog, filters={"id": blog_id})

        if not blog:
            return jsonify({"error": "Blog not found"}), 404

        if blog.author_id != current_user.user_id and current_user.role != "admin":
            return jsonify({"error": "You do not have permission to update this blog"}), 403

        db.update_record(Blog, filters={"id": blog_id}, title=title, content=content)

        blog_after_update = db.fetch_one(Blog, filters={"id": blog_id})

        return jsonify({
            "id": blog_after_update.id,
            "title": blog_after_update.title,
            "content": blog_after_update.content
        }), 200

    @staticmethod
    def delete_blog(blog_id, current_user):
        db = current_app.config['DATABASE']

        blog = db.fetch_one(Blog, filters={"id": blog_id})

        if not blog:
            return jsonify({"error": "Blog not found"}), 404

        if blog.author_id != current_user.user_id and current_user.role != "admin":
            return jsonify({"error": "You do not have permission to delete this blog"}), 403

        db.delete_record(Blog, filters={"id": blog_id})
        return jsonify({"message": "Blog deleted successfully"}), 200
