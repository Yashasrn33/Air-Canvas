"""
main.py - Main entry point for the Air Canvas application
"""

import cv2
import numpy as np
import time
from color_detection import ColorDetector
from canvas import Canvas
from drawing_tools import ToolManager
from ui import UserInterface
import config
from utils import create_directories, nothing

def main():
    """Main function to run the application"""
    print("=== Air Canvas Application ===")
    print("Initializing...")
    
    # Create required directories
    create_directories()
    
    # Initialize components
    canvas = Canvas()
    color_detector = ColorDetector()
    tool_manager = ToolManager(canvas)
    ui = UserInterface(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    
    # Create trackbar for brush thickness
    cv2.createTrackbar("Brush Size", "Color detectors", 
                     config.DEFAULT_BRUSH_THICKNESS, 25, lambda x: tool_manager.set_thickness(x))
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.WINDOW_HEIGHT)
    
    # Create windows
    cv2.namedWindow("Air Canvas", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Paint", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Air Canvas", config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    cv2.resizeWindow("Paint", config.WINDOW_WIDTH, config.WINDOW_HEIGHT - config.UI_HEIGHT)
    cv2.resizeWindow("Color detectors", 600, 300)
    
    print("Application initialized successfully!")
    print("\nInstructions:")
    print("- Use the trackbars to adjust HSV values for object detection")
    print("- Use the UI to select tools and colors")
    print("- Press 'q' to quit")
    print("- Press 's' to save the canvas")
    print("- Press 'c' to clear the canvas")
    print("- Press 'z' to undo")
    print("- For text tool: Click where you want to place text, type, and press Enter")
    
    # Main loop
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from webcam")
            break
        
        # Flip frame horizontally for more intuitive interaction
        frame = cv2.flip(frame, 1)
        
        # Detect object
        frame, mask, center, _ = color_detector.detect(frame)
        
        # Get smoothed position
        smoothed_position = color_detector.get_smoothed_position()
        
        # Create UI panel
        ui_panel = ui.create_ui(tool_manager)
        
        # If we have a valid position
        if smoothed_position:
            # Check for UI interaction first
            if not ui.handle_click(smoothed_position, tool_manager, canvas):
                # If not interacting with UI, handle drawing
                # Adjust y coordinate to account for UI height
                drawing_position = (smoothed_position[0], 
                                  smoothed_position[1] - config.UI_HEIGHT)
                
                # Only draw if position is within canvas
                if 0 <= drawing_position[1] < canvas.height:
                    tool_manager.handle_drawing(drawing_position)
        
        # Get preview (for shape tools)
        if smoothed_position:
            drawing_position = (smoothed_position[0], 
                              smoothed_position[1] - config.UI_HEIGHT)
            preview_canvas = tool_manager.get_preview(drawing_position)
        else:
            preview_canvas = canvas.get_copy()
        
        # Combine UI and frame
        frame_with_ui = np.vstack((ui_panel, frame))
        
        # Show windows
        cv2.imshow("Air Canvas", frame_with_ui)
        cv2.imshow("Paint", preview_canvas)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = canvas.save()
            print(f"Canvas saved as {filename}")
        elif key == ord('c'):
            tool_manager.clear_all()
            print("Canvas cleared")
        elif key == ord('z'):
            if canvas.undo():
                print("Undo successful")
            else:
                print("Nothing to undo")
        else:
            # Let tool manager handle other keys (for text input, etc.)
            tool_manager.handle_key(key)
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed")

if __name__ == "__main__":
    main()