import cv2
import numpy as np
from ultralytics import YOLO
import utlis

scale = 3
wP = 440 * scale
hP = 300 * scale
def reorder_points(points):
    # Ensure points are in the order: top-left, top-right, bottom-right, bottom-left
    points = sorted(points, key=lambda x: x[0])  # Sort by x-coordinates
    left = sorted(points[:2], key=lambda x: x[1])  # Sort the left-most points by y-coordinates
    right = sorted(points[2:], key=lambda x: x[1])  # Sort the right-most points by y-coordinates
    return np.array([left[0], right[0], right[1], left[1]])



def find_and_draw_contours(binary_image, original_image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE):
    """
    Finds and draws contours on the original image and retrieves the corner points of each object.
    """
    contours, _ = cv2.findContours(binary_image, mode, method)
    annotated_image = original_image.copy()
    all_corner_points = []

    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        ordered_points = utlis.reorder(box)

        # Calculate dimensions
        nW = round((utlis.findDis(ordered_points[1] // scale, ordered_points[0] // scale) / 10), 1)
        nH = round((utlis.findDis(ordered_points[0] // scale, ordered_points[2] // scale) / 10), 1)

        all_corner_points.append(box.tolist())
        cv2.drawContours(annotated_image, [box], 0, (0, 255, 0), 2)

        dimensions_text = f"W: {nW}cm, H: {nH}cm"
        text_position = (int(rect[0][0]), int(rect[0][1] + 20))
        cv2.putText(annotated_image, dimensions_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)

    return all_corner_points, annotated_image


def segment_image_and_draw(model, frame, resize_dims=None):
    """
    Segments a frame using YOLO and draws contours on detected masks.
    """
    original_dims = frame.shape[:2]
    if resize_dims:
        frame = cv2.resize(frame, resize_dims)

    results = model.predict(frame, task='segment')

    if results:
        result = results[0]
        if result.masks is None:
            return frame

        masks = result.masks.data.cpu().numpy()
        composite_mask = np.zeros_like(masks[0], dtype=np.uint8)

        for mask in masks:
            composite_mask = np.maximum(composite_mask, mask)

        binary_mask = (composite_mask * 255).astype(np.uint8)
        binary_mask_resized = cv2.resize(binary_mask, (original_dims[1], original_dims[0]))

        _, processed_frame = find_and_draw_contours(binary_mask_resized, frame)
        return processed_frame

    return frame

def warp_rotated_rectangle(image, lower_bound=(40, 40, 40), upper_bound=(80, 255, 255), resize_dim=(500, 500)):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    rotated_rect = None

    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        area = cv2.contourArea(box)

        if area > largest_area:
            largest_area = area
            rotated_rect = box

    warped_image = None
    if rotated_rect is not None:
        rotated_rect = reorder_points(rotated_rect)
        side_lengths = [
            np.linalg.norm(rotated_rect[0] - rotated_rect[1]),
            np.linalg.norm(rotated_rect[1] - rotated_rect[2]),
            np.linalg.norm(rotated_rect[2] - rotated_rect[3]),
            np.linalg.norm(rotated_rect[3] - rotated_rect[0])
        ]
        width, height = sorted(side_lengths)[-2:]  # Always use the longer side as width

        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        rect_pts = rotated_rect.astype("float32")
        M = cv2.getPerspectiveTransform(rect_pts, dst_pts)
        warped_image = cv2.warpPerspective(image, M, (int(width), int(height)))
        warped_image = cv2.resize(warped_image, resize_dim)

    return warped_image, mask



def process_video(video_path, output_path, model_path, lower_green=(40, 40, 40), upper_green=(80, 255, 255)):
    """
    Processes a video frame-by-frame, applying YOLO segmentation, contour detection,
    and saving the processed frames to a new video file.
    """
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video properties - FPS: {fps}, Width: {frame_width}, Height: {frame_height}")

    # Initialize VideoWriter
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        print(f"Failed to initialize VideoWriter. Check the output path or codec.")
        return

    # Load the YOLO model
    model = YOLO(model_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        # Warp the rotated rectangle
        warped_frame, _ = warp_rotated_rectangle(frame, lower_green, upper_green, resize_dim=(wP, hP))

        if warped_frame is not None:
            # Apply YOLO segmentation and contour detection
            processed_frame = segment_image_and_draw(model, warped_frame)
        else:
            processed_frame = frame

        # Ensure processed_frame matches VideoWriter dimensions
        if processed_frame.shape[:2] != (frame_height, frame_width):
            processed_frame = cv2.resize(processed_frame, (frame_width, frame_height))

        # Write the processed frame
        out.write(processed_frame)

        cv2.imshow('Processed Frame', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Check if file is created
    if not cv2.os.path.exists(output_path):
        print(f"Output file was not created at: {output_path}")
    else:
        print(f"Video saved successfully at: {output_path}")


# Paths and configuration
video_input_path = r"D:\AI_Course\30DaycvChallenge\Day24\Test3.mp4"
video_output_path = r"D:\AI_Course\30DaycvChallenge\Day24\output_video6.mp4"
model_path = "yolo11n-seg.pt"  # Replace with your model path

# Process the video
process_video(video_input_path, video_output_path, model_path)
