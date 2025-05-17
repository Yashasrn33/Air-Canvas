"""
color_detection.py - Color detection and tracking functionality
"""

import cv2
import numpy as np
import config
from utils import get_contour_center

class ColorDetector:
    def __init__(self):
        """Initialize the color detector"""
        # Create kernel for morphological operations
        self.kernel = np.ones(config.KERNEL_SIZE, np.uint8)
        
        # Create the color detection window and trackbars
        cv2.namedWindow("Color detectors", cv2.WINDOW_NORMAL)
        cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, self.trackbar_callback)
        cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, self.trackbar_callback)
        cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, self.trackbar_callback)
        cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, self.trackbar_callback)
        cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, self.trackbar_callback)
        cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, self.trackbar_callback)
        
        # Initialize last detected center
        self.last_center = None
        
        # Buffer for position smoothing
        self.position_buffer = []
        self.max_buffer_size = 5
    
    def trackbar_callback(self, x):
        """Callback function for trackbars"""
        pass
    
    def get_hsv_values(self):
        """Get the current HSV thresholds from trackbars"""
        l_h = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_s = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_v = cv2.getTrackbarPos("Lower Value", "Color detectors")
        u_h = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_s = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_v = cv2.getTrackbarPos("Upper Value", "Color detectors")
        
        return np.array([l_h, l_s, l_v]), np.array([u_h, u_s, u_v])
    
    def set_hsv_values(self, lower_hsv, upper_hsv):
        """Set HSV values on the trackbars"""
        cv2.setTrackbarPos("Lower Hue", "Color detectors", lower_hsv[0])
        cv2.setTrackbarPos("Lower Saturation", "Color detectors", lower_hsv[1])
        cv2.setTrackbarPos("Lower Value", "Color detectors", lower_hsv[2])
        cv2.setTrackbarPos("Upper Hue", "Color detectors", upper_hsv[0])
        cv2.setTrackbarPos("Upper Saturation", "Color detectors", upper_hsv[1])
        cv2.setTrackbarPos("Upper Value", "Color detectors", upper_hsv[2])
    
    def set_color_preset(self, color_name):
        """Set a preset HSV range for a specific color"""
        if color_name in config.COLORS:
            lower_hsv = config.COLORS[color_name]['default_hsv_lower']
            upper_hsv = config.COLORS[color_name]['default_hsv_upper']
            self.set_hsv_values(lower_hsv, upper_hsv)
    
    def detect(self, frame):
        """Detect the colored object in the frame"""
        # Convert frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get current HSV thresholds
        lower_hsv, upper_hsv = self.get_hsv_values()
        
        # Create mask
        mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        
        # Apply morphological operations to clean up the mask
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.dilate(mask, self.kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        center = None
        largest_contour = None
        
        # Process contours if any found
        if contours and len(contours) > 0:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Only proceed if the contour is large enough
            if cv2.contourArea(largest_contour) > 100:
                # Get enclosing circle
                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                
                # Calculate center
                center = get_contour_center(largest_contour)
                
                if center:
                    # Draw the circle and center point
                    cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    
                    # Add to buffer for smoothing
                    self.position_buffer.append(center)
                    if len(self.position_buffer) > self.max_buffer_size:
                        self.position_buffer.pop(0)
                    
                    # Update last center
                    self.last_center = center
        
        return frame, mask, center, largest_contour
    
    def get_smoothed_position(self):
        """Get the smoothed position from buffer"""
        if not self.position_buffer:
            return None
        
        x_avg = sum(p[0] for p in self.position_buffer) // len(self.position_buffer)
        y_avg = sum(p[1] for p in self.position_buffer) // len(self.position_buffer)
        
        return (x_avg, y_avg)
    
    def reset_buffer(self):
        """Reset position buffer"""
        self.position_buffer = []
        self.last_center = None