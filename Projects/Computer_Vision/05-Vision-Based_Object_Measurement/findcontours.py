import cv2
import numpy as np

def find_minimum_rotated_rectangle(image, lower_bound=(40, 40, 40), upper_bound=(80, 255, 255)):
    """
    Finds the minimum rotated rectangle around the largest green object in the image.

    Args:
        image (ndarray): Input BGR image.
        lower_bound (tuple): Lower HSV bound for green color (default: (40, 40, 40)).
        upper_bound (tuple): Upper HSV bound for green color (default: (80, 255, 255)).

    Returns:
        rotated_rect (tuple): Box points of the minimum rotated rectangle.
        output_image (ndarray): Image with the minimum rotated rectangle drawn.
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
    if rotated_rect is not None:
        cv2.drawContours(output_image, [rotated_rect], 0, (0, 255, 0), 2)

    return rotated_rect, output_image, mask


img_path = r"D:\AI_Course\30DaycvChallenge\Day24\Test1.jpeg"
# Load the input image
image = cv2.imread(img_path)

# Define HSV bounds for green color
lower_green = (40, 40, 40)  # Adjust these values for your specific shade of green
upper_green = (80, 255, 255)

# Find the minimum rotated rectangle
rotated_rect, output_image, mask = find_minimum_rotated_rectangle(image, lower_green, upper_green)

# Display results
if rotated_rect is not None:
    print("Rotated Rectangle Points:", rotated_rect)  # Prints the four corner points
else:
    print("No green object detected.")

cv2.imshow("Original Image with Rotated Rectangle", output_image)
cv2.imshow("Green Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()