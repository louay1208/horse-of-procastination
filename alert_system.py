"""
Alert System for AI Procrastination Detector
Displays carousel of horse-of-wisdom images with transition effects.
"""
import logging
import os
from typing import List, Optional

import pygame

from config import AppConfig
from constants import *

# Optional GIF handling
try:
    import imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    IMAGEIO_AVAILABLE = False

logger = logging.getLogger(__name__)


def load_horse_images(folder: str) -> List[pygame.Surface]:
    """
    Load all horse-of-wisdom images (PNG and GIF) from folder.
    
    Args:
        folder: Path to folder containing images
        
    Returns:
        List of pygame.Surface objects
    """
    surfaces: List[pygame.Surface] = []
    
    if not os.path.exists(folder):
        logger.error(f"Images folder not found: {folder}")
        return surfaces
    
    try:
        files = sorted(os.listdir(folder))
    except Exception as e:
        logger.error(f"Error reading images folder: {e}")
        return surfaces
    
    for fname in files:
        lower = fname.lower()
        if not (lower.endswith('.png') or lower.endswith('.gif')):
            continue
        
        path = os.path.join(folder, fname)
        
        if lower.endswith('.png'):
            try:
                img = pygame.image.load(path)
                surfaces.append(img)
                logger.debug(f"Loaded PNG: {fname}")
            except pygame.error as e:
                logger.warning(f"Failed to load image {path}: {e}")
        else:  # .gif handling
            if not IMAGEIO_AVAILABLE:
                # Fallback: load only first frame
                try:
                    img = pygame.image.load(path)
                    surfaces.append(img)
                    logger.debug(f"Loaded GIF (first frame): {fname}")
                except pygame.error as e:
                    logger.warning(f"Failed to load gif {path}: {e}")
            else:
                try:
                    gif = imageio.mimread(path)
                    for frame_idx, frame in enumerate(gif):
                        # Convert (H, W, 4) numpy array → pygame surface
                        surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                        surfaces.append(surf)
                    logger.debug(f"Loaded GIF ({len(gif)} frames): {fname}")
                except Exception as e:
                    logger.warning(f"Failed to read gif {path}: {e}")
    
    logger.info(f"Loaded {len(surfaces)} image(s) from {folder}")
    return surfaces


