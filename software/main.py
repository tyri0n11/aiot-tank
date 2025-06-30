from typing import Union
import json
import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import paho.mqtt.client as paho
from paho import mqtt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Global MQTT client variable
mqtt_client = None
latest_messages = {}

# Pydantic models for request/response
class CommandRequest(BaseModel):
    command: str
    parameters: dict = {}

class MQTTMessage(BaseModel):
    topic: str
    payload: str
    timestamp: str

# MQTT callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"MQTT connected with code {rc}")
    if rc == 0:
        # Subscribe to all ESP32 topics
        client.subscribe("esp32/#", qos=0)
        print("Subscribed to esp32/# topics")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message: {topic} - {payload}")
    
    # Store the latest message for each topic
    latest_messages[topic] = {
        "payload": payload,
        "timestamp": asyncio.get_event_loop().time()
    }

def on_publish(client, userdata, mid, properties=None):
    print(f"Message published with mid: {mid}")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed with mid: {mid}, QoS: {granted_qos}")

def setup_mqtt_client():
    """Initialize and configure MQTT client"""
    global mqtt_client
    
    # Create MQTT client
    mqtt_client = paho.Client(client_id="aiot-tank-server", userdata=None, protocol=paho.MQTTv5)
    
    # Set callbacks
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish
    mqtt_client.on_subscribe = on_subscribe
    
    # Enable TLS for secure connection
    mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    
    # Set username and password
    mqtt_client.username_pw_set(
        os.getenv("MQTT_USERNAME"), 
        os.getenv("MQTT_PASSWORD")
    )
    
    # Connect to MQTT broker
    broker = os.getenv("MQTT_BROKER")
    port = int(os.getenv("MQTT_PORT", 8883))
    
    try:
        mqtt_client.connect(broker, port, keepalive=60)
        mqtt_client.loop_start()
        print(f"MQTT client connected to {broker}:{port}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting MQTT client...")
    setup_mqtt_client()
    yield
    # Shutdown
    print("Shutting down MQTT client...")
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

app = FastAPI(lifespan=lifespan, title="AIoT Tank Server", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "message": "AIoT Tank Server", 
        "version": "1.0.0",
        "mqtt_connected": mqtt_client.is_connected() if mqtt_client else False
    }

@app.get("/status")
def get_status():
    """Get server and MQTT connection status"""
    return {
        "server": "running",
        "mqtt_connected": mqtt_client.is_connected() if mqtt_client else False,
        "latest_messages": latest_messages
    }

@app.post("/command")
def send_command(command_request: CommandRequest):
    """Send command to ESP32 via MQTT"""
    if not mqtt_client or not mqtt_client.is_connected():
        raise HTTPException(status_code=503, detail="MQTT client not connected")
    
    # Create command payload
    payload = {
        "command": command_request.command,
        "parameters": command_request.parameters
    }
    
    # Publish to ESP32 command topic
    topic = "esp32/cmd"
    message = json.dumps(payload)
    
    try:
        result = mqtt_client.publish(topic, payload=message, qos=0)
        if result.rc == paho.MQTT_ERR_SUCCESS:
            return {
                "status": "success",
                "topic": topic,
                "message": message,
                "mid": result.mid
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to publish message: {result.rc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing message: {str(e)}")

@app.get("/messages")
def get_latest_messages():
    """Get latest messages from all ESP32 topics"""
    return latest_messages

@app.get("/messages/{topic_path:path}")
def get_message_by_topic(topic_path: str):
    """Get latest message from specific topic"""
    full_topic = f"esp32/{topic_path}"
    if full_topic in latest_messages:
        return {
            "topic": full_topic,
            **latest_messages[full_topic]
        }
    else:
        raise HTTPException(status_code=404, detail=f"No messages found for topic: {full_topic}")

# Legacy endpoint for compatibility
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}