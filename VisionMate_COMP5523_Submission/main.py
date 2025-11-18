#!/usr/bin/env python3
"""
VisionMate-Lite: Assistive Vision System
Main entry point for the application with comprehensive error handling
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration and error handling
import config
from src.error_handler import (
    initialize_error_handling, 
    get_system_validator, 
    get_error_handler, 
    get_graceful_shutdown,
    get_privacy_manager
)

def setup_logging():
    """Setup logging configuration"""
    log_level = logging.DEBUG if config.ENABLE_LOGGING else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_environment():
    """Validate that required dependencies and environment are available"""
    logger = logging.getLogger(__name__)
    
    # Check platform support
    if not (config.IS_WINDOWS or config.IS_MACOS):
        logger.warning(f"Platform {config.PLATFORM} may have limited support. Windows and macOS are recommended.")
    
    # Check test data path
    test_data_path = Path(config.TEST_DATA_PATH)
    if not test_data_path.exists():
        logger.info(f"Creating test data directory: {test_data_path}")
        test_data_path.mkdir(parents=True, exist_ok=True)
    
    # Check required directories
    required_dirs = ['src', 'test_data/detection', 'test_data/ocr', 'evaluation', 'models']
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    logger.info("Environment validation complete")

def main():
    """Main application entry point with comprehensive error handling"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting VisionMate-Lite...")
    logger.info(f"Platform: {config.PLATFORM}")
    logger.info(f"TTS Engine: {config.TTS_ENGINE}")
    logger.info(f"Test Data Path: {config.TEST_DATA_PATH}")
    
    # Initialize error handling system
    if not initialize_error_handling():
        logger.error("System validation failed. Cannot start application.")
        
        # Print validation report for user
        validator = get_system_validator()
        print("\n" + validator.get_validation_report())
        sys.exit(1)
    
    # Get error handling components
    error_handler = get_error_handler()
    shutdown_handler = get_graceful_shutdown()
    privacy_manager = get_privacy_manager()
    
    logger.info("System validation passed")
    logger.info(f"Privacy settings: {privacy_manager.get_privacy_status()}")
    
    try:
        validate_environment()
        
        # Import core modules
        from src.camera import CameraInterface
        from src.detection import ObjectDetector
        from src.ocr import OCREngine
        from src.audio import AudioManager
        from src.keyboard_handler import SimpleKeyboardHandler
        from src.ocr_processor import create_ocr_processor
        from src.scene_integration import SceneIntegration
        
        logger.info("Initializing core components...")
        
        # Initialize components with error handling
        camera = CameraInterface()
        if not camera.initialize_camera(config.CAMERA_INDEX):
            logger.error("Failed to initialize camera")
            error_handler.handle_error("camera_error", Exception("Camera initialization failed"), {})
            sys.exit(1)
        
        audio_manager = AudioManager(speech_rate=config.SPEECH_RATE)
        ocr_engine = OCREngine(min_text_length=config.MIN_TEXT_LENGTH)
        object_detector = ObjectDetector(confidence_threshold=config.CONFIDENCE_THRESHOLD)
        
        # Create OCR processor for asynchronous processing
        ocr_processor = create_ocr_processor(ocr_engine, audio_manager, threaded=True)
        ocr_processor.start_processor()
        
        # Initialize keyboard handler
        keyboard_handler = SimpleKeyboardHandler(ocr_trigger_key=config.OCR_TRIGGER_KEY)
        
        # Initialize scene classification if enabled
        scene_integration = None
        if config.ENABLE_SCENE_CLASSIFICATION:
            scene_integration = SceneIntegration(
                audio_manager,
                update_interval=config.SCENE_UPDATE_INTERVAL,
                confidence_threshold=config.SCENE_CONFIDENCE_THRESHOLD,
                enabled=True
            )
            if scene_integration.is_enabled():
                logger.info("Scene classification enabled")
            else:
                logger.info("Scene classification disabled - dependencies not available")
                scene_integration = None
        else:
            logger.info("Scene classification disabled by configuration")
        
        logger.info("VisionMate-Lite initialized successfully")
        logger.info("Press SPACE to trigger OCR, ESC or Q to quit")
        
        # Start main application loop
        run_main_loop(camera, object_detector, ocr_processor, keyboard_handler, audio_manager, scene_integration, logger)
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Failed to initialize VisionMate-Lite: {e}")
        error_handler.handle_error("general_error", e, {"phase": "initialization"})
        sys.exit(1)
    finally:
        # Graceful shutdown will handle cleanup automatically
        logger.info("Initiating graceful shutdown...")
        shutdown_handler.shutdown()


