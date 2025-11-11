#!/usr/bin/env python3
"""
Test script for keyboard input integration with OCR triggering.
Tests the keyboard handler and OCR processor integration without requiring a camera.
"""

import sys
import os
import logging
import time
import cv2
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.keyboard_handler import SimpleKeyboardHandler
from src.ocr_processor import create_ocr_processor
from src.ocr import create_ocr_engine
from src.audio import AudioManager

def create_test_frame_with_text(text: str = "Hello World!") -> np.ndarray:
    """Create a test frame with text for OCR testing."""
    frame = np.ones((300, 600, 3), dtype=np.uint8) * 255
    cv2.putText(frame, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    return frame

def test_keyboard_ocr_integration():
    """Test the integration of keyboard input with OCR processing."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Testing keyboard input integration with OCR...")
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        audio_manager = AudioManager(speech_rate=200)
        ocr_engine = create_ocr_engine()
        ocr_processor = create_ocr_processor(ocr_engine, audio_manager, threaded=True)
        keyboard_handler = SimpleKeyboardHandler(ocr_trigger_key='space')
        
        # Start OCR processor
        ocr_processor.start_processor()
        
        # Create test frame
        test_frame = create_test_frame_with_text("Testing OCR Integration")
        
        # Create display window
        cv2.namedWindow('Keyboard OCR Test', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Keyboard OCR Test', 600, 300)
        
        logger.info("Test ready!")
        logger.info("Press SPACE to trigger OCR on test image")
        logger.info("Press ESC or Q to quit")
        
        frame_count = 0
        
        while True:
            # Create display frame
            display_frame = test_frame.copy()
            
            # Add instructions
            cv2.putText(display_frame, "Press SPACE for OCR, ESC/Q to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Add processing status
            if ocr_processor.is_busy():
                cv2.putText(display_frame, "Processing OCR...", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Add frame counter
            cv2.putText(display_frame, f"Frame: {frame_count}", 
                       (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            
            cv2.imshow('Keyboard OCR Test', display_frame)
            
            # Check for keyboard input
            action = keyboard_handler.check_input(30)  # 30ms timeout
            
            if action == 'ocr_trigger':
                logger.info("OCR trigger detected - processing test frame")
                success = ocr_processor.process_frame(test_frame)
                if success:
                    logger.info("OCR processing queued successfully")
                else:
                    logger.warning("OCR processing failed to queue")
            
            elif action == 'quit':
                logger.info("Quit signal received")
                break
            
            frame_count += 1
            
            # Small delay
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
    
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False
    
    finally:
        # Cleanup
        try:
            ocr_processor.stop_processor()
            cv2.destroyAllWindows()
        except:
            pass
        
        logger.info("Test completed")
    
    return True

if __name__ == "__main__":
    success = test_keyboard_ocr_integration()
    sys.exit(0 if success else 1)