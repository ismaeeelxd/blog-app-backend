from flask import jsonify, current_app
from flaskr.models.user import User
from flaskr.models.blog import Blog
from werkzeug.security import check_password_hash, generate_password_hash

class UserController:

    @staticmethod
    def get_all_users():
        db = current_app.config['DATABASE']
        users = db.fetch_all(User)  
        users_list = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_list), 200
    
    @staticmethod 
    def get_user_by_id(id):
        db = current_app.config['DATABASE']
        user_by_id = db.fetch_one(User, filters={'id': id})
        if user_by_id:
            user = {
                'id': user_by_id.id,
                'username': user_by_id.username
            }
            return jsonify(user), 200
        
        return jsonify({"error": "User not found"}), 404
    
    @staticmethod
    def create_user(request):
        data = request.get_json()
        username = data.get('username')
        role = data.get('role')
        password = data.get('password')
        if password: 
            password = generate_password_hash(password)
        if role == None:
            role = 'reader'
        db = current_app.config['DATABASE']
        error = None
        if db.fetch_one(User, filters={'username': username}):
            error = f'User {username} is already registered.'

        if error is None:
            new_user = db.create_record(User, username=username, role=role, password_hash= password)
            print(new_user)
            return jsonify({
                "id": new_user.id,
                "username": new_user.username,
                "role": new_user.role
            }), 201
        else:
            return jsonify({
                "msg" : error
            })

    @staticmethod
    def update_user(id,current_user, request):
        db = current_app.config['DATABASE']
        data = request.get_json()
        username = data.get('username')
        role = data.get('role')
        password = data.get('password')
        if password: 
            password = generate_password_hash(password)
        user = db.fetch_one(User, filters={"id": id})
        print(user)
        if user.id != current_user.id and current_user.role != "admin":
            return jsonify({"error": "You do not have permission to update this User"}), 403

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if db.fetch_one(User, filters={'username': username}):
            return jsonify({"error" : f'User {username} is already registered.'})



        user_updated = db.update_record(User, filters={"id": id}, username=username,role=role,password=password)

        return jsonify({
            "id": user_updated.id,
            "username": user_updated.username,
            "role" : user_updated.role,
        }), 200

    @staticmethod
    def delete_user(id, current_user):
        db = current_app.config['DATABASE']

        user = db.fetch_one(User, filters={"id": id})

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.id != current_user.id and current_user.role != "admin":
            return jsonify({"error": "You do not have permission to delete this User"}), 403

        db.delete_record(User, filters={"id": id})
        return jsonify({"message": "User deleted successfully"}), 200
