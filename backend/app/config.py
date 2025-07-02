import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # MQTT Configuration
    MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST')
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT'))
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
