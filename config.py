"""
config.py - Configuration settings for the Air Canvas application
"""

# Window dimensions
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
UI_HEIGHT = 80  # Height of the UI section

# Colors dictionary with name, BGR values, HSV default range
COLORS = {
    'blue': {'bgr': (255, 0, 0), 'text_color': (255, 255, 255), 
             'default_hsv_lower': (100, 150, 100), 'default_hsv_upper': (140, 255, 255)},
    'green': {'bgr': (0, 255, 0), 'text_color': (255, 255, 255), 
              'default_hsv_lower': (40, 100, 100), 'default_hsv_upper': (80, 255, 255)},
    'red': {'bgr': (0, 0, 255), 'text_color': (255, 255, 255), 
            'default_hsv_lower': (0, 150, 100), 'default_hsv_upper': (10, 255, 255)},
    'yellow': {'bgr': (0, 255, 255), 'text_color': (50, 50, 50), 
               'default_hsv_lower': (20, 100, 100), 'default_hsv_upper': (40, 255, 255)},
    'purple': {'bgr': (255, 0, 255), 'text_color': (255, 255, 255), 
               'default_hsv_lower': (140, 100, 100), 'default_hsv_upper': (170, 255, 255)},
    'orange': {'bgr': (0, 165, 255), 'text_color': (255, 255, 255), 
               'default_hsv_lower': (10, 150, 100), 'default_hsv_upper': (20, 255, 255)},
    'black': {'bgr': (0, 0, 0), 'text_color': (255, 255, 255),
              'default_hsv_lower': (0, 0, 0), 'default_hsv_upper': (180, 255, 30)},
    'white': {'bgr': (255, 255, 255), 'text_color': (0, 0, 0),
              'default_hsv_lower': (0, 0, 200), 'default_hsv_upper': (180, 30, 255)},
}

# Tool options
TOOLS = {
    'brush': {'icon': None, 'text': 'BRUSH'},
    'eraser': {'icon': None, 'text': 'ERASER'},
    'rectangle': {'icon': None, 'text': 'RECT'},
    'circle': {'icon': None, 'text': 'CIRCLE'},
    'line': {'icon': None, 'text': 'LINE'},
    'text': {'icon': None, 'text': 'TEXT'},
}

# Default selections
DEFAULT_COLOR = 'blue'
DEFAULT_TOOL = 'brush'
DEFAULT_BRUSH_THICKNESS = 5

# Canvas state configuration
MAX_STATES = 10  # Maximum number of states to save for undo

# Deque configuration
MAX_POINTS = 1024  # Maximum points in deque for each color

# Morphological kernel size
KERNEL_SIZE = (5, 5)

# Save directory
SAVE_DIR = 'saved_drawings'

# Button dimensions for UI
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 60
BUTTON_SPACING = 10

# Font settings
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_THICKNESS = 2
FONT_LINE_TYPE = 16  # cv2.LINE_AA