from flask import Blueprint, jsonify, request
from app.services.device_service import DeviceService

device_bp = Blueprint('device', __name__, url_prefix='/api/devices')

@device_bp.route('/', methods=['GET'])
def get_devices():
    """Get all devices"""
    devices = DeviceService.get_all_devices()
    return jsonify(devices)

@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    """Get device by ID"""
    device = DeviceService.get_device_by_id(device_id)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    return jsonify(device)

@device_bp.route('/', methods=['POST'])
def create_device():
    """Create new device"""
    data = request.get_json()
    required_fields = ['name', 'device_type', 'topic']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Name, device_type, and topic are required'}), 400
    
    device = DeviceService.create_device(data)
    return jsonify(device), 201

@device_bp.route('/<int:device_id>/status', methods=['PUT'])
def update_device_status(device_id):
    """Update device status"""
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    device = DeviceService.update_device_status(device_id, data['status'])
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    return jsonify(device)

@device_bp.route('/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete device"""
    if DeviceService.delete_device(device_id):
        return jsonify({'message': 'Device deleted successfully'})
    return jsonify({'error': 'Device not found'}), 404

@device_bp.route('/<int:device_id>/sensor-data', methods=['POST'])
def add_sensor_data(device_id):
    """Add sensor data for a device"""
    data = request.get_json()
    required_fields = ['sensor_type', 'value']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'sensor_type and value are required'}), 400
    
    sensor_data = DeviceService.add_sensor_data(
        device_id,
        data['sensor_type'],
        data['value'],
        data.get('unit')
    )
    return jsonify(sensor_data), 201

@device_bp.route('/<int:device_id>/sensor-data', methods=['GET'])
def get_sensor_data(device_id):
    """Get sensor data for a device"""
    sensor_type = request.args.get('sensor_type')
    limit = int(request.args.get('limit', 100))
    
    data = DeviceService.get_sensor_data(device_id, sensor_type, limit)
    return jsonify(data)
