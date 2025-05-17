"""
drawing_tools.py - Implementation of drawing tools
"""

import cv2
import numpy as np
import config
from collections import deque
from utils import calculate_distance

class Tool:
    """Base class for drawing tools"""
    def __init__(self, canvas):
        self.canvas = canvas
        self.color = config.COLORS[config.DEFAULT_COLOR]['bgr']
        self.thickness = config.DEFAULT_BRUSH_THICKNESS
    
    def set_color(self, color_name):
        """Set the current drawing color"""
        if color_name in config.COLORS:
            self.color = config.COLORS[color_name]['bgr']
    
    def set_thickness(self, thickness):
        """Set the current drawing thickness"""
        self.thickness = max(1, thickness)
    
    def handle_drawing(self, position):
        """Handle drawing at the given position"""
        pass
    
    def reset(self):
        """Reset tool state"""
        pass

class BrushTool(Tool):
    """Brush tool for freehand drawing"""
    def __init__(self, canvas):
        super().__init__(canvas)
        self.points = {}
        self.indices = {}
        
        # Initialize points for each color
        for color in config.COLORS:
            self.points[color] = [deque(maxlen=config.MAX_POINTS)]
            self.indices[color] = 0
        
        self.current_color_name = config.DEFAULT_COLOR
        self.last_position = None
    
    def set_color(self, color_name):
        """Set the current drawing color"""
        super().set_color(color_name)
        self.current_color_name = color_name
    
    def handle_drawing(self, position):
        """Handle drawing at the given position"""
        if position is None:
            # If no position, create a new point collection
            self.points[self.current_color_name].append(deque(maxlen=config.MAX_POINTS))
            self.indices[self.current_color_name] += 1
            self.last_position = None
            return
        
        # Add the point to the deque
        self.points[self.current_color_name][self.indices[self.current_color_name]].appendleft(position)
        
        # Draw the line on the canvas if there's a previous point
        if self.last_position:
            self.canvas.draw_line(self.last_position, position, self.color, self.thickness)
        
        self.last_position = position
    
    def reset(self):
        """Reset brush state"""
        self.last_position = None
        
    def clear(self):
        """Clear all points"""
        for color in config.COLORS:
            self.points[color] = [deque(maxlen=config.MAX_POINTS)]
            self.indices[color] = 0
        self.last_position = None

class EraserTool(Tool):
    """Eraser tool for removing drawn content"""
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_position = None
    
    def handle_drawing(self, position):
        """Handle erasing at the given position"""
        if position is None:
            self.last_position = None
            return
        
        # Erase around the position
        erase_radius = self.thickness * 2
        self.canvas.erase(position, erase_radius)
        
        self.last_position = position
    
    def reset(self):
        """Reset eraser state"""
        self.last_position = None

class ShapeTool(Tool):
    """Base class for shape drawing tools"""
    def __init__(self, canvas):
        super().__init__(canvas)
        self.start_point = None
        self.drawing = False
        self.temp_canvas = None
    
    def start_shape(self, position):
        """Start drawing a shape"""
        self.start_point = position
        self.drawing = True
        self.temp_canvas = self.canvas.get_copy()
    
    def preview_shape(self, position):
        """Preview the shape during drawing"""
        if not self.drawing or not self.start_point:
            return self.canvas.get_copy()
        
        # Create a copy of the temp canvas for preview
        preview = self.temp_canvas.copy()
        
        # Draw preview shape on it
        self.draw_preview(preview, position)
        
        return preview
    
    def finish_shape(self, position):
        """Complete the shape drawing"""
        if not self.drawing or not self.start_point:
            return False
        
        # Draw the final shape on the actual canvas
        self.draw_final_shape(position)
        
        # Reset state
        self.drawing = False
        self.start_point = None
        self.temp_canvas = None
        
        return True
    
    def draw_preview(self, preview_canvas, position):
        """Draw shape preview - to be implemented by subclasses"""
        pass
    
    def draw_final_shape(self, position):
        """Draw final shape - to be implemented by subclasses"""
        pass
    
    def handle_drawing(self, position):
        """Handle shape drawing at the given position"""
        if position is None:
            return
        
        if not self.drawing:
            self.start_shape(position)
        else:
            self.finish_shape(position)
            self.canvas.save_state()
    
    def reset(self):
        """Reset shape tool state"""
        self.drawing = False
        self.start_point = None
        self.temp_canvas = None

class RectangleTool(ShapeTool):
    """Tool for drawing rectangles"""
    def draw_preview(self, preview_canvas, position):
        """Draw rectangle preview"""
        cv2.rectangle(preview_canvas, self.start_point, position, self.color, self.thickness)
    
    def draw_final_shape(self, position):
        """Draw final rectangle"""
        self.canvas.draw_rectangle(self.start_point, position, self.color, self.thickness)

