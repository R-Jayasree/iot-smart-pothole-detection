# IoT-Based Smart Road Pothole Detection and Monitoring System

## Overview

This project presents an IoT-based system for detecting road potholes using sensor data and providing real-time monitoring through a cloud-enabled dashboard. The system combines embedded hardware, communication protocols, and web technologies to automate pothole detection and assist in infrastructure maintenance.

Traditional road inspection methods rely on manual surveys, which are inefficient and time-consuming. This system enables automated detection, classification, and visualization of pothole data.

---

## Features

* Real-time pothole detection using sensor inputs
* Severity classification (Low, Medium, High)
* Cloud-based data processing and storage
* REST API for data communication
* Interactive web dashboard with analytics and visualization
* Simulated GPS-based geospatial mapping
* Support for both IoT sensor data and manual reporting

---

## System Architecture

The system follows a layered IoT architecture:

1. **Sensing Layer**

   * Ultrasonic sensor (HC-SR04) for distance measurement
   * Vibration sensor for detecting road impact
   * Arduino / ESP32 for data acquisition

2. **Communication Layer**

   * Serial communication (simulation)
   * JSON-based data formatting

3. **Cloud Processing Layer**

   * Flask-based backend server
   * REST APIs for data ingestion and retrieval
   * Data storage and analytics

4. **Application Layer**

   * Web dashboard (HTML, CSS, JavaScript)
   * Map-based visualization (Leaflet)
   * Incident monitoring and reporting

---

## Tech Stack

### Hardware

* Arduino Uno / ESP32
* Ultrasonic Sensor (HC-SR04)
* Vibration Sensor
* LED, Buzzer

### Software

* Arduino IDE (Embedded programming)
* Python (Flask backend)
* HTML, CSS, JavaScript (Dashboard)
* REST APIs
* JSON

---

## Repository Structure

```
.
├── pothole_detection.ino          # Arduino code
├── pothole_detection_esp32.ino    # ESP32 version
├── cloud_gateway.py               # Flask backend server
├── cloud_gateway.js               # Alternative gateway (Node.js)
├── dashboard.html                # Web dashboard
├── report.pdf                    # Project report file
└── README.md
```

---

## How It Works

1. Sensors collect road condition data (distance + vibration)
2. Arduino/ESP32 processes the readings
3. Potholes are detected based on threshold values
4. Severity is classified (Low / Medium / High)
5. Data is formatted as JSON and transmitted
6. Flask server receives and processes the data
7. Dashboard visualizes incidents and analytics

---

## Setup Instructions

### 1. Hardware Setup

* Connect ultrasonic sensor, vibration sensor, LED, and buzzer to Arduino/ESP32
* Upload the `.ino` file using Arduino IDE

### 2. Backend Setup

```bash
pip install flask flask-cors
python cloud_gateway.py
```

### 3. Run Dashboard

* Open `dashboard.html` in a browser
* Ensure backend server is running

---

## Sample Data Format

```json
{
  "lat": 13.0827,
  "lon": 80.2707,
  "dist": 35,
  "vib": 420,
  "pothole": true,
  "severity": "HIGH"
}
```

---

## Applications

* Smart city infrastructure monitoring
* Road safety improvement
* Municipal maintenance planning
* Real-time incident tracking

---

## Future Enhancements

* Integration with real GPS modules
* Wireless communication using ESP32 / WiFi
* Mobile application for citizen reporting
* Machine learning-based road condition analysis
* Large-scale deployment across multiple nodes

---

## Contributors

* Jayasree R
* M K Kavya

---

## License

This project is developed for academic and research purposes.
