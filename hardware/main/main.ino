#include <WiFi.h>
#include <WiFiClientSecure.h>  
#include <PubSubClient.h>
#include <ESP32Servo.h>
#include <ArduinoJson.h>
#include "config.h"

// WiFi and MQTT credentials
const char* ssid = SSID;
const char* password = WIFI_PASSWORD;
const char* mqtt_broker = MQTT_BROKER;
const char* topic = MQTT_TOPIC;
const char* command_topic = MQTT_TOPIC "/cmd";  // For receiving commands
const char* status_topic = MQTT_TOPIC "/status"; // For sending status
const char* mqtt_username = MQTT_USERNAME;
const char* mqtt_password = MQTT_PASSWORD;
const int mqtt_port = MQTT_PORT;

// Servo configuration - SG90
Servo feedServo;
const int servoPin = 13;
const int initialPosition = 0;
const int feedPosition = 180;
const int servoDelay = 400; // Optimized for SG90
const int holdDelay = 600;   // Reduced hold time

// Connection management
const unsigned long reconnectInterval = 5000; // 5 seconds
const unsigned long heartbeatInterval = 30000; // 30 seconds
const int maxReconnectAttempts = 3; // Max attempts before giving up temporarily
unsigned long lastReconnectAttempt = 0;
unsigned long lastHeartbeat = 0;
int reconnectAttempts = 0;
bool servoInOperation = false;
WiFiClientSecure espClient;
PubSubClient client(espClient);

// Function declarations
void setupWiFi();
void setupMQTT();
void initializeServo();
void performFeedCycle();
bool reconnectMQTT();
bool reconnectWiFi();
void sendHeartbeat();
void callback(char *topic, byte *payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    Serial.println("\n=== ESP32 IoT Tank Starting ===");
    
    initializeServo();
    setupWiFi();
    setupMQTT();
    
    Serial.println("=== Setup Complete ===\n");
}

void setupWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.printf("Connected to WiFi: %s\n", ssid);
        Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());
        Serial.printf("Signal strength: %d dBm\n", WiFi.RSSI());
        reconnectAttempts = 0; // Reset counter on successful connection
    } else {
        Serial.println("\nWiFi connection failed!");
        // Don't restart immediately, let the main loop handle reconnection
    }
}

bool reconnectWiFi() {
    if (WiFi.status() == WL_CONNECTED) {
        return true;
    }
    
    Serial.println("Attempting WiFi reconnection...");
    WiFi.disconnect();
    delay(100);
    WiFi.begin(ssid, password);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 10) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println(" WiFi reconnected!");
        reconnectAttempts = 0;
        return true;
    } else {
        Serial.println(" WiFi reconnection failed");
        return false;
    }
}

void setupMQTT() {
    espClient.setInsecure(); // For development - use proper certificates in production
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    client.setKeepAlive(60);
    client.setSocketTimeout(30);
    
    // Only attempt initial connection if WiFi is connected
    if (WiFi.status() == WL_CONNECTED) {
        reconnectMQTT();
    }
}

void initializeServo() {
    Serial.println("Initializing SG90 servo...");
    feedServo.attach(servoPin);
    delay(50);
    feedServo.write(initialPosition);
    delay(servoDelay);
    Serial.println("Servo initialized at initial position");
}

void callback(char *topic, byte *payload, unsigned int length) {
    // Prevent processing if servo is already in operation
    if (servoInOperation) {
        Serial.println("Servo busy, ignoring command");
        return;
    }
    
    // Limit message length to prevent buffer overflow
    if (length > 512) {
        Serial.println("Message too long, ignoring");
        return;
    }
    
    Serial.printf("Message received [%s]: ", topic);
    
    // Convert payload to string with null termination safety
    char buffer[513]; // +1 for null terminator
    memcpy(buffer, payload, length);
    buffer[length] = '\0';
    String message(buffer);
    
    Serial.println(message);
    
    // Parse JSON with error handling
    StaticJsonDocument<256> doc; // Use StaticJsonDocument for better stability
    DeserializationError error = deserializeJson(doc, message);
    
    if (error) {
        Serial.printf("JSON parsing failed: %s\n", error.c_str());
        return; // Don't send error response to avoid feedback loop
    }
    
    // Process commands only - ignore status messages completely
    if (doc.containsKey("command")) {
        const char* command = doc["command"];
        if (command && strcmp(command, "feed") == 0) {
            Serial.println("Feed command received!");
            performFeedCycle();
        } else {
            Serial.println("Unknown command received");
        }
    }
    // Silently ignore non-command messages to prevent feedback loops
}

