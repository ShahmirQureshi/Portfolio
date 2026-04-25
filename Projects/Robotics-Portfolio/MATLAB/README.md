# Robotics Portfolio

A curated collection of robotics projects focused on kinematics, trajectory planning, dynamics and control, mobile robot navigation, SCARA systems, and vision-based human-robot interaction.

This repository is organized as a robotics engineering portfolio rather than a raw file dump. Each subfolder groups related MATLAB and Simulink work into a clear project theme.

---

## Repository Highlights

This portfolio demonstrates:

- Forward and inverse kinematics for 2DOF and 3DOF manipulators
- Trajectory generation using polynomial and spline-based methods
- Robot dynamics and control using PD and computed torque control
- SCARA robot modeling and inverse kinematics
- Mobile robot navigation using occupancy grids and PRM
- Gesture-based robotic control using computer vision

---

## Project Structure

### 1. Kinematics
**Folder:** `01_kinematics/`

Includes forward kinematics, inverse kinematics, and basic manipulator motion models for planar and spatial robot arms.

Representative files:
- `DOF2_PlanarRobot.m`
- `Lesson1_DOF2_FK.slx`
- `Lesson2_DOF2_IK.slx`
- `DOF2_Arm.slx`
- `DOF3_Arm.slx`
- `Lesson5_DOF3_FK.slx`
- `Lesson5_DOF3_IK.slx`

---

### 2. Trajectory Planning
**Folder:** `02_trajectory_planning/`

Contains multiple trajectory generation approaches for robotic motion, including cubic, quintic, trapezoidal, and B-spline trajectories.

Representative files:
- `Lesson3_DOF2_GenerateTrajectory.slx`
- `Lesson3B_DOF2_GenerateTrajectory.slx`
- `Lesson5_DOF3_GenerateTrajectory.slx`
- `Lesson14_CubicPoly.slx`
- `Lesson14_QuinticPoly.slx`
- `Lesson14_BSplineTraj.slx`
- `Lesson14_TrapezoidalTrajec.slx`

---

### 3. Dynamics and Control
**Folder:** `03_dynamics_and_control/`

Focuses on robot dynamics, PD control, computed torque control, and torque-based motion execution.

Representative files:
- `Lesson6_DOF3_DriveUsingDynamics.slx`
- `Lesson6B_DOF3_DriveUsingDynamics.slx`
- `Lesson7_DOF3_RRR_PD.slx`
- `Lesson8_DOF3_RRR_CTC.slx`
- `Lin_model_Torque.m`

---

### 4. SCARA Robot
**Folder:** `04_scara_robot/`

Contains SCARA robot kinematics and inverse kinematics models, along with supporting Simulink files.

Representative files:
- `Lesson10_SCARA_IK.slx`
- `inverseKin1.m`
- `start_file.m`
- `IK_SCARA_drive.slx`
- `SCARA.slx`
- `SLab4_Org.slx`
- `SLab4_Robot.slx`

---

### 5. Mobile Robot Navigation
**Folder:** `05_mobile_robot_navigation/`

Contains occupancy-grid-based mapping and sampling-based path planning using PRM.

Representative files:
- `Lesson9_PRM_MobileRobot.m`
- `Final_occupancy_grid.mat`
- `Final_occupancy_grid_inflated.mat`

---

### 6. Human-Robot Interaction
**Folder:** `06_human_robot_interaction/`

Contains gesture-based control work and vision-assisted robotic interaction models.

Representative files:
- `GestureBased_DOF3_FK.slx`
- `DOF3_Arm.slx`
- `DOF2_PlanarRobot.m`

---

## Key Robotics Concepts Covered

This repository demonstrates the following concepts:

- Forward and inverse kinematics
- Jacobian-based motion reasoning
- Trajectory generation and interpolation
- Robot dynamics and control
- Path planning with occupancy grids and PRM
- SCARA robot modeling
- Vision-based gesture control for robotic systems

---

## Toolchain

- MATLAB
- Simulink
- Robotics System Toolbox
- Computer Vision Toolbox
- Python for supporting integration in selected projects

---

## What the Simulink Files Represent

The `.slx` files are Simulink model files. They are used to build, simulate, and test robot behavior visually in block-diagram form.

They are included here to show:
- robot kinematics models
- motion planning logic
- dynamic simulation
- controller design
- system-level integration

---

## How to Use This Repository

1. Open the relevant project folder.
2. Run the MATLAB script or open the Simulink model.
3. Review the model parameters and workspace variables.
4. Simulate the system and observe the output.

Example:
- For PRM navigation, open `05_mobile_robot_navigation/Lesson9_PRM_MobileRobot.m`
- For SCARA kinematics, open `04_scara_robot/inverseKin1.m`
- For control systems, open the PD or CTC Simulink models in `03_dynamics_and_control/`

---

## Recommended Portfolio Ordering

If you want to present these projects on GitHub, highlight them in this order:

1. Mobile robot navigation
2. SCARA kinematics
3. Dynamics and control
4. Trajectory planning
5. Kinematics
6. Gesture-based control

That ordering makes the portfolio feel more robotics-focused and more advanced.

---

## Notes

This repository is intentionally organized as a clean engineering portfolio. Temporary simulation files, caches, and generated artifacts are excluded so that the structure stays readable and professional.

---

## Conclusion

This portfolio shows practical work in robotic modeling, planning, control, and human-robot interaction. It reflects a progression from basic kinematics to more advanced autonomous navigation and control systems.