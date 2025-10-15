#!/usr/bin/env python3
"""
Simple test for keyboard input functionality without OCR dependencies.
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

def test_keyboard_functionality():
    """Test keyboard input handling functionality."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Testing keyboard input functionality...")
    
    try:
        # Initialize keyboard handler
        keyboard_handler = SimpleKeyboardHandler(ocr_trigger_key='space')
        
        # Create test window
        cv2.namedWindow('Keyboard Test', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Keyboard Test', 500, 200)
        
        logger.info("Keyboard test ready!")
        logger.info("Press SPACE to simulate OCR trigger")
        logger.info("Press ESC or Q to quit")
        
        ocr_trigger_count = 0
        frame_count = 0
        
        while True:
            # Create display frame
            display_frame = np.ones((200, 500, 3), dtype=np.uint8) * 64
            
            # Add instructions
            cv2.putText(display_frame, "Press SPACE for OCR trigger", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, "Press ESC or Q to quit", 
                       (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add counters
            cv2.putText(display_frame, f"OCR Triggers: {ocr_trigger_count}", 
                       (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(display_frame, f"Frames: {frame_count}", 
                       (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            cv2.imshow('Keyboard Test', display_frame)
            
            # Check for keyboard input
            action = keyboard_handler.check_input(30)  # 30ms timeout
            
            if action == 'ocr_trigger':
                ocr_trigger_count += 1
                logger.info(f"OCR trigger detected! (Count: {ocr_trigger_count})")
                
                # Simulate OCR processing feedback
                print(">>> Simulating OCR processing...")
                time.sleep(0.5)  # Simulate processing time
                print(">>> OCR processing complete!")
            
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
        cv2.destroyAllWindows()
        logger.info(f"Test completed - OCR triggers: {ocr_trigger_count}")
    
    return True

if __name__ == "__main__":
    success = test_keyboard_functionality()
    print(f"\nKeyboard functionality test: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)