void performFeedCycle() {
    servoInOperation = true;
    Serial.println("Starting feed cycle...");
    
    // Move to feed position
    feedServo.write(feedPosition);
    delay(servoDelay);
    
    // Hold position for feeding
    delay(holdDelay);
    
    // Return to initial position
    feedServo.write(initialPosition);
    delay(servoDelay);
    
    servoInOperation = false;
    Serial.println("Feed cycle completed!");
    
    // Send confirmation
    StaticJsonDocument<100> response;
    response["status"] = "feed_completed";
    response["servo"] = "SG90";
    response["timestamp"] = millis();
    
    String responseStr;
    serializeJson(response, responseStr);
    client.publish(status_topic, responseStr.c_str());
}

bool reconnectMQTT() {
    // Check WiFi first - don't attempt MQTT if WiFi is down
    if (WiFi.status() != WL_CONNECTED) {
        return false;
    }
    
    if (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        
        // Create unique client ID
        String clientId = "esp32-tank-";
        clientId += WiFi.macAddress();
        clientId.replace(":", "");
        
        if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) {
            Serial.println(" connected!");
            
            // Subscribe to command topic only
            client.subscribe(command_topic);
            Serial.printf("Subscribed to command topic: %s\n", command_topic);
            
            // Send online status to status topic
            StaticJsonDocument<100> status;
            status["status"] = "online";
            status["device"] = "esp32-tank";
            status["ip"] = WiFi.localIP().toString();
            
            String statusStr;
            serializeJson(status, statusStr);
            client.publish(status_topic, statusStr.c_str());
            
            reconnectAttempts = 0; // Reset counter on successful connection
            return true;
        } else {
            Serial.printf(" failed, rc=%d\n", client.state());
            return false;
        }
    }
    return true;
}

void sendHeartbeat() {
    if (client.connected()) {
        StaticJsonDocument<150> heartbeat;
        heartbeat["status"] = "heartbeat";
        heartbeat["uptime"] = millis();
        heartbeat["free_heap"] = ESP.getFreeHeap();
        heartbeat["rssi"] = WiFi.RSSI();
        
        String heartbeatStr;
        serializeJson(heartbeat, heartbeatStr);
        client.publish(status_topic, heartbeatStr.c_str());
    }
}

void loop() {
    unsigned long now = millis();
    
    // Handle WiFi connection first
    if (WiFi.status() != WL_CONNECTED) {
        if (now - lastReconnectAttempt > reconnectInterval) {
            lastReconnectAttempt = now;
            reconnectAttempts++;
            
            if (reconnectAttempts <= maxReconnectAttempts) {
                if (reconnectWiFi()) {
                    // WiFi reconnected, reset MQTT connection attempt
                    lastReconnectAttempt = 0;
                }
            } else {
                // Too many failed attempts, wait longer before trying again
                if (reconnectAttempts > maxReconnectAttempts + 5) {
                    Serial.println("Too many failed connection attempts, restarting...");
                    ESP.restart();
                }
                // Wait 30 seconds before next attempt
                if (now - lastReconnectAttempt > 30000) {
                    reconnectAttempts = 0;
                }
            }
        }
        return; // Don't proceed with MQTT if WiFi is down
    }
    
    // Handle MQTT connection
    if (!client.connected()) {
        if (now - lastReconnectAttempt > reconnectInterval) {
            lastReconnectAttempt = now;
            if (reconnectMQTT()) {
                lastReconnectAttempt = 0;
            }
        }
    } else {
        client.loop();
        
        // Send periodic heartbeat
        if (now - lastHeartbeat > heartbeatInterval) {
            lastHeartbeat = now;
            sendHeartbeat();
        }
    }
    
    // Small delay to prevent tight loop
    delay(10);
}
