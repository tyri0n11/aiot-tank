from flask import Blueprint, jsonify, request
from app.services.mqtt_service import MQTTService

mqtt_bp = Blueprint('mqtt', __name__, url_prefix='/api/mqtt')

@mqtt_bp.route('/publish', methods=['POST'])
def publish_message():
    """Publish message to MQTT topic"""
    data = request.get_json()
    if not data or 'topic' not in data or 'message' not in data:
        return jsonify({'error': 'Topic and message are required'}), 400
    
    try:
        MQTTService.publish_message(data['topic'], data['message'])
        return jsonify({'status': 'success', 'message': 'Message published successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mqtt_bp.route('/subscribe/<topic>', methods=['POST'])
def subscribe_to_topic(topic):
    """Subscribe to MQTT topic"""
    try:
        MQTTService.subscribe_to_topic(topic)
        return jsonify({'status': 'success', 'message': f'Subscribed to {topic}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mqtt_bp.route('/status', methods=['GET'])
def mqtt_status():
    """Get MQTT connection status"""
    status = MQTTService.get_connection_status()
    return jsonify(status)
