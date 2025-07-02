from flask import Flask
from flask_cors import CORS
from app.extensions import db, bcrypt, jwt
from app.config import Config
from app.services.mqtt_service import MQTTService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize MQTT service
    MQTTService.initialize(app)
    
    # Register blueprints
    from app.routes.user import user_bp
    from app.routes.mqtt import mqtt_bp
    from app.routes.device import device_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(mqtt_bp)
    app.register_blueprint(device_bp)
    
    # Add a simple health check route
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'AI IoT Tank Backend is running!'}
    
    return app
