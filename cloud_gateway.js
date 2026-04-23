/**
 * CLOUD / EDGE PROCESSING LAYER (Simulation)
 * This script mimics a cloud server receiving data from IoT devices.
 */

const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Simulated database to store pothole locations
let potholeLogs = [];

// Endpoint for IoT devices to "upload" data (Communication Layer Interface)
app.post('/api/pothole-report', (req, res) => {
    const data = req.body;
    console.log("☁️ Cloud Received Data:", data);

    // Logic: Only store if it's a confirmed pothole
    if (data.alert === true || data.alert === "true") {
        const report = {
            id: Date.now(),
            latitude: data.lat,
            longitude: data.lon,
            severity: data.vib > 300 ? "High" : "Medium",
            timestamp: new Date().toLocaleTimeString()
        };
        potholeLogs.unshift(report); // Add to top
        if (potholeLogs.length > 20) potholeLogs.pop(); // Keep last 20
    }

    res.status(200).send({ status: "Data Processed" });
});

// Endpoint for the Visualization Dashboard
app.get('/api/potholes', (req, res) => {
    res.json(potholeLogs);
});

app.listen(PORT, () => {
    console.log(`🚀 Cloud Gateway running at http://localhost:${PORT}`);
    console.log(`📡 Ready to receive data from Pothole Detection System...`);
});
