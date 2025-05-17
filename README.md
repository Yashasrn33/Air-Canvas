# Air Canvas - Modular Implementation

This is a complete implementation of the Air Canvas application, broken down into multiple modules for better organization, readability, and maintainability. The application allows you to draw on a virtual canvas by tracking a colored object through your webcam.

## File Structure

```
air_canvas/
│
├── main.py                 # Main entry point that initializes and runs the application
├── canvas.py               # Canvas-related functionality
├── color_detection.py      # Color detection and tracking
├── ui.py                   # User interface components and handling
├── drawing_tools.py        # Drawing tools implementation
├── utils.py                # Utility functions and helpers
└── config.py               # Configuration settings and constants
```

## Features

- **Object Color Tracking**: Track a colored object (like a finger with a colored marker) using HSV color space detection
- **Multiple Drawing Tools**: Brush, Eraser, Rectangle, Circle, Line, and Text
- **Color Selection**: Choose from 8 colors (blue, green, red, yellow, purple, orange, black, white)
- **Adjustable Brush Size**: Change brush thickness on the fly
- **Undo Functionality**: Revert to previous states
- **Save Functionality**: Save drawings as PNG files
- **Clean UI**: Intuitive interface with buttons for all tools and colors

## Components

### 1. `config.py`
Contains all configurable settings like window dimensions, colors, tools, and defaults.

### 2. `utils.py`
Provides utility functions for creating UI elements, calculating distances, file management, etc.

### 3. `canvas.py`
Handles the drawing canvas, its state management, and operations like saving and clearing.

### 4. `color_detection.py`
Manages the color detection and tracking of objects using HSV color space and contour detection.

### 5. `drawing_tools.py`
Implements the various drawing tools (brush, eraser, shapes, text) with their specific behaviors.

### 6. `ui.py`
Creates and manages the user interface elements like buttons and handles user interactions.

### 7. `main.py`
The main application entry point that orchestrates all the components and runs the main loop.

## How to Use

1. Run `main.py` to start the application.
2. Use the trackbars in the "Color detectors" window to adjust HSV values for object detection.
3. Hold a colored object (like a colored marker cap) in front of the webcam.
4. Use the UI to select tools and colors.
5. Draw on the canvas by moving the detected object.
6. Save your creation using the SAVE button or by pressing 's'.

## Controls

- **Mouse**: Control through colored object tracking
- **Keyboard**:
  - 'q': Quit the application
  - 's': Save the canvas
  - 'c': Clear the canvas
  - 'z': Undo the last action
  - For text tool: Type characters and press Enter to confirm

## Improvements Over Original

1. **Modular Structure**: Code split into logical modules for better organization
2. **Object-Oriented Design**: Clear class hierarchies and separation of concerns
3. **Enhanced UI**: More intuitive user interface with visual feedback
4. **Multiple Drawing Tools**: Added tools for various drawing needs
5. **Save & Undo**: Added ability to save drawings and undo actions
6. **Better Error Handling**: More robust error checking and handling
7. **Position Smoothing**: Smoother drawing with position averaging
8. **Customizable Settings**: Easy configuration through config.py
