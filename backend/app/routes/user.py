from flask import Blueprint, jsonify, request
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    """Get list of users"""
    users = UserService.get_all_users()
    return jsonify(users)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_bp.route('/', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    user = UserService.create_user(data)
    return jsonify(user), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    data = request.get_json()
    user = UserService.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    if UserService.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
