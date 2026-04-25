import cv2
import mediapipe as mp
import face_recognition
import numpy as np

print(cv2.__version__)

# Initialize the face detection using Mediapipe
Width = 640
Height = 360
FPS = 30
output_video_path = r'D:\AI_Course\DemoImages\output_video5.mp4'  # Specify output video path

video_path = r'D:\AI_Course\DemoImages\DT2.mov'

# Try to capture video from the specified path
try:
    cam = cv2.VideoCapture(video_path)
    # Get video properties
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cam.get(cv2.CAP_PROP_FPS)
    if not cam.isOpened():
        raise ValueError("Error: Unable to open video file.")
except Exception as e:
    print(f"Error opening video: {e}")
    exit(1)

findFace = mp.solutions.face_detection.FaceDetection()
drawFace = mp.solutions.drawing_utils

# Load known face encodings and names
known_face_encodings = []
known_face_names = []

# Load sample images and create face encodings
known_images = [
    'D:/AI_Course/DemoImages/known/Anthony Fauci.jpg',
    'D:\AI_Course\DemoImages\known\Donald Trump.jpg',
    'D:/AI_Course/DemoImages/known/Shahmir.jpg',
    'D:/AI_Course/DemoImages/known/Qayoom.png',
    'D:/AI_Course/DemoImages/known/IK.jpg'
]
known_names = ['Anthony Fauci','Donald Trump', 'Shahmir', 'Qayoom','Imran Khan']

# Try to load known images and create face encodings
for img_path, name in zip(known_images, known_names):
    try:
        image = face_recognition.load_image_file(img_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
    except IndexError:
        print(f"Error: No face found in image {img_path}. Skipping this image.")
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for the output video
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

while True:
    try:
        ret, frame = cam.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Use MediaPipe for face detection
        results = findFace.process(frame_rgb)

        if results.detections:
            face_locations = []
            for detection in results.detections:
                ih, iw, _ = frame.shape
                bBoxCords = detection.location_data.relative_bounding_box
                xmin, ymin, w, h = int(bBoxCords.xmin * iw), int(bBoxCords.ymin * ih), \
                                   int(bBoxCords.width * iw), int(bBoxCords.height * ih)
                topLeft = (xmin, ymin)
                bottomRight = (xmin + w, ymin + h)

                # Add face location in top-left and bottom-right corner format for face recognition
                face_locations.append((ymin, xmin + w, ymin + h, xmin))

                cv2.rectangle(frame, topLeft, bottomRight, (255, 0, 0), 2)

            # Recognize faces using face_recognition
            if face_locations:
                face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown Person"

                    # Use the known face with the smallest distance if a match is found
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    # If the face is unknown, blur it
                    if name == "Unknown Person":
                        face_region = frame[top:bottom, left:right]
                        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)  # Apply Gaussian blur
                        frame[top:bottom, left:right] = blurred_face  # Replace the face with the blurred version

                    # Draw the label with the name above the face rectangle
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Show the processed frame
        cv2.imshow("My WEBcam", frame)
        cv2.moveWindow("My WEBcam", 0, 0)

        # Write the frame to the output video file
        out.write(frame)  # Save the current frame

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error during frame processing: {e}")

# Release resources
try:
    cam.release()
    out.release()  # Release the video writer
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Error releasing resources: {e}")
