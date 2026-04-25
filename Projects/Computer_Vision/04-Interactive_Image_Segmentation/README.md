# 🎯 Interactive Image Segmentation System using Streamlit and AI API  
### User-Guided Background Removal with Click-Based Input

---

## 🧠 Overview
This project implements an interactive image segmentation system that allows users to remove image backgrounds using a simple click-based interface.

The system combines a web-based frontend with an AI-powered backend API to perform background removal based on user-selected points, enabling precise and controllable image editing.

---

## 🎯 Problem Statement
Automatic background removal systems often struggle with complex scenes or ambiguous foreground objects. Fully automated approaches lack user control, leading to incorrect segmentation.

This project addresses the problem by introducing a **human-in-the-loop interaction**, where the user provides spatial guidance to improve segmentation accuracy.

---

## ⚙️ System Architecture

The system is divided into three main components:

### 1. User Interface (Frontend)
- Built using Streamlit  
- Image upload and visualization  
- Click-based coordinate selection  

### 2. Interaction Module
- Captures user click coordinates  
- Encodes image and metadata  
- Sends structured request to API  

### 3. AI Processing Backend
- External API performs background removal  
- Returns processed image with transparency  
- Result is decoded and displayed  

---

## 🏗️ Project Structure

```

Day29/
├── app.py                # Streamlit application
├── bg2.jpg              # Background UI image
└── cached_outputs/      # Locally saved processed images

````id="h3k9zt"

---

## 🔁 System Pipeline

1. Upload input image  
2. Display image in UI  
3. User clicks on target region  
4. Capture (x, y) coordinates  
5. Encode image in Base64  
6. Send request to AI API:
   - Image data  
   - Click coordinates  
7. Receive processed output  
8. Decode and render result  
9. Cache output locally  

---

## 🔑 Key Features

- ✅ Interactive click-based segmentation  
- ✅ Human-in-the-loop AI system  
- ✅ Real-time web interface using Streamlit  
- ✅ API-based inference (decoupled architecture)  
- ✅ Local caching to optimize repeated requests  

---

## 🧪 Core Concept (Engineering Insight)

### Human-Guided Segmentation

Instead of relying purely on automated detection, the system uses:

- **User-provided spatial cues (click points)**  
- **AI model guided by interaction input**  

This approach improves:
- Segmentation accuracy  
- User control  
- Robustness in complex scenes  

---

### Efficient Data Handling

- Image is encoded in **Base64** before transmission  
- API response is decoded back into image format  
- Processed results are cached locally to reduce redundant API calls  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- OpenCV  
- NumPy  
- PIL  
- REST API (Model Deployment)  

---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install streamlit opencv-python numpy pillow requests
````

### 2. Run the application

```bash id="k2p4mx"
streamlit run app.py
```

### 3. Usage

* Upload an image
* Click on the object of interest
* Press **"Remove Background"**
* View the processed result

---

## 📊 Results & Insights

* Provides intuitive and interactive segmentation
* Improves accuracy compared to fully automated methods
* Demonstrates effective frontend-backend AI integration
* Shows real-world usability for image editing tasks

---

## 🚧 Limitations & Future Work

* Depends on external API performance
* Requires internet connectivity
* Future improvements:

  * Multi-click segmentation support
  * Brush-based interaction
  * Real-time preview updates
  * On-device model deployment

---

## 📌 Project Highlights

* Built an **interactive AI-powered image editing system**
* Implemented **human-in-the-loop decision making**
* Designed **frontend + backend integration pipeline**
* Demonstrated **practical deployment of AI models**

---

## 📬 Conclusion

This project demonstrates how AI systems can be enhanced through **user interaction and system design**, bridging the gap between automated models and real-world usability.


## Project Demo

🎥 Watch the demo on LinkedIn:
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-blue?style=for-the-badge)](https://www.linkedin.com/posts/shahmir-qureshi_ai-computervision-python-activity-7285187267831152641-Y7Ei)
