"""
ui.py - User interface components and handling
"""

import cv2
import numpy as np
import config
from utils import create_button, draw_text_with_background, inside_rectangle

class UserInterface:
    def __init__(self, width, height):
        """Initialize the UI with dimensions"""
        self.width = width
        self.height = config.UI_HEIGHT
        
        # Create a base UI panel
        self.ui_panel = np.ones((self.height, width, 3), dtype=np.uint8) * 230
        
        # Button dimensions
        self.button_width = config.BUTTON_WIDTH
        self.button_height = config.BUTTON_HEIGHT
        self.button_spacing = config.BUTTON_SPACING
        
        # Track button areas for hit testing
        self.buttons = {}
        
        # Track current selections
        self.selected_tool = config.DEFAULT_TOOL
        self.selected_color = config.DEFAULT_COLOR
        self.brush_thickness = config.DEFAULT_BRUSH_THICKNESS
    
    def create_ui(self, tool_manager):
        """Create the UI panel with all buttons"""
        # Start with clean panel
        ui = self.ui_panel.copy()
        
        # Initialize position for buttons
        x_start = self.button_spacing
        y_center = self.height // 2
        
        # Clear button
        clear_btn = create_button(
            ui,
            (x_start, y_center - self.button_height // 2),
            (self.button_width, self.button_height),
            "CLEAR",
            color=(200, 200, 200),
            text_color=(0, 0, 0)
        )
        self.buttons['clear'] = clear_btn
        x_start += self.button_width + self.button_spacing
        
        # Undo button
        undo_btn = create_button(
            ui,
            (x_start, y_center - self.button_height // 2),
            (self.button_width, self.button_height),
            "UNDO",
            color=(200, 200, 200),
            text_color=(0, 0, 0)
        )
        self.buttons['undo'] = undo_btn
        x_start += self.button_width + self.button_spacing
        
        # Save button
        save_btn = create_button(
            ui,
            (x_start, y_center - self.button_height // 2),
            (self.button_width, self.button_height),
            "SAVE",
            color=(200, 200, 200),
            text_color=(0, 0, 0)
        )
        self.buttons['save'] = save_btn
        x_start += self.button_width + self.button_spacing
        
        # Add a separator
        cv2.line(ui, (x_start, 10), (x_start, self.height - 10), (150, 150, 150), 1)
        x_start += self.button_spacing
        
        # Tool buttons
        self.buttons['tools'] = {}
        for tool_name in config.TOOLS:
            is_selected = tool_name == self.selected_tool
            
            # Create tool button
            tool_btn = create_button(
                ui,
                (x_start, y_center - self.button_height // 2),
                (self.button_width, self.button_height),
                config.TOOLS[tool_name]['text'],
                color=(180, 180, 180) if is_selected else (220, 220, 220),
                text_color=(0, 0, 0),
                selected=is_selected
            )
            self.buttons['tools'][tool_name] = tool_btn
            x_start += self.button_width + self.button_spacing
        
        # Add a separator
        cv2.line(ui, (x_start, 10), (x_start, self.height - 10), (150, 150, 150), 1)
        x_start += self.button_spacing
        
        # Color buttons
        self.buttons['colors'] = {}
        for color_name in config.COLORS:
            is_selected = color_name == self.selected_color
            color_bgr = config.COLORS[color_name]['bgr']
            text_color = config.COLORS[color_name]['text_color']
            
            # Create color button
            color_btn = create_button(
                ui,
                (x_start, y_center - self.button_height // 2),
                (self.button_width, self.button_height),
                color_name.upper(),
                color=color_bgr,
                text_color=text_color,
                selected=is_selected
            )
            self.buttons['colors'][color_name] = color_btn
            x_start += self.button_width + self.button_spacing
        
        # Show current settings at the right end
        size_text = f"Size: {tool_manager.current_thickness}"
        tool_text = f"Tool: {tool_manager.current_tool_name}"
        color_text = f"Color: {tool_manager.current_color_name}"
        
        cv2.putText(ui, size_text, (self.width - 200, 20), 
                   config.FONT, config.FONT_SCALE, (0, 0, 0), 1, config.FONT_LINE_TYPE)
        cv2.putText(ui, tool_text, (self.width - 200, 40), 
                   config.FONT, config.FONT_SCALE, (0, 0, 0), 1, config.FONT_LINE_TYPE)
        cv2.putText(ui, color_text, (self.width - 200, 60), 
                   config.FONT, config.FONT_SCALE, (0, 0, 0), 1, config.FONT_LINE_TYPE)
        
        # If text tool is active and waiting for input, show the current text
        current_tool = tool_manager.get_current_tool()
        if tool_manager.current_tool_name == 'text' and hasattr(current_tool, 'is_waiting_for_text') and current_tool.is_waiting_for_text():
            text_status = f"Text: {current_tool.current_text}"
            draw_text_with_background(
                ui, 
                text_status, 
                (10, self.height - 10),
                bg_color=(240, 240, 240)
            )
        
        return ui
    
    def handle_click(self, position, tool_manager, canvas):
        """Handle clicks on UI elements"""
        x, y = position
        
        # Only handle if in UI area
        if y > self.height:
            return False
        
        # Check clear button
        if inside_rectangle(position, (self.buttons['clear'][0], self.buttons['clear'][1]), 
                          (self.buttons['clear'][2], self.buttons['clear'][3])):
            tool_manager.clear_all()
            return True
        
        # Check undo button
        if inside_rectangle(position, (self.buttons['undo'][0], self.buttons['undo'][1]), 
                          (self.buttons['undo'][2], self.buttons['undo'][3])):
            canvas.undo()
            return True
        
        # Check save button
        if inside_rectangle(position, (self.buttons['save'][0], self.buttons['save'][1]), 
                          (self.buttons['save'][2], self.buttons['save'][3])):
            canvas.save()
            return True
        
        # Check tool buttons
        for tool_name, btn in self.buttons['tools'].items():
            if inside_rectangle(position, (btn[0], btn[1]), (btn[2], btn[3])):
                self.selected_tool = tool_name
                tool_manager.set_tool(tool_name)
                return True
        
        # Check color buttons
        for color_name, btn in self.buttons['colors'].items():
            if inside_rectangle(position, (btn[0], btn[1]), (btn[2], btn[3])):
                self.selected_color = color_name
                tool_manager.set_color(color_name)
                return True
        
        return False
    
    def update_brush_thickness(self, thickness):
        """Update the brush thickness"""
        self.brush_thickness = thickness