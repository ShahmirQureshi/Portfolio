# 📏 Vision-Based Object Measurement System using Segmentation and Perspective Correction  
### Real-Time Dimension Estimation with Geometric Normalization

---

## 🧠 Overview
This project implements a computer vision-based measurement system capable of estimating object dimensions from video input.

The system combines instance segmentation, contour extraction, and perspective transformation to detect objects, normalize their orientation, and compute real-world dimensions.

---

## 🎯 Problem Statement
Accurate object measurement using vision systems is challenging due to:
- Perspective distortion  
- Arbitrary object orientation  
- Background noise  

Traditional pixel-based measurements are unreliable without proper geometric correction.

This project addresses these challenges by integrating:
- Segmentation for object isolation  
- Contour analysis for boundary extraction  
- Perspective warping for geometric normalization  

---

## ⚙️ System Architecture

The system is composed of four main modules:

### 1. Segmentation Module
- YOLO-based segmentation model  
- Extracts object masks from input frames  

### 2. Contour Extraction Module
- Converts masks into binary images  
- Detects object boundaries using contour detection  
- Approximates rotated bounding rectangles  

### 3. Perspective Normalization Module
- Identifies dominant object orientation  
- Applies homography transformation  
- Warps object into a top-down (rectified) view  

### 4. Measurement Module
- Computes object dimensions from corrected geometry  
- Converts pixel distances into approximate real-world units  

---

## 🏗️ Project Structure

```

Day24/
├── Day24FinalwithFixOrders.py   # Final pipeline implementation
├── utlis.py                     # Utility functions (reordering, distance)
├── contours.py / findcontours.py
├── findcontourwithwrap.py       # Intermediate experiments
├── Test*.mp4 / Test*.jpeg       # Input data
├── output_video*.mp4            # Processed outputs
└── output_image_with_contours*.jpeg

````id="d4lm2p"

---

## 🔁 System Pipeline

1. Capture video frame  
2. Detect target region using color segmentation  
3. Extract largest object region  
4. Compute minimum rotated bounding rectangle  
5. Apply perspective transformation (warp)  
6. Perform YOLO-based segmentation on warped frame  
7. Extract contours from segmentation mask  
8. Compute object dimensions  
9. Overlay measurements on frame  
10. Save processed video  

---

## 🔑 Key Features

- ✅ Real-time object segmentation using YOLO  
- ✅ Perspective correction via homography  
- ✅ Rotated bounding box extraction  
- ✅ Approximate real-world dimension estimation  
- ✅ End-to-end video processing pipeline  

---

## 🧪 Core Concepts (Engineering Insight)

### Perspective Correction
Objects captured at arbitrary angles are transformed into a **top-down view** using homography:
- Detect rotated rectangle  
- Map to rectangular plane  
- Eliminate perspective distortion  

---

### Measurement Strategy
- Extract ordered corner points  
- Compute Euclidean distances  
- Convert pixel values into approximate real-world units  

---

### Robust Object Isolation
- Combines color thresholding + segmentation  
- Reduces noise and irrelevant regions  
- Focuses measurement on target object  

---

## 🛠️ Tech Stack

- Python  
- OpenCV  
- NumPy  
- Ultralytics YOLO (Segmentation)  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install opencv-python ultralytics numpy
````

### 2. Update paths

```python id="f8z2mx"
video_input_path = "path_to_input_video.mp4"
video_output_path = "path_to_output_video.mp4"
model_path = "path_to_segmentation_model.pt"
```

### 3. Run the pipeline

```bash id="l2p9xz"
python Day24FinalwithFixOrders.py
```

---

## 📊 Results & Insights

* Successfully extracts object boundaries under varying orientations
* Perspective normalization significantly improves measurement stability
* Demonstrates integration of geometry and deep learning
* Suitable for inspection and measurement tasks

---

## 🚧 Limitations & Future Work

* Approximate scale conversion (no explicit calibration)
* Sensitive to lighting and color segmentation thresholds
* Future improvements:

  * Camera calibration for accurate metric scaling
  * Multi-object measurement
  * Integration with robotic inspection systems
  * Depth-based measurement (RGB-D sensors)

---

## 📌 Project Highlights

* Designed a **vision-based measurement pipeline**
* Implemented **perspective correction using homography**
* Combined **segmentation + classical vision techniques**
* Demonstrated **real-world applicability in inspection tasks**

---

## 📬 Conclusion

This project demonstrates how combining deep learning with geometric reasoning enables **practical measurement systems**, bridging the gap between perception and real-world quantitative analysis.


## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_measurement-ai-computervision-activity-7275011919483211776-Gvvi)
