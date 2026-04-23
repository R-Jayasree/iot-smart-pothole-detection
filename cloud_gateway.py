"""
SMART ROAD POTHOLE DETECTION - MUNICIPAL ANALYTICS GATEWAY
Layer 3: Cloud / Edge Processing (Refined v2.1)
Features: Realistic Budgeting, Zonal Resolution, Map Analytics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time
import random

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
AREAS = ["Adyar", "T-Nagar", "Velachery", "Mylapore", "Guindy", "Anna Nagar", "Besant Nagar", "Tambaram"]
LAT_RANGE = (12.9200, 13.1000)
LON_RANGE = (80.2000, 80.2800)

# Refined Cost Mapping (More realistic for a simulation unit)
COST_MAP = {"Critical": 1200, "High": 800, "Medium": 400}

# --- DATA STORE ---
pothole_logs = []

def generate_mock_incident(is_historical=False):
    area = random.choice(AREAS)
    sev = random.choice(["Critical", "High", "Medium"])
    status = random.choice(["Pending", "In Progress", "Fixed"]) if is_historical else "Pending"
    depth = random.randint(5, 50)
    
    return {
        "id": int(time.time() * 1000) + random.randint(0, 1000),
        "latitude": round(random.uniform(*LAT_RANGE), 6),
        "longitude": round(random.uniform(*LON_RANGE), 6),
        "area": area,
        "depth": depth,
        "vibration": random.randint(100, 900),
        "severity": sev,
        "status": status,
        "cost_est": COST_MAP[sev],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "source": "IOT_SENSOR" if random.random() > 0.3 else "CITIZEN_APP"
    }

# Initial Population
for _ in range(20):
    pothole_logs.append(generate_mock_incident(is_historical=True))

# --- BACKGROUND GENERATOR ---
def background_pothole_generator():
    while True:
        time.sleep(9) 
        pothole_logs.insert(0, generate_mock_incident())
        if len(pothole_logs) > 100: pothole_logs.pop()
        print(f"INFO: Detection synced for {pothole_logs[0]['area']}")

threading.Thread(target=background_pothole_generator, daemon=True).start()

# --- API ENDPOINTS ---

@app.route('/', methods=['GET'])
def home():
    return "<h1>Smart Road Cloud Gateway <span style='color:blue'>Running</span></h1>"

@app.route('/api/potholes', methods=['GET'])
def get_potholes():
    return jsonify(pothole_logs)

@app.route('/api/pothole-report', methods=['POST'])
def iot_pothole_report():
    data = request.json
    if data.get('alert') in [True, "true"]:
        sev = "High" if data.get('vib', 0) > 400 else "Medium"
        report = {
            "id": int(time.time() * 1000),
            "latitude": data.get('lat'),
            "longitude": data.get('lon'),
            "area": "Detected Zone",
            "depth": data.get('dist', 0),
            "vibration": data.get('vib', 0),
            "severity": sev,
            "status": "Pending",
            "cost_est": COST_MAP[sev],
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "source": "IOT_SENSOR"
        }
        pothole_logs.insert(0, report)
    return jsonify({"status": "Success"}), 200

@app.route('/api/report-manual', methods=['POST'])
def manual_pothole_report():
    data = request.json
    sev = data.get('severity', 'Medium')
    report = {
        "id": int(time.time() * 1000),
        "latitude": data.get('lat', 13.0827),
        "longitude": data.get('lon', 80.2707),
        "area": data.get('area', 'Manual Entry'),
        "depth": data.get('depth', 0),
        "vibration": 0,
        "severity": sev,
        "status": "Pending",
        "cost_est": COST_MAP[sev],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "source": "CITIZEN_APP"
    }
    pothole_logs.insert(0, report)
    return jsonify({"status": "Success"}), 200

@app.route('/api/update-status', methods=['POST'])
def update_pothole_status():
    data = request.json
    p_id, n_status = data.get('id'), data.get('status')
    for log in pothole_logs:
        if log['id'] == p_id:
            log['status'] = n_status
            return jsonify({"status": "Updated"}), 200
    return jsonify({"error": "Null"}), 404

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    area_stats = {area: {"total": 0, "fixed": 0, "crit": 0, "cost": 0} for area in AREAS}
    sev_counts = {"Critical": 0, "High": 0, "Medium": 0}
    active_budget_est = 0
    total_fixed_count = 0

    for log in pothole_logs:
        area = log.get('area')
        if area in area_stats:
            area_stats[area]["total"] += 1
            if log['status'] == 'Fixed':
                area_stats[area]["fixed"] += 1
                total_fixed_count += 1
            else:
                # ONLY Pending/In Progress count towards active budget
                area_stats[area]["cost"] += log['cost_est']
                active_budget_est += log['cost_est']
                
            if log['severity'] == 'Critical':
                area_stats[area]["crit"] += 1
        
        sev = log['severity']
        if sev in sev_counts: sev_counts[sev] += 1

    return jsonify({
        "total_incidents": len(pothole_logs),
        "total_fixed": total_fixed_count,
        "budget_required": active_budget_est,
        "area_breakdown": area_stats,
        "severity_breakdown": sev_counts,
        "efficiency_rate": round((total_fixed_count / max(len(pothole_logs), 1)) * 100, 1)
    })

if __name__ == '__main__':
    print("MUNICIPAL CLOUD v2.1 (Refined Budget) - port 5000")
    app.run(port=5000, debug=False)
