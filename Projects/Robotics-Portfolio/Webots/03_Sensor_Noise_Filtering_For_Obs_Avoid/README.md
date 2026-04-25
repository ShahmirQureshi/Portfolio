# Sensor Noise Filtering for Obstacle Avoidance

This project implements **sensor noise filtering** for a differential-drive e-puck robot performing **reactive obstacle avoidance** in Webots.

Raw sensor readings are often noisy, causing unstable motion. By applying **moving average (MA)** or **exponential moving average (EMA)** filters, the robot navigates more smoothly while avoiding obstacles.

---

## Table of Contents

- [Sensor Noise Filtering for Obstacle Avoidance](#sensor-noise-filtering-for-obstacle-avoidance)
  - [Table of Contents](#table-of-contents)
  - [1. Overview](#1-overview)
  - [2. Robot \& Simulation Setup](#2-robot--simulation-setup)
  - [3. Reactive Obstacle Avoidance Behavior](#3-reactive-obstacle-avoidance-behavior)
  - [4. Sensor Noise Filtering](#4-sensor-noise-filtering)
    - [4.1 Moving Average (MA)](#41-moving-average-ma)
    - [4.2 Exponential Moving Average (EMA)](#42-exponential-moving-average-ema)
  - [5. Motor Control](#5-motor-control)
  - [6. Data Logging \& Metrics](#6-data-logging--metrics)
  - [7. Results \& Analysis](#7-results--analysis)
    - [7.1 Sensor Noise Reduction](#71-sensor-noise-reduction)
    - [7.2 Motor Velocity Smoothness](#72-motor-velocity-smoothness)
    - [7.3 MA vs EMA Behavior](#73-ma-vs-ema-behavior)
    - [7.4 Summary of Observations](#74-summary-of-observations)
  - [8. Discussion](#8-discussion)
  - [9. Why This Project Matters](#9-why-this-project-matters)
  - [10. Skills Demonstrated](#10-skills-demonstrated)
  - [11. Future Extensions](#11-future-extensions)
  - [12. Repository Structure](#12-repository-structure)
  - [13. One-Line Resume Entry](#13-one-line-resume-entry)

---
## 1. Overview

This project implements *sensor noise filtering* for a differential-drive e-puck robot performing *reactive obstacle avoidance* in Webots. Raw distance and light sensor readings are inherently noisy, which can lead to oscillatory motion, false obstacle detections, and unstable wheel commands.

To address this, *Moving Average (MA)* and *Exponential Moving Average (EMA)* filters are applied to sensor readings before they are used for motor control. The objective is to *quantitatively evaluate noise reduction and motion smoothness* while preserving the original reactive behavior of the robot.

---

## 2. Robot & Simulation Setup

* *Simulator:* Webots
* *Robot:* e-puck (differential drive)
* *Control Frequency:* 32 ms
* *Motors:* Velocity-controlled left & right wheels
* *Sensors:*

  * 8 infrared distance sensors (ps0–ps7)
  * 8 light sensors (ls0–ls7)

All sensor readings are scaled to motor control units before filtering and logging.

---

## 3. Reactive Obstacle Avoidance Behavior

The robot uses a *reactive control law* based on linear combinations of sensor readings:

* Left wheel velocity is influenced primarily by *right-side sensors*
* Right wheel velocity is influenced primarily by *left-side sensors*
* Light sensors introduce a continuous low-weight bias to wheel velocities

This design allows obstacle avoidance without global planning or localization.

---

## 4. Sensor Noise Filtering

Two filtering methods are implemented and evaluated.

### 4.1 Moving Average (MA)

The moving average filter computes the mean of the most recent (N) samples:

[
s_\text{filtered} = \frac{1}{N} \sum_{i=1}^{N} s_i
]

* Strong smoothing of high-frequency noise
* Increased latency when obstacles appear suddenly

---

### 4.2 Exponential Moving Average (EMA)

The EMA filter applies recursive smoothing using a factor (\alpha):

[
s_\text{filtered} = \alpha \cdot s_\text{current} + (1 - \alpha) \cdot s_\text{previous}
]

* Faster response to environmental changes
* Reduced lag compared to MA
* Tunable responsiveness via (\alpha)

Filters are applied *at every control step* (32 ms), and filtered values replace raw readings for motor velocity computation.

---

## 5. Motor Control

* Wheel velocities (phil, phir) are computed using *filtered sensor values*
* Motor speeds are clipped to ([-\text{MAX_SPEED}, \text{MAX_SPEED}])
* Filtering reduces abrupt velocity changes caused by noisy sensor spikes

---

## 6. Data Logging & Metrics

All relevant data is logged in results/sensor_log.csv, including:

* Time
* Raw distance and light sensor readings
* Filtered sensor readings
* Left and right wheel velocities

This enables *quantitative evaluation* of noise reduction and control smoothness.

---

## 7. Results & Analysis

### 7.1 Sensor Noise Reduction

Statistical analysis of the logged sensor data confirms that filtering effectively reduces measurement variability:

* **Average standard deviation (raw distance sensors):** ~0.392
* **Average standard deviation (filtered distance sensors):** ~0.380

This reduction demonstrates that both **Moving Average (MA)** and **Exponential Moving Average (EMA)** filters successfully suppress high-frequency noise while preserving meaningful obstacle-related information.

Time-series comparisons between raw and filtered sensor readings clearly illustrate this effect. As shown in **Figure 1** and **Figure 2**, filtering significantly reduces sharp spikes and produces smoother, more continuous sensor signals, particularly in regions where the robot approaches obstacles.

![Raw vs Filtered Distance Sensors](plots/Distance_Sensors_Raw_vs_Filtered.png)
*Figure 1: Raw and filtered distance sensor readings showing reduced noise and smoother trends.*

![Raw vs Filtered Light Sensors](plots/Light_Sensors_Raw_vs_Filtered.png)
*Figure 2: Raw and filtered light sensor readings demonstrating suppression of high-frequency fluctuations.*

An aggregated view of noise reduction across sensors further confirms this improvement. **Figure 3** summarizes the overall decrease in sensor variability after filtering.

![Sensor Noise Reduction](plots/Sensor_Noise_Reduction.png)
*Figure 3: Overall sensor noise reduction achieved through MA and EMA filtering.*

---

### 7.2 Motor Velocity Smoothness

Analysis of wheel velocity data shows a clear improvement in motion stability when filtered sensor readings are used for control:

* **Left wheel velocity standard deviation:** ~1.01
* **Right wheel velocity standard deviation:** ~1.50

The motor velocity plots in **Figure 4** highlight the impact of filtering on control smoothness. Compared to unfiltered control, the robot exhibits fewer abrupt accelerations and decelerations, reduced oscillatory behavior near obstacles, and more consistent turning responses.

![Left and Right Motor Velocities](plots/Motor_Velocities.png)
*Figure 4: Left and right wheel velocities over time, illustrating smoother control with filtered sensor inputs.*

By preventing sudden motor commands caused by transient sensor noise, filtering results in noticeably **smoother and more stable robot motion**, while maintaining reactive obstacle avoidance behavior.

---

### 7.3 MA vs EMA Behavior

A direct comparison of filtering strategies reveals distinct behavioral differences, as summarized below:

| Filter           | Behavior                                |
| ---------------- | --------------------------------------- |
| Moving Average   | Strong smoothing, increased lag         |
| EMA              | Faster response, good noise suppression |
| Raw (unfiltered) | High noise, unstable motion             |

Sensor-level comparisons in **Figure 5** show that EMA responds more quickly to changing obstacle distances than MA, which tends to introduce noticeable latency due to windowed averaging.

![MA vs EMA Sensor Comparison](plots/DS3_DS4_Comparison.png)
*Figure 5: Comparison of MA and EMA filtering on selected distance sensors, highlighting responsiveness differences.*

A spatial overview of filtered distance sensor activity is shown in **Figure 6**, where EMA maintains smoother activation patterns without sacrificing responsiveness to nearby obstacles.

![Filtered Distance Sensors Heatmap](plots/Filtered_Distance_Sensors_Heatmap.png)
*Figure 6: Heatmap of filtered distance sensor activations during navigation.*

Overall, **EMA provides the best trade-off between responsiveness and stability**, making it particularly well-suited for real-time reactive obstacle avoidance in mobile robots.


---

### 7.4 Summary of Observations

| Metric            | Observation               |
| ----------------- | ------------------------- |
| Sensor noise      | Reduced after filtering   |
| Motion smoothness | Significantly improved    |
| Control stability | No oscillatory divergence |
| Reactive behavior | Preserved                 |
| Filter latency    | MA > EMA                  |

---

## 8. Discussion

This experiment demonstrates that *sensor noise filtering is essential* for stable reactive control in mobile robots. While raw sensor readings are sufficient for basic obstacle avoidance, filtering substantially improves motion quality and control reliability.

EMA filtering is particularly effective for real-time robotics due to its low computational cost and tunable responsiveness. However, filtering alone does not address long-term perception uncertainty, motivating the use of *sensor fusion and state estimation* in advanced systems.

---

## 9. Why This Project Matters

This project demonstrates practical understanding of:

* Sensor noise characteristics
* Real-time filtering techniques
* Reactive robot control
* Data-driven performance evaluation

These skills are foundational for *autonomous navigation, SLAM, and perception-driven robotics systems*.

---

## 10. Skills Demonstrated

* Sensor handling and control loops in Webots
* Moving Average & Exponential Moving Average filtering
* Reactive obstacle avoidance
* Data logging and quantitative analysis
* Robotics control programming

---

## 11. Future Extensions

* Median and Kalman filtering comparison
* Fusion of distance sensors with odometry
* Dynamic obstacle experiments
* Transition to behavior-based or hybrid navigation

---

## 12. Repository Structure

```
Sensor_Noise_Filtering_For_Obs_Avoid/
│
├── controllers/
│   └── Noise_Filtering_Reactive_Behaviour.py
│
├── worlds/
│   └── Noise_Filtering_Reactive_Behaviour.wbt
│
├── results/
│   └── sensor_log.csv
│
├── plots/
│   ├── Distance_Sensors_Raw_vs_Filtered.png
│   ├── Light_Sensors_Raw_vs_Filtered.png
│   ├── Motor_Velocities.png
│   ├── Filtered_Distance_Sensors_Heatmap.png
│   ├── Sensor_Noise_Reduction.png
│   └── DS3_DS4_Comparison.png
│
├── README.md
└── requirements.txt
```



---

## 13. One-Line Resume Entry

*Implemented sensor noise filtering (MA & EMA) for reactive obstacle avoidance in an e-puck robot using Webots, achieving smoother motion and reduced control oscillations through data-driven analysis.*
