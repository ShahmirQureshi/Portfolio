
# 🔥 Real-Time Fire Detection and Intelligent Alert System  
### AI-Powered Vision + Embedded Control Integration

---

## 🧠 Overview
This project implements a real-time fire detection and alert system that integrates deep learning-based computer vision with a microcontroller-driven response mechanism.

A YOLO-based model processes live video input and triggers alerts only when fire is consistently detected over multiple frames. This ensures robust performance and minimizes false positives in dynamic real-world environments.

---

## 🎯 Problem Statement
Conventional vision-based fire detection systems often generate false alarms due to noise, lighting variations, or transient visual patterns.

In safety-critical systems, unreliable alerts can reduce trust and effectiveness. This project addresses the issue by introducing **temporal validation and state-based decision logic** to ensure reliable detection before triggering any action.

---

## ⚙️ System Architecture

The system is composed of three main modules:

### 1. Vision Module
- Real-time video capture using OpenCV  
- YOLO model inference for fire detection  
- Confidence and IoU-based filtering  

### 2. Decision Logic Module
- Temporal consistency validation  
- Detection persistence tracking  
- Stateful alert triggering (Fire / Stop)  

### 3. Embedded Interface Module
- Serial communication with microcontroller  
- Command-based control signaling  
- Real-time response execution  

---

## 🏗️ Project Structure

```

Day21/
├── main.py               # Core application (video processing + decision logic)
├── Arduino.py           # Microcontroller communication interface
├── prepareDataset.py    # Dataset preparation utility
├── best.pt              # Trained YOLO model weights
├── config.yaml          # Model/dataset configuration
├── cs.md / cs.pdf       # Supporting documentation
├── download.jpg         # Sample image / dataset reference
└── **pycache**/         # Compiled Python files

````

---

## 🔁 System Pipeline

1. Capture live video stream  
2. Perform YOLO inference on each frame  
3. Extract detection results  
4. Apply temporal filtering:
   - Track consecutive detection frames  
   - Suppress transient detections  
5. Decision logic:
   - Send **"Fire"** signal after sustained detection  
   - Send **"Stop"** signal after prolonged absence  
6. Transmit command to microcontroller-based alert system  
7. Display annotated output in real-time  

---

## 🔑 Key Features

- ✅ Real-time fire detection using YOLO  
- ✅ Temporal filtering to reduce false positives  
- ✅ Stateful alert system with hysteresis behavior  
- ✅ Live visualization with detection overlays  
- ✅ Integration with embedded control system  

---

## 🧪 Core Detection Logic

The system improves reliability through:

- **Detection Persistence Threshold**  
  Alerts are triggered only after multiple consecutive detections  

- **No-Detection Timeout**  
  System resets only after sustained absence of fire  

This creates a **stable and noise-resistant detection system**, suitable for real-world deployment.

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- Ultralytics YOLO  
- PySerial (Serial Communication)  
- Embedded Microcontroller System  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python ultralytics pyserial
````

### 2. Update model path in `main.py`

```python
model_path = "path_to_best.pt"
```

### 3. Configure communication port

```python
port = "COM3"
```

### 4. Run the system

```bash
python main.py
```

---

## 📊 Results & Insights

* Achieves stable real-time fire detection
* Significantly reduces false positives using temporal filtering
* Demonstrates effective integration of AI and embedded systems
* Suitable for extension into industrial safety and monitoring systems

---

## 🚧 Limitations & Future Work

* Performance depends on training dataset quality
* Limited to visible-spectrum detection
* Future improvements:

  * Multi-class hazard detection
  * Edge deployment optimization
  * IoT-based remote alert system
  * Thermal + vision sensor fusion

---

## 📌 Project Highlights

* Developed a **real-time AI-based safety system**
* Implemented **robust temporal decision logic**
* Integrated **computer vision with embedded control**
* Focused on **practical reliability over raw detection accuracy**

---

## 📬 Conclusion

This project demonstrates how AI models can be extended beyond prediction into **actionable real-world systems**, where reliability, stability, and system design are as critical as model performance.


## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_objectdetection-ai-arduino-activity-7264265355416494082-548M)


