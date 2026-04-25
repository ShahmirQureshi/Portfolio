import cv2
import numpy as np
from ultralytics import YOLO
import utlis

scale = 3
wP = 440 *scale
hP= 300 *scale


def find_and_draw_contours(binary_image, original_image, output_path, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE, draw=True):
    """
    Finds and optionally draws contours on the original image and retrieves the corner points of each object.

    Args:
        binary_image (ndarray): Binary image with objects.
        original_image (ndarray): The original image where contours will be drawn.
        output_path (str): Path to save the image with drawn contours and dimensions.
        mode (int): Contour retrieval mode (default: cv2.RETR_EXTERNAL).
        method (int): Contour approximation method (default: cv2.CHAIN_APPROX_SIMPLE).
        draw (bool): Whether to draw contours on the image (default: True).

    Returns:
        corner_points (list): List of corner points for each object.
    """
    # Find contours
    contours, _ = cv2.findContours(binary_image, mode, method)

    # To store all corner points
    all_corner_points = []

    if draw:
        # Work directly on the original image (a copy is recommended to avoid modifying the original data)
        annotated_image = original_image.copy()

        # Object counter
        object_count = 1

        for contour in contours:
            # Fit a rotated rectangle around the contour
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)  # Get the box points (float coordinates)
            box = np.intp(box)  # Convert to integer
            # Reorder the points
            ordered_points = utlis.reorder(box)

            # Calculate width and height
            nW = round((utlis.findDis(ordered_points[1]//scale, ordered_points[0]//scale) / 10), 1)
            nH = round((utlis.findDis(ordered_points[0]//scale, ordered_points[2]//scale) / 10), 1)

            # Append corner points
            all_corner_points.append(box.tolist())  # Convert to a Python list

            # Draw the rotated rectangle
            cv2.drawContours(annotated_image, [box], 0, (0, 255, 0), 2)

            # Label the object with its number
            object_label = f"Object {object_count}"
            cv2.putText(annotated_image, object_label, tuple(box[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Display width and height near the object
            dimensions_text = f"W: {nW}cm, H: {nH}cm"
            text_position = (int(rect[0][0]), int(rect[0][1] + 20))  # Position below the rectangle
            cv2.putText(annotated_image, dimensions_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            # Increment object count
            object_count += 1

        # Save the image with drawn contours and dimensions
        cv2.imwrite(output_path, annotated_image)

    return all_corner_points
def segment_image_and_draw(model_path, image, output_path, resize_dims=None):
    """
    Segments an image using a YOLO model, draws contours, and saves the result.

    Args:
        model_path (str): Path to the YOLO model.
        image (ndarray): Input image as a NumPy array.
        output_path (str): Path to save the result.
        resize_dims (tuple): Dimensions to resize the image to before segmentation (width, height).

    Returns:
        None
    """
    # Get original image dimensions
    original_width, original_height = image.shape[:2]

    # Optionally resize the image
    if resize_dims:
        image = cv2.resize(image, resize_dims)
    else:
        # Use original dimensions as resize dimensions
        resize_dims = (original_width, original_height)

    # Load the YOLO model
    model = YOLO(model_path)

    # Run the YOLO model for segmentation
    results = model.predict(image, task='segment')

    if results:
        result = results[0]  # Access the first result
        if result.masks is None:
            print("No masks were detected in the image.")
            return  # Exit early if no masks were found
        
        masks = result.masks.data.cpu().numpy()  # Convert masks to numpy array on CPU
        
        # Create a composite mask
        composite_mask = np.zeros_like(masks[0], dtype=np.uint8)
        for mask in masks:
            composite_mask = np.maximum(composite_mask, mask)  # Combine masks using max
        
        # Normalize the mask to be in the range [0, 255] for visualization
        binary_mask = (composite_mask * 255).astype(np.uint8)

        # Resize the mask back to the original image dimensions
        print("width = ", resize_dims[1] // scale, "Height = ", resize_dims[0] // scale)
        binary_mask_resized = cv2.resize(binary_mask, (resize_dims[1], resize_dims[0]))
        
        cv2.imshow("mask", binary_mask_resized)

        # Draw contours and calculate dimensions
        all_contours = find_and_draw_contours(binary_mask_resized, image, output_path)
        # pointsx = ((points[0][1][0] - points[0][0][0]) ** 2 + (points[0][1][1] - points[0][0][1])) ** 0.5
        # nW = round((utlis.findDis(ordered_points[1]//scale,ordered_points[0]//scale)/10),1)
        # nH = round((utlis.findDis(ordered_points[0]//scale,ordered_points[2]//scale)/10),1)
        #     # nH = 0
        # print ("nWF = ",nW,"nHF = ",nH)
        
        # print(pointsx)
    else:
        print("No segmentation results were found.")


def warp_rotated_rectangle(image, lower_bound=(40, 40, 40), upper_bound=(80, 255, 255), resize_dim=(500, 500)):
    """
    Finds the minimum rotated rectangle around the largest green object, 
    warps the area under the rectangle in the original image, and resizes it.

    Args:
        image (ndarray): Input BGR image.
        lower_bound (tuple): Lower HSV bound for green color (default: (40, 40, 40)).
        upper_bound (tuple): Upper HSV bound for green color (default: (80, 255, 255)).
        resize_dim (tuple): Desired dimensions to resize the warped image (default: (500, 500)).

    Returns:
        warped_image (ndarray): Perspective-warped and resized image of the rectangle area.
        output_image (ndarray): Original image with the rectangle drawn.
        mask (ndarray): Mask of the green color.
    """
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for green color
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to track the largest rotated rectangle
    largest_area = 0
    rotated_rect = None

    # Iterate through contours
    for contour in contours:
        # Get the minimum area rectangle for each contour
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)  # Get the 4 corner points of the rectangle
        box = np.int0(box)

        # Calculate the area of the rectangle
        area = cv2.contourArea(box)

        # Update the largest rectangle if the current one is bigger
        if area > largest_area:
            largest_area = area
            rotated_rect = box

    # Draw the largest rotated rectangle on the original image
    output_image = image.copy()
    warped_image = None
    if rotated_rect is not None:
        cv2.drawContours(output_image, [rotated_rect], 0, (0, 255, 0), 2)

        # Define the destination points for the warped rectangle
        width = int(max(
            np.linalg.norm(rotated_rect[0] - rotated_rect[1]),
            np.linalg.norm(rotated_rect[2] - rotated_rect[3])
        ))
        height = int(max(
            np.linalg.norm(rotated_rect[1] - rotated_rect[2]),
            np.linalg.norm(rotated_rect[3] - rotated_rect[0])
        ))

        # Destination points for the perspective transform
        dst_pts = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")

        # Get the perspective transform matrix
        rect_pts = rotated_rect.astype("float32")
        M = cv2.getPerspectiveTransform(rect_pts, dst_pts)

        # Perform the perspective warp
        warped_image = cv2.warpPerspective(image, M, (width, height))

        # Resize the warped image
        warped_image = cv2.resize(warped_image, resize_dim)

    return warped_image, output_image, mask

img_path = r"D:\AI_Course\30DaycvChallenge\Day24\Test4.jpeg"
model_path = "yolo11n-seg.pt"  # Replace with your model path
output_path = r"D:\AI_Course\30DaycvChallenge\Day24\output_image_with_contours5.jpeg"
# Load the input image
image = cv2.imread(img_path)

# Define HSV bounds for green color
lower_green = (40, 40, 40)  # Adjust these values for your specific shade of green
upper_green = (80, 255, 255)

# Desired dimensions for resized warped image
resize_dim = (wP, hP)  # Example dimensions (width, height)

# Warp and resize the perspective of the rotated rectangle
warped_image, output_image, mask = warp_rotated_rectangle(image, lower_green, upper_green, resize_dim)

# Display results
if warped_image is not None:
    cv2.imshow("Warped Resized Rectangle", warped_image)
    segment_image_and_draw(model_path, warped_image, output_path)
else:
    print("No green object detected.")

cv2.imshow("Original Image with Rotated Rectangle", output_image)
cv2.imshow("Green Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()