# 🖐️ Vision-Based Gesture Control System for Real-Time Actuation  
### Human–Machine Interface using Hand Tracking and Signal Mapping

---

## 🧠 Overview
This project implements a real-time gesture-based control system that translates human hand movements into control signals for an embedded system.

Using hand landmark detection, the system estimates relative finger positions and maps them to a continuous control variable (angle). The generated signal is transmitted to a microcontroller, enabling intuitive and contactless control.

---

## 🎯 Problem Statement
Traditional control interfaces (buttons, joysticks, sliders) are limited in flexibility and require physical interaction.

In robotics and automation, there is increasing demand for:
- Contactless control systems  
- Intuitive human–machine interaction  
- Real-time responsiveness  

This project addresses these needs by developing a **vision-based control interface** using hand gestures.

---

## ⚙️ System Architecture

The system consists of three key modules:

### 1. Perception Module
- Hand tracking using MediaPipe  
- Extraction of 21 key landmarks  
- Identification of fingertip positions  

### 2. Signal Processing Module
- Computes normalized distance between thumb and index finger  
- Uses palm size for scale normalization  
- Maps distance to control signal (angle)  
- Applies smoothing to reduce noise  

### 3. Embedded Interface Module
- Serial communication with microcontroller  
- Transmits real-time control values  
- Enables physical actuation  

---

## 🏗️ Project Structure

```

GestureControl/
├── main.py               # Main application loop
├── value_mapper.py      # Mapping function (distance → control signal)
└── requirements.txt     # Dependencies

````

---

## 🔁 System Pipeline

1. Capture live video from webcam  
2. Detect hand landmarks using MediaPipe  
3. Extract key points (thumb, index, palm)  
4. Compute normalized distance between fingers  
5. Map distance to control variable  
6. Apply smoothing filter  
7. Send control signal via serial communication  
8. Visualize results in real-time  

---

## 🔑 Key Features

- ✅ Real-time hand tracking and gesture recognition  
- ✅ Continuous control using finger distance  
- ✅ Scale-invariant measurement (normalized by palm size)  
- ✅ Signal smoothing for stable output  
- ✅ Integration with embedded system via serial communication  

---

## 🧪 Core Concepts (Engineering Insight)

### Gesture-to-Signal Mapping
The system converts spatial hand motion into a continuous control variable:

- Distance between thumb and index finger → control input  
- Normalized by palm size → robustness to distance from camera  

---

### Signal Smoothing
To avoid jitter:
- A smoothing filter is applied  
- Ensures stable and realistic actuation  

---

### Gesture-Based Mode Activation
- Specific finger configuration activates control mode  
- Prevents unintended signal generation  

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- PySerial  
- Embedded Microcontroller System  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python mediapipe numpy pyserial
````

### 2. Set communication port

```python
port = "COM3"
```

### 3. Run the system

```bash
python main.py
```

---

## 📊 Results & Insights

* Achieves smooth and responsive gesture-based control
* Demonstrates reliable mapping from perception to actuation
* Shows robustness through normalization and filtering
* Suitable for robotics and interactive control systems

---

## 🚧 Limitations & Future Work

* Sensitive to lighting and occlusion
* Single-hand interaction only
* Future improvements:

  * Multi-gesture command system
  * Integration with robotic arms or actuators
  * Depth-based gesture understanding
  * Machine learning-based gesture classification

---

## 📌 Project Highlights

* Developed a **vision-based human–machine interface**
* Implemented **continuous control via gesture mapping**
* Designed **signal processing pipeline for stability**
* Integrated **computer vision with embedded control**

---

## 📬 Conclusion

This project demonstrates how computer vision can enable **intuitive and contactless control systems**, bridging the gap between human interaction and robotic actuation.


## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_computervision-opencv-mediapipe-activity-7254082250797932544-LvkO)
