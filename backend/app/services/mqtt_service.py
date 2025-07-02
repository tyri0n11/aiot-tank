import paho.mqtt.client as mqtt
import json
import threading
from flask import current_app

class MQTTService:
    _client = None
    _connected = False
    _lock = threading.Lock()
    
    @classmethod
    def initialize(cls, app=None):
        """Initialize MQTT client with Flask app context"""
        if app:
            with app.app_context():
                cls._client = mqtt.Client()
                cls._client.username_pw_set(
                    current_app.config.get('MQTT_USERNAME'),
                    current_app.config.get('MQTT_PASSWORD')
                )
                cls._client.on_connect = cls._on_connect
                cls._client.on_disconnect = cls._on_disconnect
                cls._client.on_message = cls._on_message
                
                try:
                    cls._client.connect(
                        current_app.config.get('MQTT_BROKER_HOST'),
                        current_app.config.get('MQTT_BROKER_PORT'),
                        60
                    )
                    cls._client.loop_start()
                except Exception as e:
                    print(f"Failed to connect to MQTT broker: {e}")
    
    @classmethod
    def _on_connect(cls, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server"""
        if rc == 0:
            cls._connected = True
            print("Connected to MQTT broker")
        else:
            print(f"Failed to connect to MQTT broker with code {rc}")
    
    @classmethod
    def _on_disconnect(cls, client, userdata, rc):
        """Callback for when the client disconnects from the server"""
        cls._connected = False
        print("Disconnected from MQTT broker")
    
    @classmethod
    def _on_message(cls, client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server"""
        topic = msg.topic
        message = msg.payload.decode('utf-8')
        print(f"Received message on topic '{topic}': {message}")
        # Here you can add logic to handle received messages
    
    @classmethod
    def publish_message(cls, topic, message):
        """Publish a message to a topic"""
        if not cls._client or not cls._connected:
            raise Exception("MQTT client not connected")
        
        if isinstance(message, dict):
            message = json.dumps(message)
        
        with cls._lock:
            result = cls._client.publish(topic, message)
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise Exception(f"Failed to publish message: {result.rc}")
    
    @classmethod
    def subscribe_to_topic(cls, topic):
        """Subscribe to a topic"""
        if not cls._client or not cls._connected:
            raise Exception("MQTT client not connected")
        
        with cls._lock:
            result = cls._client.subscribe(topic)
            if result[0] != mqtt.MQTT_ERR_SUCCESS:
                raise Exception(f"Failed to subscribe to topic: {result[0]}")
    
    @classmethod
    def get_connection_status(cls):
        """Get MQTT connection status"""
        return {
            'connected': cls._connected,
            'client_initialized': cls._client is not None
        }
