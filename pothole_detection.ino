/* 
 * Smart Road Pothole Detection System
 * Version: 2.0 (Simulated IoT Ready)
 */

const int pingPin = 7;
const int ledPin = 6;
const int buzzerPin = 8;
const int vibrationPin = A0;

// Variables for sensors
long duration;
int distance;
int vibrationValue;

// Simulated GPS coordinates (e.g., Bangalore area)
float currentLat = 12.9716;
float currentLon = 77.5946;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
  
  // Seed random for GPS simulation
  randomSeed(analogRead(A1)); 
}

void loop() {
  // 1. DATA ACQUISITION
  
  // Trigger ultrasonic sensor
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);

  // Read echo
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);
  distance = duration * 0.034 / 2;

  // Read vibration sensor
  vibrationValue = analogRead(vibrationPin);

  // 2. SIMULATED GPS LOGIC
  // We simulate slight movement in coordinates
  currentLat += (random(-100, 100) / 100000.0);
  currentLon += (random(-100, 100) / 100000.0);

  // 3. DETECTION LOGIC
  bool potholeDetected = (distance > 20 || vibrationValue > 100);

  if (potholeDetected) {
    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);
  }

  // 4. COMMUNICATION LAYER: JSON FORMAT OUTPUT
  // This format is what the cloud dashboard will use to track the pothole
  Serial.print("{");
  Serial.print("\"lat\":"); Serial.print(currentLat, 6);
  Serial.print(", \"lon\":"); Serial.print(currentLon, 6);
  Serial.print(", \"dist\":"); Serial.print(distance);
  Serial.print(", \"vib\":"); Serial.print(vibrationValue);
  Serial.print(", \"pothole\":"); Serial.print(potholeDetected ? "true" : "false");
  Serial.println("}");

  delay(1000); // 1 second update rate for simulation
}
