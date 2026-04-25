
# 🚗 Real-Time Traffic Flow Analysis using YOLOv8 and Multi-Object Tracking

### Intelligent Vehicle Counting and Direction Estimation System

---

## 🧠 Overview
This project implements a real-time traffic flow analysis system using deep learning-based object detection and multi-object tracking.

The system processes video input to detect vehicles, track them across frames, and estimate their movement direction (up/down) based on spatial transitions. It provides structured traffic insights such as directional counts for different vehicle types.

---

## 🎯 Problem Statement
Accurate traffic monitoring is essential for smart cities, infrastructure planning, and autonomous systems. Traditional counting methods often fail in dynamic environments due to occlusion, overlapping objects, and inconsistent detection.

This project addresses these challenges by combining **object detection with persistent tracking**, enabling reliable counting and direction estimation in real-world scenarios.

---

## ⚙️ System Architecture

The system consists of three core components:

### 1. Detection Module
- YOLOv8 model for real-time object detection  
- Identifies vehicles such as cars, trucks, buses, and motorcycles  

### 2. Tracking Module
- Persistent object tracking using built-in tracking IDs  
- Maintains identity across frames  
- Handles occlusion and motion continuity  

### 3. Direction Analysis Module
- Virtual line-based crossing logic  
- Determines movement direction (Up / Down)  
- Updates class-wise counters  

---

## 🏗️ Project Structure

```

Day28/
├── main.py                # Core logic (detection + tracking + counting)
├── Video (3).mp4         # Input traffic video
└── processed_video7.mp4  # Output processed video with annotations

````

---

## 🔁 System Pipeline

1. Load input video stream  
2. Perform YOLOv8 detection on each frame  
3. Assign persistent IDs using tracking  
4. Compute object centroid  
5. Compare previous and current positions  
6. Detect line crossing events  
7. Classify direction:
   - Upward movement  
   - Downward movement  
8. Update class-wise counters  
9. Render annotated output video  

---

## 🔑 Key Features

- ✅ Real-time vehicle detection using YOLOv8  
- ✅ Multi-object tracking with persistent IDs  
- ✅ Direction-aware vehicle counting  
- ✅ Class-wise traffic statistics  
- ✅ Annotated video output generation  

---

## 🧪 Core Logic (Engineering Insight)

The system uses a **virtual horizontal line** as a reference:

- Each object’s centroid is tracked across frames  
- Movement is determined by comparing previous vs current position  
- Crossing the line triggers a directional event  

### Direction Rules:
- Crossing from above → below → **Down**
- Crossing from below → above → **Up**

This creates a **lightweight yet effective traffic flow estimation system** without requiring complex trajectory prediction models.

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- Ultralytics YOLOv8  
- Built-in Multi-Object Tracking (MOT)  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python ultralytics
````

### 2. Update input/output paths in `main.py`

```python id="z0h8sq"
video_path = "path_to_input_video.mp4"
output_path = "path_to_output_video.mp4"
```

### 3. Run the script

```bash id="y2d8lm"
python main.py
```

---

## 📊 Results & Insights

* Successfully tracks multiple vehicles simultaneously
* Provides direction-aware traffic statistics
* Handles moderate occlusion scenarios effectively
* Demonstrates practical application of MOT in traffic systems

---

## 🚧 Limitations & Future Work

* Performance depends on detection quality in crowded scenes
* Limited robustness under extreme occlusion
* Future improvements:

  * Lane-wise traffic analysis
  * Speed estimation using frame timing
  * Trajectory prediction models
  * Integration with smart traffic control systems

---

## 📌 Project Highlights

* Designed a **real-time traffic analysis system**
* Implemented **multi-object tracking with ID persistence**
* Developed **direction-aware counting logic**
* Demonstrated **spatial reasoning using vision data**

---

## 📬 Conclusion

This project showcases how computer vision can be extended beyond detection into **scene understanding and behavioral analysis**, forming the foundation for intelligent transportation and autonomous systems.

## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_ai-computervision-deeplearning-activity-7283380791982645248-0BPY)

