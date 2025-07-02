from app.models.user import User
from app.extensions import db

class UserService:
    @staticmethod
    def get_all_users():
        """Get all users"""
        users = User.query.all()
        return [user.to_dict() for user in users]
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        return user.to_dict() if user else None
    
    @staticmethod
    def create_user(data):
        """Create new user"""
        user = User(
            name=data['name'],
            email=data.get('email')
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict()
    
    @staticmethod
    def update_user(user_id, data):
        """Update user"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        return user.to_dict()
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
