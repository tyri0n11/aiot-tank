#!/usr/bin/env python3
"""
Database initialization script
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.device import Device, SensorData

def init_db():
    """Initialize the database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample data if tables are empty
        if User.query.count() == 0:
            # Add sample users
            users = [
                User(name="Admin", email="admin@aiottank.com"),
                User(name="Tank Operator", email="operator@aiottank.com")
            ]
            for user in users:
                db.session.add(user)
        
        if Device.query.count() == 0:
            # Add sample devices
            devices = [
                Device(
                    name="Temperature Sensor",
                    device_type="sensor",
                    topic="aiot/tank/temperature",
                    status="online"
                ),
                Device(
                    name="Water Level Sensor",
                    device_type="sensor", 
                    topic="aiot/tank/water_level",
                    status="online"
                ),
                Device(
                    name="Motor Controller",
                    device_type="actuator",
                    topic="aiot/tank/motor",
                    status="offline"
                ),
                Device(
                    name="Main Controller",
                    device_type="controller",
                    topic="aiot/tank/controller",
                    status="online"
                )
            ]
            for device in devices:
                db.session.add(device)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
