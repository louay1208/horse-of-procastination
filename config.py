"""
Configuration management for the AI Procrastination Detector.
Loads settings from config.yaml or uses defaults from constants.py
"""
import os
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from constants import *


@dataclass
class DetectionConfig:
    """Detection-related configuration."""
    threshold: int = DETECTION_THRESHOLD
    confidence: float = DETECTION_CONFIDENCE
    yolo_model_path: str = YOLO_MODEL_PATH
    cell_phone_class_id: int = CELL_PHONE_CLASS_ID


@dataclass
class AlertConfig:
    """Alert system configuration."""
    images_folder: str = "horse of wisdom"
    audio_file: str = "alert_sound.mp3"
    window_max_width: int = ALERT_WINDOW_MAX_WIDTH
    switch_interval: int = ALERT_SWITCH_INTERVAL
    transition_duration: int = ALERT_TRANSITION_DURATION


@dataclass
class UIConfig:
    """UI-related configuration."""
    button_width: int = BUTTON_WIDTH
    button_height: int = BUTTON_HEIGHT
    button_continue_text: str = BUTTON_CONTINUE_TEXT
    button_quit_text: str = BUTTON_QUIT_TEXT
    display_window_name: str = DISPLAY_WINDOW_NAME
    display_fps: int = DISPLAY_FPS
    quit_key: str = QUIT_KEY


@dataclass
class AppConfig:
    """Main application configuration."""
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    alert: AlertConfig = field(default_factory=AlertConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    log_level: str = LOG_LEVEL


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from YAML file or use defaults.
    
    Args:
        config_path: Path to config.yaml file. If None, looks in current directory.
        
    Returns:
        AppConfig instance with loaded or default settings.
    """
    if config_path is None:
        config_path = "config.yaml"
    
    config = AppConfig()
    
    if not YAML_AVAILABLE:
        logging.warning("PyYAML not installed. Using default configuration.")
        return config
    
    if not os.path.exists(config_path):
        logging.info(f"Config file {config_path} not found. Using defaults.")
        return config
    
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if data:
            # Load detection settings
            if 'detection' in data:
                det = data['detection']
                config.detection = DetectionConfig(
                    threshold=det.get('threshold', DETECTION_THRESHOLD),
                    confidence=det.get('confidence', DETECTION_CONFIDENCE),
                    yolo_model_path=det.get('yolo_model_path', YOLO_MODEL_PATH),
                    cell_phone_class_id=det.get('cell_phone_class_id', CELL_PHONE_CLASS_ID)
                )
            
            # Load alert settings
            if 'alert' in data:
                alert = data['alert']
                config.alert = AlertConfig(
                    images_folder=alert.get('images_folder', config.alert.images_folder),
                    audio_file=alert.get('audio_file', 'alert_sound.mp3'),
                    window_max_width=alert.get('window_max_width', ALERT_WINDOW_MAX_WIDTH),
                    switch_interval=alert.get('switch_interval', ALERT_SWITCH_INTERVAL),
                    transition_duration=alert.get('transition_duration', ALERT_TRANSITION_DURATION)
                )
            
            # Load UI settings
            if 'ui' in data:
                ui = data['ui']
                config.ui = UIConfig(
                    button_width=ui.get('button_width', BUTTON_WIDTH),
                    button_height=ui.get('button_height', BUTTON_HEIGHT),
                    button_continue_text=ui.get('button_continue_text', BUTTON_CONTINUE_TEXT),
                    button_quit_text=ui.get('button_quit_text', BUTTON_QUIT_TEXT),
                    display_window_name=ui.get('display_window_name', DISPLAY_WINDOW_NAME),
                    display_fps=ui.get('display_fps', DISPLAY_FPS),
                    quit_key=ui.get('quit_key', QUIT_KEY)
                )
            
            # Load logging settings
            config.log_level = data.get('log_level', LOG_LEVEL)
        
        logging.info(f"Configuration loaded from {config_path}")
    except Exception as e:
        logging.error(f"Error loading config file: {e}. Using defaults.")
    
    return config


def create_default_config_file(path: str = "config.yaml") -> None:
    """
    Create a default config.yaml file with all available options.
    
    Args:
        path: Path where to create the config file.
    """
    default_config = """# AI Procrastination Detector Configuration

# Detection Settings
detection:
  threshold: 30  # Number of consecutive frames to trigger alert
  confidence: 0.5  # Minimum confidence for detection (0.0 - 1.0)
  yolo_model_path: "yolo11n.pt"
  cell_phone_class_id: 67

# Alert System Settings
alert:
  images_folder: "horse of wisdom"  # Relative to project directory
  audio_file: "alert_sound.mp3"
  window_max_width: 500
  switch_interval: 2000  # Milliseconds between carousel images
  transition_duration: 800  # Milliseconds for transition animation

# UI Settings
ui:
  button_width: 160
  button_height: 40
  button_continue_text: "I'm working!"
  button_quit_text: "Quit App"
  display_window_name: "Procrastination Detector"
  display_fps: 60
  quit_key: "q"

# Logging
log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
"""
    
    try:
        with open(path, 'w') as f:
            f.write(default_config)
        print(f"Default configuration file created at {path}")
    except Exception as e:
        logging.error(f"Error creating config file: {e}")


if __name__ == "__main__":
    # Create default config file if run directly
    create_default_config_file()
