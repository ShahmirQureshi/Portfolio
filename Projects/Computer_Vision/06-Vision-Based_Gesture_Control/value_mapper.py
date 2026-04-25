import math

def map_value(x,x_min=50, x_max=300):
    # Input range
    # x_min = 50
    # x_max = 300
    
    # Output range
    y_min = 0.0
    y_max = 1

    # Output range
    y_min = 0.0
    y_max = 180
    
    # Clamp x to the range [x_min, x_max]
    x = max(x_min, min(x_max, x))
    
    # Calculate mapped value
    if x < x_min:
        y = 0.0
    elif x > x_max:
        y = 1.0
    else:
        y = y_min + (y_max - y_min) * (x - x_min) / (x_max - x_min)
    
    return y

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
