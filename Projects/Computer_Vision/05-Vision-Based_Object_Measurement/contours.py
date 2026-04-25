import cv2
import utlis
scale = 3
def find_and_draw_contours(binary_image, output_path, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE, draw=True):
    """
    Finds and optionally draws contours on a binary image and retrieves the corner points of each object.

    Args:
        binary_image (ndarray): Binary image with objects.
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
        # Create a colored version of the binary image for visualization
        colored_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

        for contour in contours:
            # Fit a rotated rectangle around the contour
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)  # Get the box points (float coordinates)
            box = np.intp(box)  # Convert to integer
            # Reorder the points
            ordered_points = utlis.reorder(box)

            print("Original Points:")
            print(box)
            print("Reordered Points (Top-Left, Top-Right, Bottom-left, Bottom-right):")
            print(ordered_points)

            for i, point in enumerate(ordered_points):
                cv2.circle(colored_image, tuple(point), 5, (255, 0, 0), -1)  # Draw a circle at each point
                cv2.putText(colored_image, f"{i}", tuple(point), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                print(point)

            # scale = 3
            # for point in ordered_points:
            print("p1 = ",ordered_points)
                
            nW = round((utlis.findDis(ordered_points[1]//scale,ordered_points[0]//scale)/10),1)
            nH = round((utlis.findDis(ordered_points[0]//scale,ordered_points[2]//scale)/10),1)
            # nH = 0
            print ("nW = ",nW,"nH = ",nH)
            #     print("width = ",nW,"Height = ", nH)
                # cv2.arrowedLine(colored_image, (point[0][0][0], point[0][0][1]), (point[1][0][0], point[1][0][1]),
                #                     (255, 0, 255), 3, 8, 0, 0.05)
                # cv2.arrowedLine(colored_image, (ordered_points[0][0][0], ordered_points[0][0][1]), (ordered_points[2][0][0], ordered_points[2][0][1]),
                #                     (255, 0, 255), 3, 8, 0, 0.05)

            
            # Append corner points
            all_corner_points.append(box.tolist())  # Convert to a Python list

            # Draw the rotated rectangle
            cv2.drawContours(colored_image, [box], 0, (0, 255, 0), 2)

            # Extract width and height from the rectangle
            width, height = rect[1]

            # Display width and height on the image
            text = f"W:{int(width)} H:{int(height)}"
            text_position = (int(rect[0][0]), int(rect[0][1] - 10))  # Position above the rectangle
            cv2.putText(colored_image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the image with drawn contours and dimensions
        cv2.imwrite(output_path, colored_image)

    return all_corner_points, ordered_points
