from flask import Flask, render_template, request, Response, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage for slot data
parking_slots = {f"SLOT-{i}": {
    "id": f"SLOT-{i}",
    "sensor": f"ARDUINO-R4-NODE-0{1 if i<=4 else (2 if i<=8 else 3)}",
    "lot": 'A' if i<=6 else 'B',
    "occupied": False,
    "distance": 0.0,
    "last_updated": "Offline",
    "online": False,
    "occupied_since": None
} for i in range(1, 13)}

def calculate_slot_forecast(slot_id):
    slot = parking_slots[slot_id]
    if not slot['occupied']:
        return {"15m": "Available", "30m": "Available", "1h": "Available"}
    
    # Calculate probability based on time spent
    if not slot['occupied_since']:
        return {"15m": "Occupied", "30m": "Occupied", "1h": "Probable"}
    
    elapsed = (datetime.now() - slot['occupied_since']).total_seconds() / 60
    # Average stay is 45 mins
    if elapsed > 40: return {"15m": "Likely", "30m": "Available", "1h": "Available"}
    if elapsed > 20: return {"15m": "Occupied", "30m": "Likely", "1h": "Available"}
    return {"15m": "Occupied", "30m": "Occupied", "1h": "Probable"}

# Historical data for analytics (Simulated & Live)
# Stores snapshots: {"time": "HH:MM", "occupied": count}
occupancy_history = []
slot_history = {f"SLOT-{i}": [] for i in range(1, 13)}

# Pre-populate with simulated data for "Busy Hours" display
for h in range(8, 22): # 8 AM to 9 PM
    for m in [0, 30]:
        time_str = f"{h:02d}:{m:02d}"
        # Simulate a curve: peak at 12-2 PM
        peak_factor = 1.0 - (abs(h - 13) / 8)
        count = int(12 * peak_factor * (0.7 + (time.time() % 0.3)))
        occupancy_history.append({"time": time_str, "occupied": max(0, min(12, count))})
        
        # Populate per-slot history with some random occupancy
        for i in range(1, 13):
            sid = f"SLOT-{i}"
            slot_history[sid].append({"time": time_str, "occupied": (time.time() + i) % 3 > 1})

# Queue for Server-Sent Events (SSE)
subscribers = []
active_sensors = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Simple demo auth
    if data.get('id') == 'STUDENT-GLA' and data.get('code') == '1234':
        return jsonify({"status": "success", "user": "STUDENT"}), 200
    return jsonify({"status": "error", "message": "Identity Denied"}), 401

@app.route('/update-slot', methods=['POST'])
def update_slot():
    data = request.json
    slot_id = data.get('slot_id')
    distance = float(data.get('distance'))
    
    if slot_id in parking_slots:
        now_dt = datetime.now()
        was_occupied = parking_slots[slot_id]['occupied']
        occupied = distance < 25.0
        active_sensors.add(slot_id)
        
        # Track occupancy duration
        if occupied and not was_occupied:
            parking_slots[slot_id]['occupied_since'] = now_dt
        elif not occupied:
            parking_slots[slot_id]['occupied_since'] = None

        parking_slots[slot_id].update({
            "occupied": occupied,
            "distance": distance,
            "last_updated": now_dt.strftime("%H:%M:%S"),
            "online": True
        })
        
        # Update live history
        now_str = now_dt.strftime("%H:%M")
        total_occupied = sum(1 for s in parking_slots.values() if s['occupied'])
        occupancy_history.append({"time": now_str, "occupied": total_occupied})
        if len(occupancy_history) > 100: occupancy_history.pop(0)
        
        # Update per-slot history
        slot_history[slot_id].append({"time": now_str, "occupied": occupied})
        if len(slot_history[slot_id]) > 50: slot_history[slot_id].pop(0)

        # Payload includes AI predictions
        update_data = parking_slots[slot_id].copy()
        # Convert datetime to string for JSON serialization
        if update_data['occupied_since']:
            update_data['occupied_since'] = update_data['occupied_since'].isoformat()
            
        update_data['online_count'] = len(active_sensors)
        
        # Predictive Logic: Simple trend analysis
        next_val = "Clearing" if not occupied else "Busy"
        confidence = 88.5 if occupied else 92.1
        
        update_data['ai_prediction'] = {
            "next_hour": next_val,
            "confidence": confidence,
            "best_slot": "SLOT-5" if total_occupied > 8 else slot_id,
            "vacancy_eta": "15 mins" if occupied else "NOW",
            "forecast": calculate_slot_forecast(slot_id)
        }
        
        payload = json.dumps(update_data)
        for sub in subscribers:
            sub.put(payload)
            
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/api/analytics')
def get_analytics():
    # Return last 24 records for the chart and full slot forecast
    forecast_matrix = {sid: calculate_slot_forecast(sid) for sid in parking_slots}
    
    return jsonify({
        "history": occupancy_history[-24:],
        "predictions": [
            {"hour": "08:00", "prob": 20},
            {"hour": "10:00", "prob": 65},
            {"hour": "12:00", "prob": 90},
            {"hour": "14:00", "prob": 85},
            {"hour": "16:00", "prob": 40},
            {"hour": "18:00", "prob": 15}
        ],
        "slot_forecast": forecast_matrix
    })

@app.route('/api/slot-analytics/<slot_id>')
def get_slot_analytics(slot_id):
    if slot_id in slot_history:
        return jsonify({
            "id": slot_id,
            "history": slot_history[slot_id][-20:],
            "forecast": calculate_slot_forecast(slot_id),
            "info": parking_slots[slot_id]
        })
    return jsonify({"error": "Slot not found"}), 404



@app.route('/stream')
def stream():
    def event_stream():
        import queue
        q = queue.Queue()
        subscribers.append(q)
        try:
            # Send initial state with current online count
            state_slots = []
            for s in parking_slots.values():
                sd = s.copy()
                if sd.get('occupied_since') and hasattr(sd['occupied_since'], 'isoformat'):
                    sd['occupied_since'] = sd['occupied_since'].isoformat()
                state_slots.append(sd)
                
            initial_state = {
                "slots": state_slots,
                "online_count": len(active_sensors)
            }
            yield f"data: {json.dumps(initial_state)}\n\n"
            while True:
                data = q.get()
                yield f"data: {data}\n\n"
        except GeneratorExit:
            subscribers.remove(q)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" PRISM AI-ENHANCED BACKEND RUNNING")
    print(" Send POST to /update-slot to change data")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)

