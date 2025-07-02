from app.extensions import db

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)  # 'sensor', 'actuator', 'controller'
    topic = db.Column(db.String(200), nullable=False)  # MQTT topic
    status = db.Column(db.String(20), default='offline')  # 'online', 'offline', 'error'
    last_seen = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'device_type': self.device_type,
            'topic': self.topic,
            'status': self.status,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Device {self.name} ({self.device_type})>'

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # 'temperature', 'humidity', 'distance', etc.
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    device = db.relationship('Device', backref=db.backref('sensor_data', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'sensor_type': self.sensor_type,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __repr__(self):
        return f'<SensorData {self.sensor_type}: {self.value}{self.unit or ""}>'
