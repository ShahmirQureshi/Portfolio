import cv2
from ultralytics import YOLO
from Arduino import ArduinoController

def detect_and_show_video(model, arduino, imgsz=640, conf=0.5, iou=0.4, no_detection_threshold=60, detection_frames=10, width=640, height=480):
    """
    Perform object detection using the webcam and send a command to the Arduino when detection occurs.
    Sends a "Stop" command if no detection happens for `no_detection_threshold` frames after a "Fire" command.
    Sends a "Fire" command only after detection persists for `detection_frames` frames.

    Args:
        model: YOLO model for object detection.
        arduino: ArduinoController instance to send data to Arduino.
        imgsz (int): Size to resize frames for YOLO model.
        conf (float): Confidence threshold for valid detections.
        iou (float): IoU threshold for Non-Maximum Suppression (NMS).
        no_detection_threshold (int): Number of frames without detection to trigger "Stop" command.
        detection_frames (int): Number of consecutive frames with detection to trigger "Fire" command.
        width (int): Width of the captured video frame.
        height (int): Height of the captured video frame.
    """

    # Open the webcam (0 is usually the default camera on most systems)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    # Set the frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # Set frame width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # Set frame height

    frame_counter = 0  # Initialize frame counter to track frames without detection
    fire_sent = False  # Flag to check if "Fire" has been sent
    detection_counter = 0  # Counter for consecutive detections

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection with confidence and IoU thresholds
        results = model(source=frame, imgsz=imgsz, conf=conf, iou=iou)
        processed_frame = results[0].plot()  # Overlay detections on the frame

        # Check if detections are made
        if results[0].boxes is not None and len(results[0].boxes) > 0:
            # Increment the detection counter for consecutive detections
            detection_counter += 1

            # Send command to Arduino to "Fire" when detection persists for the defined number of frames
            if detection_counter >= detection_frames and not fire_sent:
                arduino.send_data('Fire')
                fire_sent = True  # Mark "Fire" as sent

            frame_counter = 0  # Reset the frame counter if detection is made
        else:
            # Increment the frame counter if no detection
            frame_counter += 1

            # Reset detection counter when no object is detected
            detection_counter = 0

            # Send "Stop" command only after 60 frames without detection and after "Fire" was sent
            if fire_sent and frame_counter >= no_detection_threshold:
                arduino.send_data('Stop')
                fire_sent = False  # Reset the flag after sending "Stop"
                frame_counter = 0  # Reset the counter after sending "Stop"

        # Display the processed frame
        cv2.imshow("Detected Frame", processed_frame)
        cv2.moveWindow("Detected Frame",0,0)

        # Press 'q' to quit the webcam window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close the window
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam detection finished.")

# Example usage
model_path = r'D:\AI_Course\30DaycvChallenge\Day21\best.pt'  # Set the correct path for your model
model = YOLO(model_path)

# Initialize the Arduino controller
arduino = ArduinoController(port='COM3', baud_rate=9600)  # Adjust the port if necessary

# Run the detection and communication with Arduino
detect_and_show_video(model, arduino, conf=0.4, iou=0.3, no_detection_threshold=5, detection_frames=5, width=1280, height=640)

# Close the Arduino connection after the program finishes
arduino.close()