class CircleTool(ShapeTool):
    """Tool for drawing circles"""
    def draw_preview(self, preview_canvas, position):
        """Draw circle preview"""
        radius = int(calculate_distance(self.start_point, position))
        cv2.circle(preview_canvas, self.start_point, radius, self.color, self.thickness)
    
    def draw_final_shape(self, position):
        """Draw final circle"""
        radius = int(calculate_distance(self.start_point, position))
        self.canvas.draw_circle(self.start_point, radius, self.color, self.thickness)

class LineTool(ShapeTool):
    """Tool for drawing straight lines"""
    def draw_preview(self, preview_canvas, position):
        """Draw line preview"""
        cv2.line(preview_canvas, self.start_point, position, self.color, self.thickness)
    
    def draw_final_shape(self, position):
        """Draw final line"""
        self.canvas.draw_line(self.start_point, position, self.color, self.thickness)

class TextTool(Tool):
    """Tool for adding text"""
    def __init__(self, canvas):
        super().__init__(canvas)
        self.text_position = None
        self.current_text = ""
        self.waiting_for_text = False
        self.font_scale_ratio = 5.0  # Ratio to convert thickness to font scale
    
    def handle_drawing(self, position):
        """Handle text placement"""
        if not self.waiting_for_text:
            self.text_position = position
            self.current_text = ""
            self.waiting_for_text = True
            print("Text position set. Type your text and press Enter.")
    
    def add_character(self, char):
        """Add a character to the current text"""
        if self.waiting_for_text:
            self.current_text += char
    
    def remove_character(self):
        """Remove the last character from current text"""
        if self.waiting_for_text and self.current_text:
            self.current_text = self.current_text[:-1]
    
    def confirm_text(self):
        """Confirm and draw the text"""
        if self.waiting_for_text and self.text_position and self.current_text:
            font_scale = self.thickness / self.font_scale_ratio
            self.canvas.draw_text(self.current_text, self.text_position, 
                                self.color, font_scale, self.thickness)
            self.canvas.save_state()
            self.reset()
            return True
        return False
    
    def reset(self):
        """Reset text tool state"""
        self.text_position = None
        self.current_text = ""
        self.waiting_for_text = False
    
    def is_waiting_for_text(self):
        """Check if the tool is waiting for text input"""
        return self.waiting_for_text

class ToolManager:
    """Manager for all drawing tools"""
    def __init__(self, canvas):
        self.canvas = canvas
        
        # Create all tools
        self.tools = {
            'brush': BrushTool(canvas),
            'eraser': EraserTool(canvas),
            'rectangle': RectangleTool(canvas),
            'circle': CircleTool(canvas),
            'line': LineTool(canvas),
            'text': TextTool(canvas)
        }
        
        # Set initial tool
        self.current_tool_name = config.DEFAULT_TOOL
        self.current_color_name = config.DEFAULT_COLOR
        self.current_thickness = config.DEFAULT_BRUSH_THICKNESS
    
    def get_current_tool(self):
        """Get the current active tool"""
        return self.tools[self.current_tool_name]
    
    def set_tool(self, tool_name):
        """Set the active tool"""
        if tool_name in self.tools:
            # Reset the current tool before switching
            self.get_current_tool().reset()
            
            # Switch tool
            self.current_tool_name = tool_name
            
            # Apply current color and thickness to the new tool
            tool = self.get_current_tool()
            tool.set_color(self.current_color_name)
            tool.set_thickness(self.current_thickness)
            
            return True
        return False
    
    def set_color(self, color_name):
        """Set the active color for all tools"""
        if color_name in config.COLORS:
            self.current_color_name = color_name
            
            # Apply to all tools
            for tool in self.tools.values():
                tool.set_color(color_name)
            
            return True
        return False
    
    def set_thickness(self, thickness):
        """Set the active thickness for all tools"""
        thickness = max(1, thickness)
        self.current_thickness = thickness
        
        # Apply to all tools
        for tool in self.tools.values():
            tool.set_thickness(thickness)
        
        return True
    
    def handle_drawing(self, position):
        """Handle drawing with the current tool"""
        return self.get_current_tool().handle_drawing(position)
    
    def get_preview(self, position=None):
        """Get preview image if the tool supports it"""
        tool = self.get_current_tool()
        
        # Check if the tool is a shape tool with preview capability
        if isinstance(tool, ShapeTool) and tool.drawing:
            return tool.preview_shape(position)
        
        return self.canvas.get_copy()
    
    def handle_key(self, key):
        """Handle key press for text tool"""
        tool = self.get_current_tool()
        
        # If current tool is text and waiting for input
        if isinstance(tool, TextTool) and tool.is_waiting_for_text():
            if key == 8:  # Backspace
                tool.remove_character()
                return True
            elif key == 13:  # Enter
                tool.confirm_text()
                return True
            elif 32 <= key <= 126:  # Printable ASCII
                tool.add_character(chr(key))
                return True
        
        return False
    
    def clear_all(self):
        """Clear all tools and the canvas"""
        # Reset all tools
        for tool in self.tools.values():
            tool.reset()
            
            # Special handling for brush
            if isinstance(tool, BrushTool):
                tool.clear()
        
        # Clear canvas
        self.canvas.clear()