/* 
  PRISM 3 SENSOR FIRMWARE - ARDUINO UNO R4 WiFi
  Hardware: Arduino Uno R4 WiFi + 3 HC-SR04 Ultrasonic Sensors
*/

#include "WiFiS3.h"
#include <ArduinoJson.h>

// ---------- WIFI CONFIG ----------
const char* ssid = "TP-Link_7AE6";
const char* password = "36144044";

// Put your laptop/backend IPv4 address here
const char* serverAddress = "192.168.0.105";
const int serverPort = 5000;

// ---------- SENSOR CONFIG ----------
const int NUM_SENSORS = 3;

const char* slotIds[NUM_SENSORS] = {
  "SLOT-1",
  "SLOT-2",
  "SLOT-3"
};

const int trigPins[NUM_SENSORS] = {
  3,2,6
};

const int echoPins[NUM_SENSORS] = {
  5,4,7
};

// Distance threshold for occupied status
const float OCCUPIED_THRESHOLD_CM = 15.0;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(1000);

  for (int i = 0; i < NUM_SENSORS; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
    digitalWrite(trigPins[i], LOW);
  }

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi module not present");
    while (true);
  }

  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    delay(5000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Connected to WiFi!");
  printWifiStatus();
}

void loop() {
  Serial.println();
  Serial.println("Reading all 3 sensors...");
  Serial.println("-------------------------");

  for (int i = 0; i < NUM_SENSORS; i++) {
    float distanceCm = measureDistance(trigPins[i], echoPins[i]);
    String status = getSlotStatus(distanceCm);

    Serial.print(slotIds[i]);
    Serial.print(" | Distance: ");
    Serial.print(distanceCm, 1);
    Serial.print(" cm | Status: ");
    Serial.println(status);

    sendDistanceToServer(slotIds[i], distanceCm, status);

    // Small delay avoids ultrasonic cross-interference
    delay(100);
  }

  delay(2000);
}

float measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return -1.0;
  }

  float distanceCm = duration * 0.034 / 2.0;
  return distanceCm;
}

String getSlotStatus(float distanceCm) {
  if (distanceCm < 0) {
    return "ERROR";
  } 
  else if (distanceCm <= OCCUPIED_THRESHOLD_CM) {
    return "OCCUPIED";
  } 
  else {
    return "AVAILABLE";
  }
}

void sendDistanceToServer(const char* slotId, float distanceCm, String status) {
  Serial.print("Sending ");
  Serial.print(slotId);
  Serial.print(" to server... ");

  if (client.connect(serverAddress, serverPort)) {
    Serial.println("Connected!");

    StaticJsonDocument<250> doc;
    doc["slot_id"] = slotId;
    doc["distance"] = distanceCm;
    doc["status"] = status;

    String requestBody;
    serializeJson(doc, requestBody);

    client.println("POST /update-slot HTTP/1.1");
    client.print("Host: ");
    client.println(serverAddress);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(requestBody.length());
    client.println("Connection: close");
    client.println();
    client.println(requestBody);

    Serial.print("[");
    Serial.print(slotId);
    Serial.print("] Sent: ");
    Serial.print(distanceCm, 1);
    Serial.print(" cm | ");
    Serial.println(status);

    while (client.connected() || client.available()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
      }
    }

    client.stop();
    Serial.println();
    Serial.println("Connection closed");
  } 
  else {
    Serial.println("Connection failed");
  }
}

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("Arduino IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("Signal strength: ");
  Serial.print(rssi);
  Serial.println(" dBm");
}