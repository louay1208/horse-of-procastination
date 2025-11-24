"""
Configuration constants for the AI Procrastination Detector.
"""

# YOLO Model Configuration
YOLO_MODEL_PATH = "yolo11n.pt"
CELL_PHONE_CLASS_ID = 67  # YOLO class ID for cell phone

# Detection Settings
DETECTION_THRESHOLD = 30  # Number of consecutive frames to trigger alert
DETECTION_CONFIDENCE = 0.5  # Minimum confidence for detection

# Alert System Settings
ALERT_WINDOW_MAX_WIDTH = 500  # Maximum width for alert window
ALERT_SWITCH_INTERVAL = 2000  # Milliseconds between carousel images
ALERT_TRANSITION_DURATION = 800  # Milliseconds for transition animation

# Button Configuration
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 40
BUTTON_CONTINUE_TEXT = "I'm working!"
BUTTON_QUIT_TEXT = "Done for the day"
BUTTON_CONTINUE_COLOR = (0, 200, 0)
BUTTON_CONTINUE_HOVER_COLOR = (0, 255, 0)
BUTTON_QUIT_COLOR = (200, 0, 0)
BUTTON_QUIT_HOVER_COLOR = (255, 50, 50)

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BACKGROUND = (20, 20, 20)

# Display Settings
DISPLAY_WINDOW_NAME = "Procrastination Detector"
DISPLAY_FPS = 60
QUIT_KEY = 'q'

# Font Settings
FONT_SIZE_BUTTON = 30
FONT_SIZE_WARNING = 24
FONT_SIZE_INFO = 20

# Audio Settings
AUDIO_FALLBACK_FREQUENCY = 1000  # Hz
AUDIO_FALLBACK_DURATION = 500  # ms

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
