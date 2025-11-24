"""
AI Procrastination Detector - Main Application
Detects cell phone usage via webcam and triggers alerts.
"""
import logging
import sys
from typing import Optional

import cv2
import torch
from ultralytics import YOLO

from config import load_config, AppConfig
from constants import *
from alert_system import trigger_alert


# Configure logging
def setup_logging(log_level: str = "INFO") -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=LOG_FORMAT
    )


def validate_environment(config: AppConfig) -> bool:
    """
    Validate that all required resources are available.
    
    Args:
        config: Application configuration
        
    Returns:
        True if environment is valid, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    # Check YOLO model
    import os
    if not os.path.exists(config.detection.yolo_model_path):
        logger.error(f"YOLO model not found at {config.detection.yolo_model_path}")
        logger.error("Please download the model or check the path in config.yaml")
        return False
    
    # Check camera availability
    test_cap = cv2.VideoCapture(0)
    if not test_cap.isOpened():
        logger.error("Could not open webcam. Please check camera connection.")
        test_cap.release()
        return False
    test_cap.release()
    
    # Check images folder
    if not os.path.exists(config.alert.images_folder):
        logger.warning(f"Images folder not found: {config.alert.images_folder}")
        logger.warning("Alert system may not work correctly without horse images.")
    
    # Check audio file (optional)
    audio_path = os.path.join(os.path.dirname(__file__), config.alert.audio_file)
    if not os.path.exists(audio_path):
        logger.warning(f"Audio file not found: {audio_path}")
        logger.warning("Will use fallback beep sound.")
    
    return True


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Load configuration
    config = load_config()
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting AI Procrastination Detector")
    
    # Validate environment
    if not validate_environment(config):
        logger.error("Environment validation failed. Exiting.")
        return 1
    
    # Check for CUDA
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using device: {device}")
    
    # Load the YOLO model
    try:
        logger.info(f"Loading YOLO model from {config.detection.yolo_model_path}")
        model = YOLO(config.detection.yolo_model_path)
    except Exception as e:
        logger.error(f"Failed to load YOLO model: {e}")
        return 1
    
    # Initialize webcam
    cap: Optional[cv2.VideoCapture] = None
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            logger.error("Could not open webcam")
            return 1
        
        logger.info(f"Detection started. Press '{config.ui.quit_key}' to quit.")
        logger.info(f"Alert triggers after {config.detection.threshold} consecutive detections")
        
        phone_detected_frames = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to capture frame")
                continue
            
            try:
                # Run inference
                results = model(
                    frame,
                    classes=[config.detection.cell_phone_class_id],
                    device=device,
                    verbose=False,
                    conf=config.detection.confidence
                )
                
                # Check if phone is detected
                phone_detected = any(len(r.boxes) > 0 for r in results)
                
                if phone_detected:
                    phone_detected_frames += 1
                    logger.debug(
                        f"Phone detected! Count: {phone_detected_frames}/"
                        f"{config.detection.threshold}"
                    )
                else:
                    phone_detected_frames = 0
                
                # Trigger alert if threshold reached
                if phone_detected_frames >= config.detection.threshold:
                    logger.info("Detection threshold reached. Triggering alert!")
                    
                    try:
                        should_continue = trigger_alert(config)
                        if not should_continue:
                            logger.info("User requested quit from alert")
                            break
                    except Exception as e:
                        logger.error(f"Error in alert system: {e}")
                    
                    phone_detected_frames = 0
                
                # Visualize results
                annotated_frame = results[0].plot()
                
                # Add quit instruction
                cv2.putText(
                    annotated_frame,
                    f"Press '{config.ui.quit_key}' to quit",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    COLOR_RED,
                    2
                )
                
                # Add detection counter
                if phone_detected_frames > 0:
                    cv2.putText(
                        annotated_frame,
                        f"Detection: {phone_detected_frames}/{config.detection.threshold}",
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 255),
                        2
                    )
                
                # Display the frame
                cv2.imshow(config.ui.display_window_name, annotated_frame)
                
                # Check for quit key
                if cv2.waitKey(1) & 0xFF == ord(config.ui.quit_key):
                    logger.info(f"Quit via '{config.ui.quit_key}' key")
                    break
                
                # Check if window was closed
                prop = cv2.getWindowProperty(
                    config.ui.display_window_name,
                    cv2.WND_PROP_VISIBLE
                )
                if prop < 1:
                    logger.info("Quit via window close")
                    break
                    
            except Exception as e:
                logger.error(f"Error during detection loop: {e}")
                continue
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1
    finally:
        # Cleanup
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        logger.info("Application shutdown complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
