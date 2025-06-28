from typing import Union
import json
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import paho.mqtt.client as mqtt
import threading
import time

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change to your MQTT broker address
MQTT_PORT = 1883
MQTT_CMD_TOPIC = "esp32/cmd"
MQTT_STATUS_TOPIC = "esp32/status"

# Global variables
mqtt_client = None
latest_status = {}

class Command(BaseModel):
    command: str

# MQTT Client Setup
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_STATUS_TOPIC)

def on_message(client, userdata, msg):
    global latest_status
    try:
        message = msg.payload.decode()
        latest_status = json.loads(message)
        print(f"Received status: {latest_status}")
    except Exception as e:
        print(f"Error processing message: {e}")

def setup_mqtt():
    global mqtt_client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        return True
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_mqtt()
    yield
    # Shutdown
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "AIoT Tank Controller"}

@app.post("/send-command")
def send_command(command: Command):
    """Send command to ESP32 via MQTT"""
    if not mqtt_client:
        raise HTTPException(status_code=500, detail="MQTT client not connected")
    
    try:
        message = json.dumps({"command": command.command})
        result = mqtt_client.publish(MQTT_CMD_TOPIC, message)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            return {"status": "success", "message": f"Command '{command.command}' sent to ESP32"}
        else:
            raise HTTPException(status_code=500, detail="Failed to publish message")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending command: {str(e)}")

@app.post("/feed")
def feed_command():
    """Send feed command to ESP32"""
    if not mqtt_client:
        raise HTTPException(status_code=500, detail="MQTT client not connected")
    
    try:
        message = json.dumps({"command": "feed"})
        result = mqtt_client.publish(MQTT_CMD_TOPIC, message)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            return {"status": "success", "message": "Feed command sent to ESP32"}
        else:
            raise HTTPException(status_code=500, detail="Failed to publish message")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending feed command: {str(e)}")

@app.get("/status")
def get_esp32_status():
    """Get latest ESP32 status"""
    if not latest_status:
        return {"status": "no_data", "message": "No status received from ESP32 yet"}
    
    return {"status": "success", "data": latest_status}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}