def trigger_alert(config: Optional[AppConfig] = None) -> bool:
    """
    Display popup with rotating carousel of horse-of-wisdom images.
    
    Args:
        config: Application configuration. If None, uses defaults.
        
    Returns:
        True to continue the main app, False to quit
    """
    if config is None:
        from config import load_config
        config = load_config()
    
    logger.info("Triggering alert")
    
    try:
        pygame.init()
    except Exception as e:
        logger.error(f"Failed to initialize pygame: {e}")
        return True
    
    # Asset locations
    image_folder = config.alert.images_folder
    audio_path = os.path.join(os.path.dirname(__file__), config.alert.audio_file)
    
    # Load carousel images
    horse_images = load_horse_images(image_folder)
    if not horse_images:
        logger.error("No horse images found. Cannot display alert.")
        pygame.quit()
        return True
    
    # Audio handling
    audio_found = False
    try:
        pygame.mixer.init()
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(-1)
            audio_found = True
            logger.debug("Audio playback started")
        else:
            logger.warning(f"Audio file not found: {audio_path}")
            try:
                import winsound
                winsound.Beep(AUDIO_FALLBACK_FREQUENCY, AUDIO_FALLBACK_DURATION)
            except Exception as e:
                logger.warning(f"Fallback beep failed: {e}")
    except Exception as e:
        logger.error(f"Audio init error: {e}")
    
    # Scale images if needed
    max_width = config.alert.window_max_width
    base_img = horse_images[0]
    img_width, img_height = base_img.get_size()
    
    if img_width > max_width:
        scale = max_width / img_width
        new_w = max_width
        new_h = int(img_height * scale)
        try:
            horse_images = [
                pygame.transform.smoothscale(img, (new_w, new_h))
                for img in horse_images
            ]
            img_width, img_height = new_w, new_h
            logger.debug(f"Scaled images to {new_w}x{new_h}")
        except Exception as e:
            logger.error(f"Error scaling images: {e}")
    
    # Create window
    try:
        screen = pygame.display.set_mode((img_width, img_height))
        pygame.display.set_caption("Horse of Wisdom Says...")
    except Exception as e:
        logger.error(f"Failed to create display: {e}")
        pygame.quit()
        return True
    
    # Button definitions
    btn_w = config.ui.button_width
    btn_h = config.ui.button_height
    btn_continue = pygame.Rect(0, 0, btn_w, btn_h)
    btn_continue.center = (img_width // 2 - 90, 30)
    btn_quit = pygame.Rect(0, 0, btn_w, btn_h)
    btn_quit.center = (img_width // 2 + 90, 30)
    
    try:
        font = pygame.font.SysFont(None, FONT_SIZE_BUTTON)
        txt_continue = font.render(config.ui.button_continue_text, True, COLOR_WHITE)
        rect_continue = txt_continue.get_rect(center=btn_continue.center)
        txt_quit = font.render(config.ui.button_quit_text, True, COLOR_WHITE)
        rect_quit = txt_quit.get_rect(center=btn_quit.center)
    except Exception as e:
        logger.error(f"Font rendering error: {e}")
        pygame.quit()
        return True
    
    # Warning for missing audio
    warning_surf = warning_rect = None
    if not audio_found:
        try:
            warn_font = pygame.font.SysFont(None, FONT_SIZE_WARNING)
            warning_surf = warn_font.render("Audio file missing!", True, COLOR_RED)
            warning_rect = warning_surf.get_rect(center=(img_width // 2, 20))
        except Exception as e:
            logger.warning(f"Warning text rendering error: {e}")
    
    # Carousel state
    idx = 0
    clock = pygame.time.Clock()
    switch_interval = config.alert.switch_interval
    transition_duration = config.alert.transition_duration
    last_switch = pygame.time.get_ticks()
    
    # Transition state
    transitioning = False
    transition_start = 0
    next_idx = idx
    
    running = True
    should_continue = True
    
    try:
        while running:
            now = pygame.time.get_ticks()
            
            # Check if it's time to start a transition
            if not transitioning and now - last_switch >= switch_interval:
                transitioning = True
                transition_start = now
                next_idx = (idx + 1) % len(horse_images)
            
            # Render the current frame
            if transitioning:
                # Calculate transition progress (0.0 to 1.0)
                progress = min(1.0, (now - transition_start) / transition_duration)
                
                if progress >= 1.0:
                    # Transition complete
                    transitioning = False
                    idx = next_idx
                    last_switch = now
                    screen.blit(horse_images[idx], (0, 0))
                else:
                    # Render cube rotation effect
                    angle = progress * 90
                    old_scale = abs(90 - angle) / 90
                    new_scale = abs(angle) / 90
                    
                    old_img = horse_images[idx]
                    new_img = horse_images[next_idx]
                    
                    screen.fill(COLOR_BLACK)
                    
                    # Render old image (shrinking)
                    if old_scale > 0.01:
                        old_w = int(img_width * old_scale)
                        if old_w > 0:
                            old_scaled = pygame.transform.smoothscale(
                                old_img, (old_w, img_height)
                            )
                            screen.blit(old_scaled, (0, 0))
                    
                    # Render new image (growing)
                    if new_scale > 0.01:
                        new_w = int(img_width * new_scale)
                        if new_w > 0:
                            new_scaled = pygame.transform.smoothscale(
                                new_img, (new_w, img_height)
                            )
                            screen.blit(new_scaled, (img_width - new_w, 0))
            else:
                screen.blit(horse_images[idx], (0, 0))
            
            mouse = pygame.mouse.get_pos()
            
            # Draw Continue button
            if btn_continue.collidepoint(mouse):
                pygame.draw.rect(screen, BUTTON_CONTINUE_HOVER_COLOR, btn_continue)
            else:
                pygame.draw.rect(screen, BUTTON_CONTINUE_COLOR, btn_continue)
            screen.blit(txt_continue, rect_continue)
            
            # Draw Quit button
            if btn_quit.collidepoint(mouse):
                pygame.draw.rect(screen, BUTTON_QUIT_HOVER_COLOR, btn_quit)
            else:
                pygame.draw.rect(screen, BUTTON_QUIT_COLOR, btn_quit)
            screen.blit(txt_quit, rect_quit)
            
            # Draw warning if needed
            if warning_surf:
                screen.blit(warning_surf, warning_rect)
            
            pygame.display.flip()
            clock.tick(config.ui.display_fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    should_continue = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                        should_continue = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_continue.collidepoint(event.pos):
                        running = False
                        should_continue = True
                    elif btn_quit.collidepoint(event.pos):
                        running = False
                        should_continue = False
    
    except Exception as e:
        logger.error(f"Error in alert loop: {e}", exc_info=True)
    finally:
        pygame.quit()
        logger.info(f"Alert closed. Continue: {should_continue}")
    
    return should_continue


if __name__ == "__main__":
    # Test the alert system
    logging.basicConfig(level=logging.DEBUG)
    trigger_alert()
