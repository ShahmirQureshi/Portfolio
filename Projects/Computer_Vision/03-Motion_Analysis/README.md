
# 🧍‍♂️ Real-Time Human Motion Analysis using Pose Estimation  
### Push-Up Detection and Repetition Counting via Joint Angle Modeling

---

## 🧠 Overview
This project implements a real-time human motion analysis system using deep learning-based pose estimation.

The system detects human body keypoints from video input and analyzes joint kinematics to identify and count push-up repetitions. By modeling elbow joint angles over time, it transforms raw pose data into meaningful biomechanical insights.

---

## 🎯 Problem Statement
Monitoring human exercises accurately is challenging due to variations in posture, speed, and camera perspective. Simple frame-based detection methods are unreliable for tracking repetitive motion.

This project addresses the problem by combining:
- Pose estimation for extracting skeletal structure  
- Geometric analysis for joint angle computation  
- Temporal state modeling for repetition counting  

---

## ⚙️ System Architecture

The system is composed of three main modules:

### 1. Pose Estimation Module
- YOLOv8 pose model for keypoint detection  
- Extracts 2D coordinates of body joints  

### 2. Kinematic Analysis Module
- Computes joint angles (shoulder–elbow–wrist)  
- Uses trigonometric relationships to estimate motion  

### 3. State-Based Repetition Counter
- Tracks movement phases (top → bottom → top)  
- Uses threshold-based state transitions  
- Counts valid push-up repetitions  

---

## 🏗️ Project Structure

```

Motion_Analysis/
├── main.py                 # Core logic (pose + angle + counting)
├── input_video            # Raw exercise video
└── out_pushup.mp4         # Annotated output video

````id="sz1b4a"

---

## 🔁 System Pipeline

1. Load input video stream  
2. Perform pose estimation on each frame  
3. Extract keypoints (shoulder, elbow, wrist)  
4. Compute elbow joint angle  
5. Apply state logic:
   - Detect downward motion (angle < threshold)  
   - Detect upward motion (angle > threshold)  
6. Increment repetition counter  
7. Overlay results on video  
8. Save processed output  

---

## 🔑 Key Features

- ✅ Real-time human pose estimation  
- ✅ Joint angle computation using geometry  
- ✅ State-based repetition counting  
- ✅ Robust to moderate motion variations  
- ✅ Annotated video output with live metrics  

---

## 🧪 Core Logic (Engineering Insight)

### Joint Angle Calculation
The elbow angle is computed using three keypoints:

- Shoulder (A)  
- Elbow (B)  
- Wrist (C)  

Angle is calculated using vector geometry:
- Uses arctangent-based formulation  
- Ensures stable angle estimation in degrees  

---

### Motion Detection Logic

The system models push-ups as a **two-state cycle**:

- **Bottom Position** → elbow angle < 90°  
- **Top Position** → elbow angle > 135°  

A valid repetition is counted when:
1. System enters bottom state  
2. Then returns to top state  

This creates a **finite-state machine**, ensuring accurate counting and avoiding false increments.

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- NumPy  
- Ultralytics YOLOv8 Pose  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python ultralytics numpy
````

### 2. Update input/output paths

```python id="g2lm8q"
input_path = "path_to_input_video"
output_path = "path_to_output_video.mp4"
```

### 3. Run the script

```bash id="k3dm1x"
python main.py
```

---

## 📊 Results & Insights

* Accurately counts push-ups in controlled scenarios
* Demonstrates reliable angle-based motion detection
* Converts pose data into interpretable metrics
* Shows potential for fitness tracking and rehabilitation

---

## 🚧 Limitations & Future Work

* Sensitive to camera angle and occlusion
* Uses only one arm (right side) for analysis
* Future improvements:

  * Multi-joint analysis for better robustness
  * Support for multiple exercises (squats, pull-ups)
  * Real-time feedback system
  * Integration with wearable or robotics systems

---

## 📌 Project Highlights

* Developed a **pose-based human motion analysis system**
* Implemented **joint angle estimation from keypoints**
* Designed a **state machine for repetition counting**
* Bridged **computer vision with biomechanics**

---

## 📬 Conclusion

This project demonstrates how pose estimation can be extended beyond visualization into **quantitative motion analysis**, forming the basis for intelligent fitness systems, rehabilitation tools, and human-robot interaction.


## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_computervision-deeplearning-ai-activity-7263110368602771457-7QGS)
