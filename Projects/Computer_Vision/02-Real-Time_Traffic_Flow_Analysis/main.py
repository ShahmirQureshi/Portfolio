from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Load input video
video_path = r'D:\AI_Course\30DaycvChallenge\Day28\Video (3).mp4'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties for output
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the output video writer
output_path = r'D:\AI_Course\30DaycvChallenge\Day28\processed_video7.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Define the line position (horizontal line)
line_position = height // 2 + 100

# Initialize object trackers and counters
object_tracker = {}
counters = {"up": {"car": 0, "truck": 0, "bus": 0, "motorcycle": 0},
            "down": {"car": 0, "truck": 0, "bus": 0, "motorcycle": 0}}

# Vehicle class IDs based on COCO dataset
vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# Function to calculate center of a bounding box
def calculate_center(box):
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

ret = True
while ret:
    ret, frame = cap.read()

    if ret:
        # Detect and track objects
        results = model.track(frame, persist=True, verbose=False)

        # Access detected objects
        detections = results[0].boxes if len(results) > 0 else []

        # Process each detected object
        for box in detections:
            coords = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
            label = box.cls[0].item()  # Object class index
            conf = box.conf[0].item()  # Confidence score
            center = calculate_center(coords)  # Calculate center point

            # Only process vehicle classes
            if label in vehicle_classes:
                # Update object tracker
                obj_id = box.id[0].item()  # Unique object ID from tracking
                if obj_id not in object_tracker:
                    object_tracker[obj_id] = {"center": center, "label": label}
                else:
                    prev_center = object_tracker[obj_id]["center"]

                    # Determine movement direction
                    if prev_center[1] <= line_position and center[1] > line_position:
                        # Object moved down
                        object_type = model.names[int(label)]
                        counters["down"][object_type] += 1
                    elif prev_center[1] > line_position and center[1] <= line_position:
                        # Object moved up
                        object_type = model.names[int(label)]
                        counters["up"][object_type] += 1

                    # Update the tracked center
                    object_tracker[obj_id]["center"] = center

                # Draw bounding box and center point
                x1, y1, x2, y2 = map(int, coords)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # Draw the line
        cv2.line(frame, (0, line_position), (width, line_position), (0, 255, 255), 3)

        # Draw the white rectangle for displaying the counts
        box_width = 400
        box_height = 150
        cv2.rectangle(frame, (10, 10), (10 + box_width, 10 + box_height), (255, 255, 255), -1)

        # Display counts inside the box
        y_offset = 50
        cv2.putText(frame, "UP", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        y_offset += 40
        for obj_type, count in counters["up"].items():
            text = f"{obj_type}: {count}"
            cv2.putText(frame, text, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            y_offset += 20

        y_offset = 50
        cv2.putText(frame, "DOWN", (box_width // 2 + 20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        y_offset += 40
        for obj_type, count in counters["down"].items():
            text = f"{obj_type}: {count}"
            cv2.putText(frame, text, (box_width // 2 + 20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            y_offset += 20

        # Write the processed frame to the output video
        out.write(frame)

        # Visualize the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()