# Comparative Odometry Analysis under Different Motion Patterns

## Overview
This project presents an experimental study on **odometry performance** for a differential-drive mobile robot (e-puck) under multiple motion behaviors. Instead of treating odometry as a standalone component, odometry is evaluated **while the robot executes different control strategies**, including open-loop and sensor-based motion.

The goal is to highlight how motion patterns and control complexity affect odometric drift—an essential insight for **mapping, localization, and SLAM**.

---

## Robot & Simulation Setup
- **Simulator:** Webots
- **Robot:** e-puck (differential drive)
- **Wheel Radius:** 0.0205 m
- **Axle Length:** 0.0565 m
- **Control Frequency:** 32 ms
- **Programming Language:** C

---

## Motion Modes Evaluated
The same odometry model is used across all experiments. Only the **motion generation strategy** changes.

### 1. Straight-Line Motion (Open-Loop)
- Constant equal wheel velocities
- No feedback or sensor correction
- Used as a baseline odometry reference

**Expected Behavior:**
- Minimal heading changes
- Lowest accumulated odometry error

---

### 2. Square Trajectory (Odometry-Guided Turns)
- Four straight segments with 90° in-place rotations
- Turns executed using **odometry-based angle estimation**

**Expected Behavior:**
- Significant error accumulation during rotations
- Demonstrates sensitivity of odometry to angular drift

---

### 3. Circular Motion (Constant Curvature)
- Unequal wheel speeds produce a continuous circular trajectory
- No external correction

**Expected Behavior:**
- Moderate odometry drift
- Continuous slip and curvature amplify integration error

---

### 4. Line Following (Sensor-Based Reactive Control)
- Ground sensors used to follow a black line
- Frequent speed corrections and heading changes
- Odometry runs passively in the background

**Expected Behavior:**
- Non-uniform odometry error
- Error influenced by sensor noise and control oscillations

---

## Odometry Model
A **midpoint integration** method is used for pose estimation:

- Linear displacement:  
  $$ ds = (dl + dr) / 2 $$
- Heading change:  
  $$ dθ = (dr − dl) / L $$

Pose update:
- $$ x ← x + ds · cos(θ + dθ/2) $$
- $$ y ← y + ds · sin(θ + dθ/2) $$
- $$ θ ← θ + dθ $$

This model remains unchanged across all experiments.

---

## Data Logging & Metrics
During execution, the following data are logged to a CSV file:
- Time
- Motion mode
- Robot action/state
- Odometry pose (x, y, θ)
- Euclidean position error from origin

This enables **offline analysis and trajectory comparison**.

---

## Results & Analysis Based on Experimental Plots

### 1. Odometry Error vs Time (Quantitative Analysis)
The error-vs-time plots clearly demonstrate that **odometry error accumulation is strongly dependent on motion strategy** rather than elapsed time alone.

**Straight-Line Motion**  
The straight-line experiment exhibits an almost perfectly linear increase in position error. This behavior is characteristic of open-loop dead reckoning where small systematic biases in wheel velocity or radius accumulate monotonically. Since no rotation is involved, heading error remains minimal, resulting in the most predictable and stable error growth.

**Circular Motion**  
The circular trajectory shows a non-monotonic but steadily increasing error profile. Continuous curvature introduces persistent angular error, which couples into translational error over time. The oscillatory nature of the curve reflects periodic alignment and misalignment between the robot’s true and estimated heading.

**Square Trajectory**  
The square motion demonstrates sharp increases in error during turning phases, followed by partial stabilization during straight segments. Each 90° in-place rotation amplifies angular estimation error, which then propagates into positional drift along the subsequent edge. This mode highlights how **discrete rotations are particularly damaging for odometry accuracy**.

**Line Following (Reactive Control)**  
Line following exhibits the highest variability in error growth. Frequent corrective maneuvers, sensor noise, and oscillatory steering introduce irregular angular disturbances. Interestingly, the error occasionally decreases, indicating partial self-correction due to sensor feedback—something not observed in purely open-loop motions.

---

### 2. Odometry Trajectories (Qualitative Analysis)
Trajectory plots provide intuitive insight into how odometry errors distort geometric paths.

**Straight Trajectory**  
The estimated trajectory remains nearly perfectly linear, confirming that odometry performs best when heading remains constant.

**Circular Trajectory**  
While the overall circular shape is preserved, the loop does not close perfectly, revealing accumulated angular drift and slight radial distortion.

**Square Trajectory**  
The square shape is visibly skewed, with edges failing to remain orthogonal and the final position not returning to the start. This distortion directly reflects rotational error at each corner.

**Line-Following Trajectory**  
The trajectory is highly irregular, reflecting continuous corrective behavior. This plot clearly shows how reactive control introduces non-smooth motion that degrades odometry consistency.

---

### Summary of Observations
| Motion Type | Odometry Accuracy | Dominant Error Source |
|------------|------------------|----------------------|
| Straight Line | High | Systematic wheel bias |
| Circle | Medium | Continuous angular drift |
| Square | Low | Discrete rotational error |
| Line Following | Variable | Sensor noise & control oscillations |

---

## Why This Project Matters
- Demonstrates **experimental thinking**, not just implementation
- Shows understanding of **odometry limitations**
- Bridges the gap between **control, sensing, and localization**
- Directly prepares for advanced topics such as **mapping and SLAM**

---

## Skills Demonstrated
- Differential-drive kinematics
- Odometry integration methods
- Finite-state motion control
- Sensor-based reactive behavior
- Experimental evaluation & data logging
- Robotics simulation using Webots

---

## Future Extensions
- Ground-truth comparison using GPS for quantitative error analysis
- Velocity-dependent odometry drift study
- Integration with mapping or localization algorithms

---

## Repository Structure (Suggested)
```
controllers/
 └── comparative_odometry.c
results/
 └── odom_log.csv
plots/
 └── trajectory_analysis.png
README.md
```

---

## One-Line Resume Description
**Comparative Odometry Analysis for an e-puck robot in Webots, evaluating localization drift across open-loop, trajectory-based, and sensor-driven motion behaviors.**

---

## GitHub README (Ready to Use)

### Comparative Odometry Analysis in Webots

This project investigates the limitations of wheel-encoder-based odometry for a differential-drive robot by comparing localization performance across four motion strategies: straight-line motion, square trajectory, circular motion, and sensor-based line following.

#### Motivation
Odometry is a foundational component of mobile robotics, yet it suffers from cumulative error. Understanding how different motion patterns affect odometry accuracy is critical for higher-level tasks such as mapping and SLAM.

#### Experimental Setup
- Robot: e-puck (differential drive)
- Simulator: Webots
- Control frequency: 32 ms
- Odometry model: Midpoint integration

#### Motion Modes
- **Straight:** Open-loop baseline with constant velocity
- **Square:** Odometry-guided 90° turns
- **Circle:** Constant curvature motion
- **Line Following:** Reactive sensor-based control

#### Results
- Straight motion yields the most predictable odometry performance
- Rotational maneuvers significantly amplify localization error
- Sensor-driven control introduces irregular but partially self-correcting behavior

#### Key Insight
> Odometry accuracy is influenced more by motion strategy and heading dynamics than by distance traveled alone.

#### Repository Structure
```
controllers/
 └── comparative_odometry.c
plots/
 └── collages/
results/
 └── odom_log.csv
README.md
```

#### Future Work
- Ground-truth comparison using GPS
- Velocity-dependent drift analysis
- Integration with mapping or SLAM algorithms

---

This project serves as a foundation for advanced localization and mapping research.

