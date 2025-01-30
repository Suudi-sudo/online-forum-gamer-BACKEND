from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User
from . import auth_bp

# Token blocklist for logout
BLOCKLIST = set()

# CREATE - Register a new user
@auth_bp.route('/user', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    hashed_password = generate_password_hash(data['password'])
    user = User(email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# READ - Getting the logged-in user's information
@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({
            'user_id': user.user_id,
            'email': user.email
        }), 200
    return jsonify({'message': 'User not found'}), 404

# UPDATE - Update user's password (using PATCH)
@auth_bp.route('/change-password', methods=['PATCH'])
@jwt_required()
def change_password():
    data = request.json
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user and check_password_hash(user.password, data['old_password']):
        user.password = generate_password_hash(data['new_password'])
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# DELETE - Delete a user account
@auth_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User account deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

# LOGIN - Log in and get access token
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.user_id)
        return jsonify({'access_token': access_token, 'user_id': user.user_id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# LOGOUT - Logout and invalidate token
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    BLOCKLIST.add(jti)
    return jsonify({'message': 'Logged out successfully'}), 200

# Middleware to check token validity and handle OPTIONS requests gracefully
@auth_bp.before_request
@jwt_required(optional=True)  # Allow optional JWT for all requests to handle CORS preflight
def check_blocklist():
    # Check if the request is an OPTIONS request; if so, skip further checks.
    if request.method == "OPTIONS":
        return jsonify({'message': 'CORS preflight request successful.'}), 200
    
    jti = get_jwt().get('jti', None)
    if jti in BLOCKLIST:
        return jsonify({'message': 'Token has been revoked'}), 401
