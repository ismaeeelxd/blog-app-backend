# Blog App RESTful API

## Description
This project is a **RESTful API** for a Blog application built using **Flask**. The API provides endpoints for managing users, blogs, and authentication using **JWT (JSON Web Tokens)**. Users can create, edit, delete, and view blog posts. It supports different user roles (Admin, Author, Reader), with authentication for secure access to the resources.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [User Management](#user-management)
  - [Blog Management](#blog-management)
- [Error Handling](#error-handling)

## Features
- **JWT Authentication**: Secure authentication and authorization for user actions.
- **User Roles**: Users can have different roles such as:
  - `admin`: Can manage all users and blogs.
  - `author`: Can create and manage their own blogs.
  - `reader`: Can read blog posts.
- **User Management**: Endpoints for user registration, login, and profile management.
- **Blog Management**: Endpoints to create, update, view, and delete blog posts.
- **Role-based Permissions**: Certain actions are restricted based on the user's role.

## Technologies Used
- **Flask**: A micro web framework for building the API.
- **Flask-JWT-Extended**: For JWT authentication and authorization.
- **SQLAlchemy**: ORM for handling database operations.
- **SQLite3**: The database for storing users, blogs, and related data.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blog-app-backend.git
   cd blog-app-backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables for Flask:
   ```bash
    export DATABASE_TYPE=sql or nosql
    export SQLALCHEMY_DATABASE_URI = sqlite:///flaskr.sqlite
    export NOSQL_DATABASE_URI= your mongodb URI
    export SECRET_KEY=dev
   ```

## Running the Application
1. Start the Flask development server:
   ```bash
   flask run
   ```

2. The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Authentication
- **Login**  
  `POST /auth/login`  
  Request body:  
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```  
  Response: JWT token on success.

- **Register**  
  `POST /auth/register`  
  Request body:  
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```  
  Response: Success message and user data.

### User Management
- **Get User Profile**  
  `GET /api/users/<user_id>`  
  - Requires JWT token.
  - Accessible by `admin` and `user` with correct permissions.

- **Update User Profile**  
  `PUT /api/users/<user_id>`  
  - Requires JWT token.

- **Delete User**  
  `DELETE /api/users/<user_id>`  
  - Requires JWT token.
  - Admin only.

### Blog Management
- **Create Blog Post**  
  `POST /api/blogs`  
  - Requires JWT token.
  - Only authors and admins can create blog posts.
  
- **Get All Blog Posts**  
  `GET /api/blogs`  
  - Public access.

- **Get Single Blog Post**  
  `GET /api/blogs/<blog_id>`  
  - Public access.

- **Update Blog Post**  
  `PUT /api/blogs/<blog_id>`  
  - Requires JWT token.
  - Authors can only update their own posts.

- **Delete Blog Post**  
  `DELETE /api/blogs/<blog_id>`  
  - Requires JWT token.
  - Authors can only delete their own posts, Admins can delete any post.

## Error Handling
The API follows a standard error response format:
- **401 Unauthorized**: Returned when JWT token is invalid or missing.
- **403 Forbidden**: Returned when a user attempts an action outside of their permissions.
- **404 Not Found**: Returned when a resource (user, blog post) is not found.
- **400 Bad Request**: Returned for invalid request data.

