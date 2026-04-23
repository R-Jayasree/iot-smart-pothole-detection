/* 
 * Smart Road Pothole Detection System - ESP32 IoT Version
 * Version 3.0: Professional Communication Layer (HTTP POST)
 */

#include <WiFi.h>
#include <HTTPClient.h>

// --- WiFi CONFIGURATION ---
const char* ssid = "Wokwi-GUEST"; 
const char* password = "";

// --- CLOUD CONFIGURATION ---
// Replace with your PC's IP address if running on actual hardware
const char* serverUrl = "http://localhost:5000/api/pothole-report";

// --- PIN CONFIGURATION ---
const int pingPin = 7;
const int ledPin = 6;
const int buzzerPin = 8;
const int vibrationPin = A0;

// Simulated GPS Data
float currentLat = 13.0827; 
float currentLon = 80.2707;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void loop() {
  // 1. SENSING LAYER
  long duration;
  int distance;
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW); delayMicroseconds(2);
  digitalWrite(pingPin, HIGH); delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);
  distance = duration * 0.034 / 2;

  int vibrationValue = analogRead(vibrationPin);
  bool potholeDetected = (distance > 20 || vibrationValue > 150);

  // 2. ACTUATION
  digitalWrite(ledPin, potholeDetected ? HIGH : LOW);
  digitalWrite(buzzerPin, potholeDetected ? HIGH : LOW);

  // 3. COMMUNICATION LAYER (HTTP POST)
  // This is the direct link to the Cloud Layer
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Prepare JSON Payload
    String jsonPayload = "{";
    jsonPayload += "\"lat\":" + String(currentLat, 6) + ",";
    jsonPayload += "\"lon\":" + String(currentLon, 6) + ",";
    jsonPayload += "\"dist\":" + String(distance) + ",";
    jsonPayload += "\"vib\":" + String(vibrationValue) + ",";
    jsonPayload += "\"alert\":" + String(potholeDetected ? "true" : "false");
    jsonPayload += "}";

    Serial.print("Sending Data to Cloud: ");
    Serial.println(jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }

  // Simulate movement
  currentLat += (random(-50, 50) / 100000.0);
  currentLon += (random(-50, 50) / 100000.0);

  delay(10000); // Send data every 10 seconds as requested
}
