#include <ESP32Servo.h>

const int servoPin = 13; // Change to your connected pin
Servo myServo;

void setup() {
    Serial.begin(115200);
    myServo.attach(servoPin);
    Serial.println("Servo test start");
}

void loop() {
    // Sweep from 0 to 180 degrees
    for (int pos = 0; pos <= 180; pos += 10) {
        myServo.write(pos);
        Serial.print("Position: ");
        Serial.println(pos);
        delay(500);
    }
    // Sweep back from 180 to 0 degrees
    for (int pos = 180; pos >= 0; pos -= 10) {
        myServo.write(pos);
        Serial.print("Position: ");
        Serial.println(pos);
        delay(500);
    }
}