def run_main_loop(camera, object_detector, ocr_processor, keyboard_handler, audio_manager, scene_integration, logger):
    """
    Main application loop with comprehensive error handling and recovery.
    
    Args:
        camera: Camera interface instance
        object_detector: Object detection instance
        ocr_processor: OCR processor instance
        keyboard_handler: Keyboard input handler
        audio_manager: Audio manager instance
        scene_integration: Scene classification integration (optional)
        logger: Logger instance
    """
    import cv2
    import time
    
    frame_count = 0
    last_alert_time = {}
    error_handler = get_error_handler()
    shutdown_handler = get_graceful_shutdown()
    privacy_manager = get_privacy_manager()
    
    # Create window for display (helps with keyboard input)
    try:
        cv2.namedWindow('VisionMate-Lite', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('VisionMate-Lite', 640, 480)
    except Exception as e:
        logger.warning(f"Could not create display window: {e}")
    
    logger.info("Starting main processing loop...")
    
    consecutive_frame_failures = 0
    max_consecutive_failures = 10
    
    try:
        while not shutdown_handler.is_shutdown_requested():
            try:
                # Capture frame with error handling
                frame = camera.get_frame()
                if frame is None:
                    consecutive_frame_failures += 1
                    logger.warning(f"Failed to capture frame ({consecutive_frame_failures}/{max_consecutive_failures})")
                    
                    if consecutive_frame_failures >= max_consecutive_failures:
                        logger.error("Too many consecutive frame failures, attempting camera recovery")
                        if not camera.initialize_camera(config.CAMERA_INDEX):
                            logger.error("Camera recovery failed, exiting")
                            break
                        consecutive_frame_failures = 0
                    
                    time.sleep(0.1)
                    continue
                else:
                    consecutive_frame_failures = 0  # Reset on successful frame
                
                # Save debug frame if enabled
                if privacy_manager.can_save_frame() and frame_count % 100 == 0:  # Save every 100th frame
                    privacy_manager.save_debug_frame(frame, f"main_loop_frame_{frame_count}.jpg")
                
                # Check for keyboard input
                try:
                    action = keyboard_handler.check_input(1)  # 1ms timeout
                    
                    if action == 'ocr_trigger':
                        logger.info("OCR trigger detected - processing current frame")
                        ocr_processor.process_frame(frame)
                    elif action == 'quit':
                        logger.info("Quit signal received")
                        break
                except Exception as e:
                    logger.warning(f"Keyboard input error: {e}")
                
                # Process object detection (every 3rd frame for performance)
                if frame_count % config.FRAME_SKIP == 0:
                    try:
                        detections = object_detector.detect(frame)
                        
                        # Process detections for proximity alerts
                        current_time = time.time()
                        for detection in detections:
                            if detection.is_close(frame.shape[1], frame.shape[0]):
                                # Check alert cooldown
                                last_alert = last_alert_time.get(detection.class_name, 0)
                                if current_time - last_alert > config.ALERT_COOLDOWN_SECONDS:
                                    if not audio_manager.is_busy() and not ocr_processor.is_busy():
                                        audio_manager.speak_alert(detection.class_name)
                                        last_alert_time[detection.class_name] = current_time
                                        logger.info(f"Alert: {detection.class_name} detected nearby")
                    except Exception as e:
                        logger.error(f"Object detection error: {e}")
                        error_handler.handle_error("general_error", e, {"phase": "object_detection"})
                
                # Process scene classification (if enabled)
                if scene_integration and frame_count % (config.FRAME_SKIP * 5) == 0:  # Less frequent than object detection
                    try:
                        announced_scene = scene_integration.process_frame(frame)
                        if announced_scene:
                            logger.info(f"Scene announced: {announced_scene}")
                    except Exception as e:
                        logger.error(f"Scene classification error: {e}")
                        error_handler.handle_error("general_error", e, {"phase": "scene_classification"})
                
                # Display frame (optional, helps with keyboard input)
                try:
                    display_frame = frame.copy()
                    
                    # Add status text
                    status_text = "VisionMate-Lite - Press SPACE for OCR, ESC/Q to quit"
                    cv2.putText(display_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    if ocr_processor.is_busy():
                        cv2.putText(display_frame, "Processing OCR...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    
                    # Show current scene if available
                    if scene_integration:
                        current_scene = scene_integration.get_current_scene()
                        if current_scene:
                            scene_text = f"Scene: {current_scene}"
                            cv2.putText(display_frame, scene_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    
                    # Show error count if any
                    error_summary = error_handler.get_error_summary()
                    if error_summary:
                        error_text = f"Errors: {sum(error_summary.values())}"
                        cv2.putText(display_frame, error_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    
                    cv2.imshow('VisionMate-Lite', display_frame)
                except Exception as e:
                    logger.warning(f"Display error: {e}")
                
                frame_count += 1
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Error in main loop iteration: {e}")
                error_handler.handle_error("general_error", e, {"phase": "main_loop", "frame_count": frame_count})
                time.sleep(0.1)  # Brief pause before continuing
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Critical error in main loop: {e}")
        error_handler.handle_error("general_error", e, {"phase": "main_loop_critical"})
    finally:
        try:
            cv2.destroyAllWindows()
        except:
            pass
        logger.info("Main loop ended")
        
        # Print error summary
        error_summary = error_handler.get_error_summary()
        if error_summary:
            logger.info(f"Error summary: {error_summary}")

if __name__ == "__main__":
    main()