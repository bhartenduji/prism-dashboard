# 🚗 Smart Parking IoT Dashboard System

An advanced real-time **IoT-based Smart Parking Management System** built using **Flask**, **Arduino UNO R4 WiFi**, and modern web technologies. This project provides intelligent parking slot monitoring, live occupancy tracking, analytics, forecasting, and a futuristic dashboard experience for smart campuses, malls, and smart city infrastructures.

---

## 📌 Project Overview

The **Smart Parking IoT Dashboard** is designed to solve one of the biggest urban problems — inefficient parking management.

The system uses IoT sensors connected to Arduino nodes to detect vehicle presence in parking slots and sends the data to a Flask-powered backend. The dashboard visualizes the parking status in real time and provides analytics and forecasting for better parking optimization.

This project demonstrates:

* Real-time IoT communication
* Smart sensor monitoring
* Live dashboard visualization
* Predictive occupancy analysis
* Server-Sent Events (SSE)
* Full-stack IoT integration
* Smart parking automation concepts

---

# ✨ Features

## 🔴 Real-Time Parking Monitoring

* Live slot occupancy detection
* Instant updates from sensors
* Dynamic online/offline sensor tracking
* Automatic slot status refresh

## 📡 IoT Sensor Integration

* Compatible with Arduino UNO R4 WiFi
* Distance-based vehicle detection
* Sensor node mapping for multiple parking lots
* Scalable architecture for additional sensors

## 📊 Analytics Dashboard

* Occupancy trends visualization
* Historical parking data analysis
* Peak hour monitoring
* Slot-wise activity tracking

## 🧠 AI-Based Forecasting

The system predicts future parking availability based on occupancy duration:

* 15-minute prediction
* 30-minute prediction
* 1-hour prediction

Forecast states include:

* Available
* Occupied
* Likely Available
* Probable Occupancy

## ⚡ Live Communication

* Uses **Server-Sent Events (SSE)** for real-time frontend updates
* Minimal latency updates
* Efficient event streaming architecture

## 🔐 Authentication System

* Secure login-based access
* JSON-based authentication flow
* Identity verification system

## 🌐 Modern Web Interface

* Responsive dashboard
* Live slot cards
* Real-time status indicators
* Smart UI visualization

---

# 🛠️ Tech Stack

## Backend

* Python
* Flask
* Flask-CORS

## Frontend

* HTML5
* CSS3
* JavaScript

## IoT Hardware

* Arduino UNO R4 WiFi
* Ultrasonic Distance Sensors
* WiFi Communication Modules

## Communication

* REST APIs
* JSON
* Server-Sent Events (SSE)

---

# 🏗️ System Architecture

```text
┌────────────────────┐
│ Ultrasonic Sensors │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Arduino UNO R4     │
│ WiFi Nodes          │
└─────────┬──────────┘
          │ HTTP Requests
          ▼
┌────────────────────┐
│ Flask Backend      │
│ API + SSE Server   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Web Dashboard      │
│ Real-Time Analytics│
└────────────────────┘
```

---

# 📂 Project Structure

```bash
Dashboard IOT/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Flask Server

```bash
python app.py
```

Server will start at:

```text
http://127.0.0.1:5000
```

---

# 📡 API Endpoints

## 🔹 Login Endpoint

```http
POST /login
```

### Request Body

```json
{
  "id": "STUDENT-GLA",
  "code": "1234"
}
```

---

## 🔹 Update Parking Slot

```http
POST /update-slot
```

### Request Body

```json
{
  "slot_id": "SLOT-1",
  "distance": 18.5
}
```

---

# 🧠 Occupancy Prediction Logic

The prediction engine estimates parking availability based on occupancy duration.

### Logic Used

| Occupancy Time    | Prediction       |
| ----------------- | ---------------- |
| Less than 20 mins | Occupied         |
| 20–40 mins        | Likely Available |
| More than 40 mins | Available Soon   |

---

# 📈 Dashboard Analytics

The dashboard maintains:

* Total occupied slots
* Slot history
* Sensor health
* Live occupancy graph
* Busy hour analysis
* Parking trends

---

# 🔥 Real-World Applications

## 🏫 Smart Campus Parking

Manage university parking efficiently.

## 🏢 Corporate Buildings

Reduce parking congestion in office spaces.

## 🛍️ Shopping Malls

Improve customer parking experience.

## 🌆 Smart Cities

Enable scalable intelligent parking infrastructure.

## 🏥 Hospitals

Optimize emergency and visitor parking.

---

# 🚀 Future Enhancements

* Mobile Application Integration
* License Plate Recognition
* AI-Based Traffic Prediction
* Google Maps Parking Navigation
* Cloud Database Integration
* QR-Based Parking Access
* RFID Vehicle Authentication
* Payment Gateway Integration
* Machine Learning Occupancy Models
* ThingWorx / AWS IoT Integration

---

# 🧪 Testing Scenarios

* Vehicle detection testing
* Sensor offline handling
* Real-time event synchronization
* Multi-slot occupancy simulation
* Forecast validation testing

---

# 🔒 Security Considerations

* Secure API communication
* Input validation
* Authentication-based dashboard access
* IoT node verification

---

# 📸 Screenshots

> <img width="1917" height="923" alt="image" src="https://github.com/user-attachments/assets/f6d44e5b-d4de-47ac-a737-29fbcef8e2b7" />

<img width="1902" height="917" alt="image" src="https://github.com/user-attachments/assets/5193f364-111d-4a21-a833-fc7a5e9dde03" />

<img width="1917" height="932" alt="image" src="https://github.com/user-attachments/assets/b2681fff-fe8c-47d8-81a1-16e319c9ce87" />

<img width="1912" height="917" alt="image" src="https://github.com/user-attachments/assets/04daaa26-0a16-4807-8f32-001d6106ffe6" />


# 👨‍💻 Developed By

## Bhartendu Ji

B.Tech CSE (AI-ML)
GLA University

### Skills

* Python
* Flask
* IoT Development
* AI & ML
* Full Stack Development
* Data Science

---

# ⭐ Why This Project Stands Out

This project combines:

* IoT Hardware Integration
* Real-Time Systems
* Smart Dashboard Engineering
* Predictive Analytics
* Web Development
* Event Streaming Architecture

It demonstrates strong practical implementation skills in:

* Embedded Systems
* Full Stack Development
* Smart Automation
* Real-Time Communication
* Data Visualization

---

# 📜 License

This project is licensed under the MIT License.

---

# 🤝 Contributions

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 🌟 Support

If you found this project useful:

⭐ Star the repository
🍴 Fork the project
📢 Share with others

---

# 💡 Quote

> “Smart systems are not built by technology alone, but by combining intelligence, automation, and vision.”

---

# 💡 Link ---  https://prism-dashboard-olive.vercel.app/
