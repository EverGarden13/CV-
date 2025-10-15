#!/usr/bin/env python3
"""
VisionMate-Lite: Assistive Vision System
Main entry point for the application
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration
import config

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
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting VisionMate-Lite...")
    logger.info(f"Platform: {config.PLATFORM}")
    logger.info(f"TTS Engine: {config.TTS_ENGINE}")
    logger.info(f"Test Data Path: {config.TEST_DATA_PATH}")
    
    try:
        validate_environment()
        
        # Import core modules
        from src.camera import CameraInterface
        from src.detection import ObjectDetector
        from src.ocr import OCREngine
        from src.audio import AudioManager
        from src.keyboard_handler import SimpleKeyboardHandler
        from src.ocr_processor import create_ocr_processor
        
        logger.info("Initializing core components...")
        
        # Initialize components
        camera = CameraInterface()
        if not camera.initialize_camera(config.CAMERA_INDEX):
            logger.error("Failed to initialize camera")
            return
        
        audio_manager = AudioManager(speech_rate=config.SPEECH_RATE)
        ocr_engine = OCREngine(min_text_length=config.MIN_TEXT_LENGTH)
        object_detector = ObjectDetector(confidence_threshold=config.CONFIDENCE_THRESHOLD)
        
        # Create OCR processor for asynchronous processing
        ocr_processor = create_ocr_processor(ocr_engine, audio_manager, threaded=True)
        ocr_processor.start_processor()
        
        # Initialize keyboard handler
        keyboard_handler = SimpleKeyboardHandler(ocr_trigger_key=config.OCR_TRIGGER_KEY)
        
        logger.info("VisionMate-Lite initialized successfully")
        logger.info("Press SPACE to trigger OCR, ESC or Q to quit")
        
        # Start main application loop
        run_main_loop(camera, object_detector, ocr_processor, keyboard_handler, audio_manager, logger)
        
    except Exception as e:
        logger.error(f"Failed to initialize VisionMate-Lite: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            if 'camera' in locals():
                camera.release()
            if 'ocr_processor' in locals():
                ocr_processor.stop_processor()
        except:
            pass


def run_main_loop(camera, object_detector, ocr_processor, keyboard_handler, audio_manager, logger):
    """
    Main application loop with keyboard input handling and OCR triggering.
    
    Args:
        camera: Camera interface instance
        object_detector: Object detection instance
        ocr_processor: OCR processor instance
        keyboard_handler: Keyboard input handler
        audio_manager: Audio manager instance
        logger: Logger instance
    """
    import cv2
    import time
    
    frame_count = 0
    last_alert_time = {}
    
    # Create window for display (helps with keyboard input)
    cv2.namedWindow('VisionMate-Lite', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('VisionMate-Lite', 640, 480)
    
    logger.info("Starting main processing loop...")
    
    try:
        while True:
            # Capture frame
            frame = camera.get_frame()
            if frame is None:
                logger.warning("Failed to capture frame")
                time.sleep(0.1)
                continue
            
            # Check for keyboard input
            action = keyboard_handler.check_input(1)  # 1ms timeout
            
            if action == 'ocr_trigger':
                logger.info("OCR trigger detected - processing current frame")
                ocr_processor.process_frame(frame)
            elif action == 'quit':
                logger.info("Quit signal received")
                break
            
            # Process object detection (every 3rd frame for performance)
            if frame_count % config.FRAME_SKIP == 0:
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
            
            # Display frame (optional, helps with keyboard input)
            display_frame = frame.copy()
            
            # Add status text
            status_text = "VisionMate-Lite - Press SPACE for OCR, ESC/Q to quit"
            cv2.putText(display_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if ocr_processor.is_busy():
                cv2.putText(display_frame, "Processing OCR...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            cv2.imshow('VisionMate-Lite', display_frame)
            
            frame_count += 1
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
    finally:
        cv2.destroyAllWindows()
        logger.info("Main loop ended")

if __name__ == "__main__":
    main()