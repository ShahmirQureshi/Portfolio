from controller import Robot
import numpy as np
import csv

# ---------- Constants ----------
TIME_STEP = 32
MAX_SPEED = 6.28
FILTER_SAMPLES = 5     # for moving average
USE_EMA = False        # set True to use Exponential Moving Average
EMA_ALPHA = 0.5        # smoothing factor for EMA

# ---------- Initialize Robot ----------
robot = Robot()

# ---------- Motors ----------
motor_left = robot.getDevice('left wheel motor')
motor_right = robot.getDevice('right wheel motor')

motor_left.setPosition(float('inf'))   # Infinite rotation
motor_right.setPosition(float('inf'))

motor_left.setVelocity(0.0)
motor_right.setVelocity(0.0)

# ---------- Distance Sensors (for obstacle detection) ----------
ds = []
for i in range(8):
    sensor = robot.getDevice('ps' + str(i))
    sensor.enable(TIME_STEP)
    ds.append(sensor)

# ---------- Light Sensors (for optional light-based behavior) ----------
ls = []
for i in range(8):
    sensor = robot.getDevice('ls' + str(i))
    sensor.enable(TIME_STEP)
    ls.append(sensor)

print("All sensors are enabled!")

# ---------- Initialize Buffers for Moving Average ----------
ds_buffer = [np.zeros(8) for _ in range(FILTER_SAMPLES)]
ls_buffer = [np.zeros(8) for _ in range(FILTER_SAMPLES)]

# ---------- Initialize EMA ----------
ds_ema = np.zeros(8)
ls_ema = np.zeros(8)

# ---------- CSV Logging ----------
log_file = open("sensor_log.csv", "w", newline="")
csv_writer = csv.writer(log_file)
header = ["time"] + [f"ds{i}" for i in range(8)] + [f"ls{i}" for i in range(8)] + \
         [f"ds_f{i}" for i in range(8)] + [f"ls_f{i}" for i in range(8)] + ["phil", "phir"]
csv_writer.writerow(header)

# ---------- Main Loop ----------
while robot.step(TIME_STEP) != -1:
    t = robot.getTime()

    # --- Read distance sensors (for obstacle avoidance) ---
    d_raw = np.array([sensor.getValue() for sensor in ds])
    d_scaled = d_raw / 1000.0 * 3.14  # example scaling

    # --- Read light sensors (optional behavior) ---
    l_raw = np.array([sensor.getValue() for sensor in ls])
    l_scaled = l_raw / 5000.0 * 3.14  # example scaling

    # --- Apply Filtering ---
    if USE_EMA:
        # Exponential Moving Average
        ds_ema = EMA_ALPHA * d_scaled + (1 - EMA_ALPHA) * ds_ema
        ls_ema = EMA_ALPHA * l_scaled + (1 - EMA_ALPHA) * ls_ema
        d_filtered = ds_ema
        l_filtered = ls_ema
    else:
        # Moving Average
        ds_buffer.pop(0)
        ds_buffer.append(d_scaled)
        d_filtered = np.mean(ds_buffer, axis=0)

        ls_buffer.pop(0)
        ls_buffer.append(l_scaled)
        l_filtered = np.mean(ls_buffer, axis=0)

    # --- Compute motor velocities (Reactive Obstacle Avoidance) ---
    # Using distance sensors only for obstacle avoidance
    phil = 3.14 - d_filtered[0] - d_filtered[1] - d_filtered[2]
    phir = 3.14 - d_filtered[7] - d_filtered[6] - d_filtered[5]

    # Optional: Add light-based influence if desired
    phil += l_filtered[7]
    phir += l_filtered[0]

    # --- Limit speeds to MAX_SPEED ---
    phil = max(min(phil, MAX_SPEED), -MAX_SPEED)
    phir = max(min(phir, MAX_SPEED), -MAX_SPEED)

    # --- Set motor velocities ---
    motor_left.setVelocity(phil)
    motor_right.setVelocity(phir)

    # --- Logging for analysis ---
    row = [t] + list(d_scaled) + list(l_scaled) + list(d_filtered) + list(l_filtered) + [phil, phir]
    csv_writer.writerow(row)

    # --- Optional: Print for debugging ---
    print(f"t={t:.2f} | phil={phil:.2f} phir={phir:.2f} | d0={d_filtered[0]:.2f} d7={d_filtered[7]:.2f}")

# ---------- Cleanup ----------
log_file.close()
motor_left.setVelocity(0.0)
motor_right.setVelocity(0.0)
print("Simulation finished and log saved.")
