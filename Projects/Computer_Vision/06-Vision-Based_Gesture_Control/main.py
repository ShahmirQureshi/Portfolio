import cv2
import numpy as np
import mediapipe as mp
from value_mapper import map_value
import serial
import time

class GestureAngleControl:
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    COLOR = (255, 0, 255)
    TEXT_COLOR = (255, 0, 0)
    CIRCLE_RADIUS = 25
    SMOOTHENING = 4  # Adjust smoothening factor (higher = smoother, slower)

    def __init__(self):
        try:
            # Initialize MediaPipe Hands
            self.hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.mp_draw = mp.solutions.drawing_utils
            self.width = 1280
            self.height = 720
            self.fps = 30

            try:
                self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1
                                             
                                             )  # Adjust COM port to match your Arduino's port
                time.sleep(2)  # Wait for Arduino to initialize
            except Exception as e:
                print(f"Error sending data to Arduino: {e}")    

            self.previous_value = 0
            self.lmList = []
            self.tipIds = [4, 8, 12, 16, 20]  # Landmarks for tips of thumb, index, middle, ring, and pinky fingers
            self.fingers = []
            self.Condition = False  # Initialize Condition to True
        except Exception as e:
            print(f"Error initializing GestureVolumeControl: {e}")
            exit()

    def send_angle_to_arduino(self, angle):
        try:
            angle_str = str(int(angle)) + '\n'  # Convert angle to string with newline
            self.arduino.write(angle_str.encode())  # Send the angle as bytes to Arduino
            print(f"Sent angle to Arduino: {angle_str}")
        except Exception as e:
            print(f"Error sending data to Arduino: {e}")

    def smoothen_value(self, current_value, target_value):
        # Smoothen the volume changes
        return current_value + (target_value - current_value) / self.SMOOTHENING

    def finger_status(self, lmList):
        """Checks which fingers are up and returns a list with 1 if up, 0 if down"""
        fingers = []

        # Thumb
        if lmList[self.tipIds[0]][0] > lmList[self.tipIds[0] - 1][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[self.tipIds[id]][1] < lmList[self.tipIds[id] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def process_frame(self, frame):
        try:
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                    # Extract landmarks and compute volume control gestures
                    my_hand = [(int(lm.x * self.width), int(lm.y * self.height)) for lm in hand_landmarks.landmark]
                    x1, y1 = my_hand[4]  # Thumb tip
                    x2, y2 = my_hand[8]  # Index finger tip
                    px1, py1 = my_hand[0]  # Palm base
                    px2, py2 = my_hand[9]  # Wrist middle

                    # Check the status of fingers
                    self.fingers = self.finger_status(my_hand)
                    # print(f"Fingers status: {self.fingers}")

                    # Check if the pinky finger (index 4 in tipIds) is up
                    if self.fingers[4] == 1 and self.fingers[3] == 0  and self.fingers[2] == 0:  # Pinky finger is up
                        self.Condition = True
                        cv2.putText(frame, str(self.Condition), (10, self.height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    if px1 > px2:
                        px1, px2 = px2, px1
                    if py1 > py2:
                        py1, py2 = py2, py1
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1

                    if x2 > x1 and y2 > y1:
                        palmsize=(((px2-px1)**2+(py2-py1)**2)**1/2)
                        dist = (((x2-x1)**2+(y2-y1)**2)**1/2)/palmsize
                        print(f"The distance between points is {dist}")

                        # Map distance to volume
                        mapped_value = map_value(dist, 0, 3)
                        print(f"Mapped Angle value: {mapped_value}")

                        # Smoothen volume changes
                        smoothened_value = self.smoothen_value(self.previous_value, mapped_value)
                        self.previous_value = smoothened_value  # Update the previous volume

                        # # Add some text
                        cv2.putText(frame, f"Angle is {round(smoothened_value,2)}", (10, self.height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                        try:
                            # Send the smoothened angle value to Arduino
                            self.send_angle_to_arduino(smoothened_value)
                        except Exception as e:
                            print(f"Error processing frame: {e}")

                        # Draw circles on key points
                    cv2.circle(frame, my_hand[4], self.CIRCLE_RADIUS, (255, 0, 255), -1)
                    cv2.circle(frame, my_hand[8], self.CIRCLE_RADIUS, (0, 255, 255), -1)
            
        except Exception as e:
            print(f"Error processing frame: {e}")

        return frame, self.Condition

def main():
    Width = 1280
    Height = 720
    FPS = 30

    try:
        # Initialize webcam
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cam.isOpened():
            print("Error: Could not open webcam.")
            exit()

        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
        cam.set(cv2.CAP_PROP_FPS, FPS)
        cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        print("Webcam initialized successfully")

        # Initialize GestureAngleControl
        gesture_angle_control = GestureAngleControl()

        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Process the frame for gesture and volume control
            frame, condition = gesture_angle_control.process_frame(frame)
            print(f"Condition: {condition}")

            # Display the frame with landmarks
            cv2.imshow("My Webcam", frame)
            cv2.moveWindow("My Webcam", 0, 0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error in main loop: {e}")

    finally:
        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()