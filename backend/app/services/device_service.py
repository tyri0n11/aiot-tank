from app.models.device import Device, SensorData
from app.extensions import db
from datetime import datetime

class DeviceService:
    @staticmethod
    def get_all_devices():
        """Get all devices"""
        devices = Device.query.all()
        return [device.to_dict() for device in devices]
    
    @staticmethod
    def get_device_by_id(device_id):
        """Get device by ID"""
        device = Device.query.get(device_id)
        return device.to_dict() if device else None
    
    @staticmethod
    def create_device(data):
        """Create new device"""
        device = Device(
            name=data['name'],
            device_type=data['device_type'],
            topic=data['topic'],
            status=data.get('status', 'offline')
        )
        db.session.add(device)
        db.session.commit()
        return device.to_dict()
    
    @staticmethod
    def update_device_status(device_id, status):
        """Update device status"""
        device = Device.query.get(device_id)
        if not device:
            return None
        
        device.status = status
        device.last_seen = datetime.utcnow()
        db.session.commit()
        return device.to_dict()
    
    @staticmethod
    def delete_device(device_id):
        """Delete device"""
        device = Device.query.get(device_id)
        if not device:
            return False
        
        db.session.delete(device)
        db.session.commit()
        return True
    
    @staticmethod
    def add_sensor_data(device_id, sensor_type, value, unit=None):
        """Add sensor data"""
        sensor_data = SensorData(
            device_id=device_id,
            sensor_type=sensor_type,
            value=value,
            unit=unit
        )
        db.session.add(sensor_data)
        db.session.commit()
        return sensor_data.to_dict()
    
    @staticmethod
    def get_sensor_data(device_id, sensor_type=None, limit=100):
        """Get sensor data for a device"""
        query = SensorData.query.filter_by(device_id=device_id)
        
        if sensor_type:
            query = query.filter_by(sensor_type=sensor_type)
        
        data = query.order_by(SensorData.timestamp.desc()).limit(limit).all()
        return [item.to_dict() for item in data]
