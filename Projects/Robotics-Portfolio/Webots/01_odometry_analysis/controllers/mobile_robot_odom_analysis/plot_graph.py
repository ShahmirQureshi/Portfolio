import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# Load CSV
# =========================
data = pd.read_csv(r"C:\Users\20MTE034\Desktop\Webot_Course\odometry_analysis\controllers\mobile_robot_odom_analysis\odom_log_Line_Following.csv")

# Create output directory
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# Get unique motion modes
modes = data["mode"].unique()

print("Detected modes:", modes)

# =========================
# Loop over each mode
# =========================
for mode in modes:
    subset = data[data["mode"] == mode]

    # -------------------------
    # (1) Trajectory: x vs y
    # -------------------------
    plt.figure()
    plt.plot(subset["x"], subset["y"])
    plt.xlabel("x position (m)")
    plt.ylabel("y position (m)")
    plt.title(f"Odometry Trajectory – {mode}")
    plt.axis("equal")
    plt.grid(True)
    plt.savefig(f"{output_dir}/trajectory_{mode}.png", dpi=300)
    plt.close()

    # -------------------------
    # (2) Error vs Time
    # -------------------------
    plt.figure()
    plt.plot(subset["time"], subset["error"])
    plt.xlabel("Time (s)")
    plt.ylabel("Position Error (m)")
    plt.title(f"Odometry Error vs Time – {mode}")
    plt.grid(True)
    plt.savefig(f"{output_dir}/error_vs_time_{mode}.png", dpi=300)
    plt.close()

    # -------------------------
    # (3) Heading vs Time
    # -------------------------
    plt.figure()
    plt.plot(subset["time"], subset["theta"])
    plt.xlabel("Time (s)")
    plt.ylabel("Heading (rad)")
    plt.title(f"Heading vs Time – {mode}")
    plt.grid(True)
    plt.savefig(f"{output_dir}/heading_vs_time_{mode}.png", dpi=300)
    plt.close()

print("All plots saved in the 'plots/' directory.")


# import os
# import matplotlib.pyplot as plt
# from PIL import Image

# # =========================
# # Path to your plots folder
# # =========================
# PLOTS_DIR = r"C:\Users\20MTE034\Desktop\Webot_Course\odometry_analysis\controllers\mobile_robot_odom_analysis\plots"

# # Output directory
# OUTPUT_DIR = os.path.join(PLOTS_DIR, "collages")
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # =========================
# # Helper function
# # =========================
# def make_collage(image_files, title, output_name):
#     images = [Image.open(f) for f in image_files]

#     fig, axes = plt.subplots(2, 2, figsize=(10, 10))
#     fig.suptitle(title, fontsize=16)

#     for ax, img, fname in zip(axes.flatten(), images, image_files):
#         ax.imshow(img)
#         ax.axis("off")
#         ax.set_title(os.path.basename(fname).replace(".png", ""), fontsize=10)

#     plt.tight_layout(rect=[0, 0, 1, 0.95])
#     plt.savefig(os.path.join(OUTPUT_DIR, output_name), dpi=300)
#     plt.close()

# # =========================
# # Collect images
# # =========================
# trajectory_imgs = sorted([
#     os.path.join(PLOTS_DIR, f)
#     for f in os.listdir(PLOTS_DIR)
#     if f.startswith("trajectory_") and f.endswith(".png")
# ])

# error_imgs = sorted([
#     os.path.join(PLOTS_DIR, f)
#     for f in os.listdir(PLOTS_DIR)
#     if f.startswith("error_vs_time_") and f.endswith(".png")
# ])

# heading_imgs = sorted([
#     os.path.join(PLOTS_DIR, f)
#     for f in os.listdir(PLOTS_DIR)
#     if f.startswith("heading_vs_time_") and f.endswith(".png")
# ])

# # =========================
# # Generate collages
# # =========================
# make_collage(
#     trajectory_imgs,
#     "Odometry Trajectories (Mode-wise)",
#     "collage_trajectories.png"
# )

# make_collage(
#     error_imgs,
#     "Odometry Error vs Time (Mode-wise)",
#     "collage_error_vs_time.png"
# )

# make_collage(
#     heading_imgs,
#     "Heading vs Time (Mode-wise)",
#     "collage_heading_vs_time.png"
# )

# print("Collages created successfully in:", OUTPUT_DIR)
