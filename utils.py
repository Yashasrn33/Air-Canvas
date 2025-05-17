"""
utils.py - Utility functions for the Air Canvas application
"""

import os
import cv2
import numpy as np
from datetime import datetime
import config

def nothing(x):
    """Empty callback function for trackbars"""
    pass

def create_directories():
    """Create necessary directories for the application"""
    os.makedirs(config.SAVE_DIR, exist_ok=True)

def save_image(image, prefix="drawing"):
    """Save an image with timestamp in the filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(config.SAVE_DIR, f"{prefix}_{timestamp}.png")
    cv2.imwrite(filename, image)
    print(f"Image saved as {filename}")
    return filename

def get_contour_center(contour):
    """Calculate the center point of a contour"""
    if contour is not None:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
    return None

def smooth_points(points, window_size=5):
    """Apply smoothing to a list of points"""
    if len(points) < window_size:
        return points
    
    smoothed = []
    for i in range(len(points) - window_size + 1):
        window = points[i:i+window_size]
        x_avg = sum(p[0] for p in window) // window_size
        y_avg = sum(p[1] for p in window) // window_size
        smoothed.append((x_avg, y_avg))
    
    return smoothed

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def inside_rectangle(point, top_left, bottom_right):
    """Check if a point is inside a rectangle"""
    x, y = point
    x1, y1 = top_left
    x2, y2 = bottom_right
    
    return (x1 <= x <= x2) and (y1 <= y <= y2)

def draw_text_with_background(image, text, position, font=config.FONT, 
                             font_scale=config.FONT_SCALE, color=(0, 0, 0), 
                             thickness=config.FONT_THICKNESS, bg_color=(255, 255, 255)):
    """Draw text with a background rectangle for better visibility"""
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font, font_scale, thickness)
    
    # Calculate background rectangle coordinates
    x, y = position
    bg_tl = (x, y - text_height - baseline - 5)
    bg_br = (x + text_width + 10, y + 5)
    
    # Draw background rectangle
    cv2.rectangle(image, bg_tl, bg_br, bg_color, -1)
    
    # Draw text
    cv2.putText(image, text, (x + 5, y - baseline - 5), 
                font, font_scale, color, thickness, config.FONT_LINE_TYPE)

def create_button(image, position, size, text, color=(200, 200, 200), 
                 text_color=(0, 0, 0), selected=False, border_color=(0, 0, 0)):
    """Create a clickable button on the image"""
    x, y = position
    width, height = size
    
    # Draw button background
    cv2.rectangle(image, (x, y), (x + width, y + height), color, -1)
    
    # If selected, draw a border
    if selected:
        cv2.rectangle(image, (x, y), (x + width, y + height), border_color, 2)
    
    # Calculate text position to center it on button
    (text_width, text_height), _ = cv2.getTextSize(
        text, config.FONT, config.FONT_SCALE, config.FONT_THICKNESS)
    
    text_x = x + (width - text_width) // 2
    text_y = y + (height + text_height) // 2
    
    # Draw text
    cv2.putText(image, text, (text_x, text_y), 
                config.FONT, config.FONT_SCALE, text_color, 
                config.FONT_THICKNESS, config.FONT_LINE_TYPE)
    
    # Return the button's bounding box for hit testing
    return (x, y, x + width, y + height)