# 🤖 Autonomous Navigation using Occupancy Grid Mapping and PRM Planning  
### Path Planning and Control Simulation for Mobile Robots

---

## 🧠 Overview
This project implements a complete autonomous navigation pipeline for a mobile robot, including environment modeling, path planning, and motion control.

The system generates a custom occupancy grid map, applies obstacle inflation for robot safety, computes a collision-free path using Probabilistic Roadmap (PRM), and simulates robot motion using a Pure Pursuit controller.

---

## 🎯 Problem Statement
Autonomous robots must navigate safely in environments with obstacles while respecting their physical constraints.

Key challenges include:
- Representing the environment accurately  
- Planning feasible collision-free paths  
- Ensuring smooth and stable motion control  

This project addresses these challenges through a **full navigation stack implementation**.

---

## ⚙️ System Architecture

The system consists of four main modules:

### 1. Environment Modeling
- Custom occupancy grid generation  
- Includes boundaries and cylindrical obstacles  
- Adjustable spatial resolution  

### 2. Map Inflation
- Expands obstacles based on robot size  
- Ensures collision-free navigation  
- Accounts for robot footprint  

### 3. Path Planning (PRM)
- Probabilistic Roadmap (PRM) algorithm  
- Random sampling of configuration space  
- Graph-based path search  

### 4. Motion Control
- Pure Pursuit controller for trajectory tracking  
- Continuous pose updates  
- Differential drive kinematics  

---

## 🏗️ Project Structure

```

NavigationProject/
├── map_generation.m        # Occupancy grid creation
├── planning_simulation.m   # PRM + control simulation
├── Final_occupancy_grid.mat
└── Final_occupancy_grid_inflated.mat

````id="n2v8qk"

---

## 🔁 System Pipeline

1. Generate occupancy grid map  
2. Define obstacles (walls + cylindrical structure)  
3. Inflate map based on robot size  
4. Select start and goal positions  
5. Generate roadmap using PRM  
6. Compute collision-free path  
7. Track path using Pure Pursuit controller  
8. Simulate robot motion in environment  

---

## 🔑 Key Features

- ✅ Custom occupancy grid generation  
- ✅ Obstacle inflation for safety margins  
- ✅ PRM-based path planning  
- ✅ Interactive start/goal selection  
- ✅ Closed-loop path tracking using controller  
- ✅ Full navigation pipeline simulation  

---

## 🧪 Core Concepts (Engineering Insight)

### Occupancy Grid Representation
- Environment discretized into grid cells  
- Binary representation:
  - 0 → free space  
  - 1 → obstacle  

---

### Map Inflation
- Expands obstacles based on robot footprint  
- Converts point robot → realistic robot model  
- Prevents collisions in narrow spaces  

---

### Probabilistic Roadmap (PRM)
- Samples random nodes in free space  
- Connects nodes based on distance  
- Finds shortest path using graph search  

---

### Pure Pursuit Control
- Tracks path using lookahead-based steering  
- Computes linear and angular velocity  
- Ensures smooth trajectory following  

---

## 🛠️ Tech Stack

- MATLAB  
- Robotics System Toolbox  
- Numerical Simulation  

---

## ▶️ How to Run

1. Run map generation script:
```matlab
map_generation
````

2. Run planning and control simulation:

```matlab
planning_simulation
```

3. Select start and goal points interactively
4. Observe planned path and robot motion

---

## 📊 Results & Insights

* Successfully generates collision-free paths
* Demonstrates stable path tracking
* Shows importance of map inflation for safety
* Validates integration of planning and control

---

## 🚧 Limitations & Future Work

* Static environment (no dynamic obstacles)
* No real robot deployment
* Future improvements:

  * A* or RRT* comparison
  * Dynamic obstacle avoidance
  * Integration with ROS / real robot
  * Sensor-based mapping (SLAM)

---

## 📌 Project Highlights

* Built a **complete robotic navigation pipeline**
* Implemented **PRM-based path planning**
* Applied **Pure Pursuit control for trajectory tracking**
* Demonstrated **integration of mapping, planning, and control**

---

## 📬 Conclusion

This project demonstrates a full-stack robotics approach, combining **environment modeling, motion planning, and control**, forming a foundation for autonomous mobile robot navigation systems.
