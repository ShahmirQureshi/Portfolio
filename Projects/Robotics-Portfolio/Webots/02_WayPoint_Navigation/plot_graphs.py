import os
import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = r"C:\Users\20MTE034\Desktop\Webot_Course\WayPoint_Navigation\controllers\Odometry_Based_Waypoint_Navigation\waypoint_log.csv"

# Read the CSV, detect the separator (assuming it's tab-separated)
df = pd.read_csv(file_path, sep=None, engine='python')

# Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Check the column names to confirm 'time' is now available
print("Columns in the DataFrame:", df.columns.tolist())

# Convert 'time' column to float (if needed)
df['time'] = df['time'].astype(float)

# Create a root plot folder
plot_root_folder = r"C:\Users\20MTE034\Desktop\Webot_Course\WayPoint_Navigation\controllers\Odometry_Based_Waypoint_Navigation\plots"
os.makedirs(plot_root_folder, exist_ok=True)  # This creates the folder if it doesn't exist

# Function to save plots
def save_plot(figure, plot_name):
    # Save the figure as an image directly in the 'plots' folder
    plot_path = os.path.join(plot_root_folder, f"{plot_name}.png")
    figure.savefig(plot_path)
    print(f"Plot saved at: {plot_path}")

# 1. Robot path vs waypoint
fig1 = plt.figure(figsize=(8, 6))
plt.plot(df['x'], df['y'], label='Robot Path', marker='o')
plt.scatter(df['wp_x'], df['wp_y'], color='red', label='Waypoint', s=100)
plt.xlabel('X position')
plt.ylabel('Y position')
plt.title('Robot Path vs Waypoint')
plt.legend()
plt.grid(True)
save_plot(fig1, 'Robot_Path_vs_Waypoint')  # Save this plot

# 2. Distance to waypoint over time
fig2 = plt.figure(figsize=(8, 6))
plt.plot(df['time'], df['distance'], color='green', marker='o')
plt.xlabel('Time [s]')
plt.ylabel('Distance to Waypoint')
plt.title('Distance to Waypoint over Time')
plt.grid(True)
save_plot(fig2, 'Distance_to_Waypoint_Over_Time')  # Save this plot

# 3. X and Y position over time
fig3 = plt.figure(figsize=(8, 6))
plt.plot(df['time'], df['x'], label='X Position', marker='o')
plt.plot(df['time'], df['y'], label='Y Position', marker='x')
plt.xlabel('Time [s]')
plt.ylabel('Position')
plt.title('X and Y Positions over Time')
plt.legend()
plt.grid(True)
save_plot(fig3, 'X_and_Y_Position_Over_Time')  # Save this plot

# 4. Theta over time
fig4 = plt.figure(figsize=(8, 6))
plt.plot(df['time'], df['theta'], color='purple', marker='o')
plt.xlabel('Time [s]')
plt.ylabel('Theta [rad]')
plt.title('Orientation (Theta) over Time')
plt.grid(True)
save_plot(fig4, 'Orientation_Theta_Over_Time')  # Save this plot

# 5. State over time
fig5 = plt.figure(figsize=(8, 4))
plt.plot(df['time'], df['state'], drawstyle='steps-post', color='orange')
plt.xlabel('Time [s]')
plt.ylabel('State')
plt.title('Robot State over Time')
plt.grid(True)
save_plot(fig5, 'Robot_State_Over_Time')  # Save this plot
