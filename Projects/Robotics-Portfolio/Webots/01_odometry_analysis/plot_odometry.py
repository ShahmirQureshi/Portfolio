import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv(r"C:\Users\20MTE034\Desktop\Webot_Course\odometry_analysis\controllers\mobile_robot_odom_analysis\odom_log_Line_Following.csv")

# -------------------------
# Trajectory Plot (x vs y)
# -------------------------
plt.figure()
plt.plot(data["x"], data["y"])
plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.title("Odometry Trajectory")
plt.axis("equal")
plt.grid(True)
plt.savefig("trajectory.png", dpi=300)
plt.show()

# -------------------------
# Error vs Time
# -------------------------
plt.figure()
plt.plot(data["time"], data["error"])
plt.xlabel("Time (s)")
plt.ylabel("Position Error (m)")
plt.title("Odometry Error Growth")
plt.grid(True)
plt.savefig("error_vs_time.png", dpi=300)
plt.show()

# -------------------------
# Heading vs Time (optional)
# -------------------------
plt.figure()
plt.plot(data["time"], data["theta"])
plt.xlabel("Time (s)")
plt.ylabel("Heading (rad)")
plt.title("Heading vs Time")
plt.grid(True)
plt.savefig("theta_vs_time.png", dpi=300)
plt.show()
