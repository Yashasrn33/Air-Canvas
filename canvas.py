"""
canvas.py - Canvas management for the Air Canvas application
"""

import numpy as np
import cv2
import config
from utils import save_image

class Canvas:
    def __init__(self):
        """Initialize the canvas"""
        # Create canvas with white background
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT - config.UI_HEIGHT
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        
        # Canvas state history for undo
        self.states = []
        self.max_states = config.MAX_STATES
        
        # Initial state
        self.save_state()
    
    def save_state(self):
        """Save the current canvas state"""
        self.states.append(self.canvas.copy())
        if len(self.states) > self.max_states:
            self.states.pop(0)
    
    def undo(self):
        """Revert to the previous canvas state"""
        if len(self.states) > 1:
            # Remove current state
            self.states.pop()
            # Set canvas to previous state
            self.canvas = self.states[-1].copy()
            return True
        return False
    
    def clear(self):
        """Clear the canvas"""
        self.canvas.fill(255)
        self.save_state()
    
    def save(self, prefix="drawing"):
        """Save the canvas as an image"""
        return save_image(self.canvas, prefix)
    
    def draw_line(self, start_point, end_point, color, thickness):
        """Draw a line on the canvas"""
        if start_point is None or end_point is None:
            return
        
        cv2.line(self.canvas, start_point, end_point, color, thickness)
    
    def draw_circle(self, center, radius, color, thickness):
        """Draw a circle on the canvas"""
        if center is None or radius <= 0:
            return
        
        cv2.circle(self.canvas, center, radius, color, thickness)
    
    def draw_rectangle(self, start_point, end_point, color, thickness):
        """Draw a rectangle on the canvas"""
        if start_point is None or end_point is None:
            return
        
        cv2.rectangle(self.canvas, start_point, end_point, color, thickness)
    
    def erase(self, center, radius):
        """Erase area on the canvas"""
        if center is None or radius <= 0:
            return
        
        cv2.circle(self.canvas, center, radius, (255, 255, 255), -1)
    
    def draw_text(self, text, position, color, font_scale=1.0, thickness=2):
        """Draw text on the canvas"""
        if position is None or not text:
            return
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.canvas, text, position, font, 
                  font_scale, color, thickness, cv2.LINE_AA)
    
    def get_copy(self):
        """Get a copy of the current canvas"""
        return self.canvas.copy()