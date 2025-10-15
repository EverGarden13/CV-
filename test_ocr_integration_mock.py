#!/usr/bin/env python3
"""
Test OCR integration with mock components (no Tesseract required).
"""

import sys
import os
import logging
import time
import cv2
import numpy as np
import threading
from queue import Queue, Empty

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.keyboard_handler import SimpleKeyboardHandler
from src.audio import AudioManager

class MockOCREngine:
    """Mock OCR engine for testing without Tesseract."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, frame):
        """Mock text extraction."""
        # Simulate processing time
        time.sleep(1.0)
        
        # Return mock text based on frame content
        mock_text = "This is mock OCR text extracted from the image"
        return mock_text, "Text extracted successfully"

class MockOCRProcessor:
    """Mock OCR processor for testing."""
    
    def __init__(self, ocr_engine, audio_manager):
        self.ocr_engine = ocr_engine
        self.audio_manager = audio_manager
        self.logger = logging.getLogger(__name__)
        
        self.processing_queue = Queue(maxsize=5)
        self.is_running = False
        self.processor_thread = None
        self.is_processing = False
        self.last_processing_time = 0
        self.processing_cooldown = 2.0
    
    def start_processor(self):
        """Start the processing thread."""
        if self.is_running:
            return
        
        self.is_running = True
        self.processor_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processor_thread.start()
        self.logger.info("Mock OCR processor started")
    
    def stop_processor(self):
        """Stop the processing thread."""
        self.is_running = False
        if self.processor_thread and self.processor_thread.is_alive():
            self.processor_thread.join(timeout=2.0)
        self.logger.info("Mock OCR processor stopped")
    
    def process_frame(self, frame):
        """Queue frame for processing."""
        current_time = time.time()
        if current_time - self.last_processing_time < self.processing_cooldown:
            self.logger.info("OCR request ignored - cooldown period")
            return False
        
        if self.is_processing:
            self.logger.info("OCR request ignored - already processing")
            return False
        
        try:
            self.processing_queue.put_nowait(frame.copy())
            self.last_processing_time = current_time
            self.logger.info("Frame queued for OCR processing")
            return True
        except:
            return False
    
    def is_busy(self):
        """Check if processor is busy."""
        return self.is_processing
    
    def _processing_loop(self):
        """Main processing loop."""
        while self.is_running:
            try:
                try:
                    frame = self.processing_queue.get(timeout=1.0)
                except Empty:
                    continue
                
                self._process_single_frame(frame)
            except Exception as e:
                self.logger.error(f"Error in processing loop: {e}")
    
    def _process_single_frame(self, frame):
        """Process a single frame."""
        try:
            self.is_processing = True
            
            # Audio feedback for processing start
            self.logger.info("Starting OCR processing")
            if not self.audio_manager.is_busy():
                self.audio_manager.speak_text("Processing text")
            
            # Extract text
            extracted_text, status = self.ocr_engine.extract_text(frame)
            
            # Speak results
            if extracted_text:
                self.logger.info(f"Text extracted: {extracted_text}")
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text(extracted_text)
            else:
                self.logger.info("No text found")
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text("No text found")
        
        except Exception as e:
            self.logger.error(f"Error processing frame: {e}")
        finally:
            self.is_processing = False

def test_full_integration():
    """Test full keyboard + OCR integration with mock components."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Testing full keyboard + OCR integration...")
    
    try:
        # Initialize components
        audio_manager = AudioManager(speech_rate=200)
        ocr_engine = MockOCREngine()
        ocr_processor = MockOCRProcessor(ocr_engine, audio_manager)
        keyboard_handler = SimpleKeyboardHandler(ocr_trigger_key='space')
        
        # Start processor
        ocr_processor.start_processor()
        
        # Create test frame
        test_frame = np.ones((300, 600, 3), dtype=np.uint8) * 255
        cv2.putText(test_frame, "Sample Text for OCR", (50, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
        
        # Create display window
        cv2.namedWindow('Full Integration Test', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Full Integration Test', 600, 300)
        
        logger.info("Integration test ready!")
        logger.info("Press SPACE to trigger OCR processing")
        logger.info("Press ESC or Q to quit")
        
        ocr_count = 0
        frame_count = 0
        
        while True:
            # Create display frame
            display_frame = test_frame.copy()
            
            # Add status overlay
            cv2.putText(display_frame, "Press SPACE for OCR, ESC/Q to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            if ocr_processor.is_busy():
                cv2.putText(display_frame, "Processing OCR...", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            cv2.putText(display_frame, f"OCR Count: {ocr_count}", 
                       (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            
            cv2.imshow('Full Integration Test', display_frame)
            
            # Check keyboard input
            action = keyboard_handler.check_input(30)
            
            if action == 'ocr_trigger':
                logger.info("OCR trigger detected")
                success = ocr_processor.process_frame(test_frame)
                if success:
                    ocr_count += 1
                    logger.info(f"OCR processing initiated (Count: {ocr_count})")
            
            elif action == 'quit':
                logger.info("Quit signal received")
                break
            
            frame_count += 1
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        logger.info("Test interrupted")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False
    finally:
        try:
            ocr_processor.stop_processor()
            cv2.destroyAllWindows()
        except:
            pass
        logger.info(f"Integration test completed - OCR triggers: {ocr_count}")
    
    return True

if __name__ == "__main__":
    success = test_full_integration()
    print(f"\nFull integration test: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)