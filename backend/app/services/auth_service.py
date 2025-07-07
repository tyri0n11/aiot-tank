from app.models.user import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def register(name, email, password):
        if User.query.filter_by(email=email).first():
            return None, "Email already exists"
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password_hash and bcrypt.check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(identity=user.id)
            return access_token, refresh_token, user
        return None, None, None