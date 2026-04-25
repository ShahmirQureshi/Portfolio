import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Load CSV
# -----------------------------
file_path = r"C:\Users\20MTE034\Desktop\Webot_Course\Sensor_Noise_Filtering_For_Obs_Avoid\results\sensor_log.csv"
df = pd.read_csv(file_path)
time = df['time']

# -----------------------------
# Create plots folder if not exists
# -----------------------------
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

# -----------------------------
# 1. Distance Sensors: Each sensor in a subplot
# -----------------------------
fig, axes = plt.subplots(8, 1, figsize=(12, 20), sharex=True)
fig.suptitle("Raw vs Filtered Distance Sensors", fontsize=16)

for i in range(8):
    axes[i].plot(time, df[f'ds{i}'], label=f'ds{i} raw', linestyle='--', color='blue')
    axes[i].plot(time, df[f'ds_f{i}'], label=f'ds{i} filtered', color='red')
    axes[i].set_ylabel(f"ds{i} Value")
    axes[i].grid(True)
    axes[i].legend(loc='upper right', fontsize=8)

axes[-1].set_xlabel("Time [s]")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(plots_dir, "Distance_Sensors_Raw_vs_Filtered.png"))
plt.show()

# -----------------------------
# 2. Light Sensors: Each sensor in a subplot
# -----------------------------
fig, axes = plt.subplots(8, 1, figsize=(12, 20), sharex=True)
fig.suptitle("Raw vs Filtered Light Sensors", fontsize=16)

for i in range(8):
    axes[i].plot(time, df[f'ls{i}'], label=f'ls{i} raw', linestyle='--', color='green')
    axes[i].plot(time, df[f'ls_f{i}'], label=f'ls{i} filtered', color='orange')
    axes[i].set_ylabel(f"ls{i} Value")
    axes[i].grid(True)
    axes[i].legend(loc='upper right', fontsize=8)

axes[-1].set_xlabel("Time [s]")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(plots_dir, "Light_Sensors_Raw_vs_Filtered.png"))
plt.show()

# -----------------------------
# 3. Motor Velocities Over Time
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(time, df['phil'], label='Left Wheel (phil)')
plt.plot(time, df['phir'], label='Right Wheel (phir)')
plt.xlabel("Time [s]")
plt.ylabel("Wheel Velocity [rad/s]")
plt.title("Motor Velocities Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "Motor_Velocities.png"))
plt.show()

# -----------------------------
# 4. Heatmap of Filtered Distance Sensors
# -----------------------------
ds_filtered = df[[f'ds_f{i}' for i in range(8)]]
plt.figure(figsize=(12, 6))
sns.heatmap(ds_filtered.T, cmap='viridis', cbar_kws={'label': 'Distance Value'})
plt.xlabel("Time Step Index")
plt.ylabel("Distance Sensor Index")
plt.title("Filtered Distance Sensors Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "Filtered_Distance_Sensors_Heatmap.png"))
plt.show()

# -----------------------------
# 5. Noise Reduction Comparison
# -----------------------------
std_raw = df[[f'ds{i}' for i in range(8)]].std(axis=1)
std_filtered = df[[f'ds_f{i}' for i in range(8)]].std(axis=1)

plt.figure(figsize=(10, 5))
plt.plot(time, std_raw, label='Raw Sensor STD', linestyle='--')
plt.plot(time, std_filtered, label='Filtered Sensor STD')
plt.xlabel("Time [s]")
plt.ylabel("Standard Deviation across sensors")
plt.title("Noise Reduction: Raw vs Filtered Sensors")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "Sensor_Noise_Reduction.png"))
plt.show()

# -----------------------------
# 6. DS3 and DS4 Comparison
# -----------------------------
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
fig.suptitle("Distance Sensors ds3 and ds4: Raw vs Filtered", fontsize=16)

# DS3
axes[0].plot(time, df['ds3'], label='ds3 raw', linestyle='--', color='blue')
axes[0].plot(time, df['ds_f3'], label='ds3 filtered', color='red')
axes[0].set_ylabel("ds3 Value")
axes[0].grid(True)
axes[0].legend(loc='upper right')

# DS4
axes[1].plot(time, df['ds4'], label='ds4 raw', linestyle='--', color='blue')
axes[1].plot(time, df['ds_f4'], label='ds4 filtered', color='red')
axes[1].set_ylabel("ds4 Value")
axes[1].set_xlabel("Time [s]")
axes[1].grid(True)
axes[1].legend(loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(plots_dir, "DS3_DS4_Comparison.png"))
plt.show()
