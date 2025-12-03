# 🧠 SystemMonitor Pro AI  
 
## 📌 Overview
**SystemMonitor Pro AI** is an advanced desktop monitoring application designed for deep real-time system analytics.  
It merges classical hardware monitoring with adaptive machine-learning logic to detect anomalies, peaks, and unusual system behavior.

| <img width="1280" height="640" alt="system" src="https://github.com/user-attachments/assets/9333b761-5572-475a-bfd9-a3a951fee3cb" /> |
|---|
The application runs fully offline and is ideal for professional and security-sensitive environments.

---

## 🚀 Core Features

### 🔹 Real-Time Monitoring
- CPU utilization
- RAM usage
- Disk usage
- Network upload/download (kB/s)
- Top-10 processes with CPU/RAM/Threads
- Kill process directly from the UI

---

### 🔹 AI & Analytics
- Adaptive threshold engine (rolling statistical windows)
- Automatic anomaly detection (OK/WARN/ALERT)
- Z-Score analysis
- AI status states: LEARN, STABLE, OK, WARN, ALERT
- Predictive forecasting (CPU/RAM/Disk – up to 30 minutes)
- AI Heatmap (weekday × hour)
- AI Eventlog (warnings & alerts)

---

### 🔹 Export & Forensics
- Export event log as JSON
- 60-second profiling mode with complete data dump
- Fully local report generation

---

### 🔹 UI & Usability
- Bilingual interface (English & German)
- GitHub button
- Info panel (About this app)
- Dark Mode & BYLICKILABS Neon Mode
- Live graphs (60s historical chart per metric)
- Modern, clean UI via PySide6

---

### 🔹 System Integration
- Auto-start via Windows Registry
- 100% offline operation
- No cloud services required

---

# 🛠️ Installation

### 1️⃣ Set up environment
```bash
pip install -r requirements.txt
```

### 2️⃣ Start application
```bash
python main.py
```

---

# 📁 Project Structure

```
systemmonitor_pro/
├─ app.py
├─ config.py
├─ CONTRIBUTING.md
├─ monitoring.py
├─ README.md
├─ requirements.txt 
├─ SECURITY.md
├─ ui_components.py
└─ ui_main.py
```

---

# ⚙️ Technologies
- Python 3.11+
- PySide6
- psutil
- Local AI/statistical analysis (rolling windows)
- Windows Registry Integration

---

# © License & Rights
© 2025 Thorsten Bylicki – BYLICKILABS – Intelligence Systems & Communications.  
[LICENSE](LICENSE)
