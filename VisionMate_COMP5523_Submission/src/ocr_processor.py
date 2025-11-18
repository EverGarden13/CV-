"""
OCR processor module for VisionMate-Lite.
Handles asynchronous OCR processing to avoid blocking the main detection loop.
"""

import threading
import time
import logging
import numpy as np
from typing import Optional, Callable
from queue import Queue, Empty

from .ocr import OCREngine
from .audio import AudioManager


class OCRProcessor:
    """
    Handles asynchronous OCR processing with audio feedback.
    Processes OCR requests in a separate thread to avoid blocking the main detection loop.
    """
    
    def __init__(self, ocr_engine: OCREngine, audio_manager: AudioManager):
        """
        Initialize OCR processor.
        
        Args:
            ocr_engine: OCR engine instance for text extraction
            audio_manager: Audio manager for speech feedback
        """
        self.ocr_engine = ocr_engine
        self.audio_manager = audio_manager
        self.logger = logging.getLogger(__name__)
        
        # Processing queue and thread
        self.processing_queue = Queue(maxsize=5)  # Limit queue size to prevent memory issues
        self.is_running = False
        self.processor_thread: Optional[threading.Thread] = None
        
        # Callbacks for processing events
        self.on_processing_start: Optional[Callable] = None
        self.on_processing_complete: Optional[Callable[[str, str], None]] = None
        
        # Processing state
        self.is_processing = False
        self.last_processing_time = 0
        
        # Import config for cooldown setting
        try:
            import config
            self.processing_cooldown = config.OCR_PROCESSING_COOLDOWN
        except:
            self.processing_cooldown = 2.0  # Fallback default
    
    def start_processor(self) -> None:
        """Start the OCR processing thread."""
        if self.is_running:
            self.logger.warning("OCR processor already running")
            return
        
        self.is_running = True
        self.processor_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processor_thread.start()
        self.logger.info("OCR processor started")
    
    def stop_processor(self) -> None:
        """Stop the OCR processing thread."""
        self.is_running = False
        if self.processor_thread and self.processor_thread.is_alive():
            self.processor_thread.join(timeout=2.0)
        self.logger.info("OCR processor stopped")
    
    def process_frame(self, frame: np.ndarray) -> bool:
        """
        Queue a frame for OCR processing.
        
        Args:
            frame: Image frame to process
            
        Returns:
            True if frame was queued successfully, False otherwise
        """
        if not self.is_running:
            self.logger.warning("OCR processor not running")
            return False
        
        # Check cooldown period
        current_time = time.time()
        if current_time - self.last_processing_time < self.processing_cooldown:
            self.logger.info(f"OCR request ignored - cooldown period ({self.processing_cooldown}s)")
            return False
        
        # Check if already processing
        if self.is_processing:
            self.logger.info("OCR request ignored - already processing")
            return False
        
        try:
            # Try to add frame to queue (non-blocking)
            self.processing_queue.put_nowait(frame.copy())
            self.last_processing_time = current_time
            self.logger.info("Frame queued for OCR processing")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to queue frame for OCR: {e}")
            return False
    
    def _processing_loop(self) -> None:
        """Main OCR processing loop running in separate thread."""
        while self.is_running:
            try:
                # Wait for frame to process
                try:
                    frame = self.processing_queue.get(timeout=1.0)
                except Empty:
                    continue
                
                # Process the frame
                self._process_single_frame(frame)
                
            except Exception as e:
                self.logger.error(f"Error in OCR processing loop: {e}")
                time.sleep(0.1)
    
    def _process_single_frame(self, frame: np.ndarray) -> None:
        """
        Process a single frame for OCR.
        
        Args:
            frame: Image frame to process
        """
        try:
            self.is_processing = True
            
            # Notify processing start
            if self.on_processing_start:
                self.on_processing_start()
            
            # Provide audio feedback that processing has started
            self.logger.info("Starting OCR processing")
            if not self.audio_manager.is_busy():
                self.audio_manager.speak_text("Processing text")
            
            # Extract text using OCR engine
            start_time = time.time()
            extracted_text, status_message = self.ocr_engine.extract_text(frame)
            processing_time = time.time() - start_time
            
            self.logger.info(f"OCR processing completed in {processing_time:.2f} seconds")
            
            # Handle results
            if extracted_text:
                self.logger.info(f"Text extracted: {extracted_text[:100]}...")
                # Speak the extracted text
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text(extracted_text)
                else:
                    # Wait a bit and try again
                    time.sleep(0.5)
                    if not self.audio_manager.is_busy():
                        self.audio_manager.speak_text(extracted_text)
            else:
                self.logger.info(f"No text found: {status_message}")
                # Speak the status message
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text(status_message)
            
            # Notify processing complete
            if self.on_processing_complete:
                self.on_processing_complete(extracted_text or "", status_message)
                
        except Exception as e:
            self.logger.error(f"Error processing OCR frame: {e}")
            error_message = "OCR processing failed"
            if not self.audio_manager.is_busy():
                self.audio_manager.speak_text(error_message)
        
        finally:
            self.is_processing = False
    
    def set_processing_callbacks(self, 
                               on_start: Optional[Callable] = None,
                               on_complete: Optional[Callable[[str, str], None]] = None) -> None:
        """
        Set callback functions for processing events.
        
        Args:
            on_start: Called when OCR processing starts
            on_complete: Called when OCR processing completes (text, status)
        """
        self.on_processing_start = on_start
        self.on_processing_complete = on_complete
    
    def is_busy(self) -> bool:
        """
        Check if OCR processor is currently busy.
        
        Returns:
            True if processing, False otherwise
        """
        return self.is_processing
    
    def get_queue_size(self) -> int:
        """
        Get current processing queue size.
        
        Returns:
            Number of frames waiting to be processed
        """
        return self.processing_queue.qsize()
    
    def clear_queue(self) -> None:
        """Clear the processing queue."""
        try:
            while True:
                self.processing_queue.get_nowait()
        except Empty:
            pass
        self.logger.info("OCR processing queue cleared")


class SimpleOCRProcessor:
    """
    Simplified OCR processor for synchronous processing.
    For use when threading is not desired or needed.
    """
    
    def __init__(self, ocr_engine: OCREngine, audio_manager: AudioManager):
        """
        Initialize simple OCR processor.
        
        Args:
            ocr_engine: OCR engine instance
            audio_manager: Audio manager instance
        """
        self.ocr_engine = ocr_engine
        self.audio_manager = audio_manager
        self.logger = logging.getLogger(__name__)
        
        self.last_processing_time = 0
        
        # Import config for cooldown setting
        try:
            import config
            self.processing_cooldown = config.OCR_PROCESSING_COOLDOWN
        except:
            self.processing_cooldown = 2.0  # Fallback default
    
    def process_frame(self, frame: np.ndarray) -> bool:
        """
        Process frame for OCR synchronously.
        
        Args:
            frame: Image frame to process
            
        Returns:
            True if processing completed, False if skipped
        """
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_processing_time < self.processing_cooldown:
            self.logger.info("OCR request ignored - cooldown period")
            return False
        
        try:
            self.last_processing_time = current_time
            
            # Provide audio feedback
            self.logger.info("Starting OCR processing")
            if not self.audio_manager.is_busy():
                self.audio_manager.speak_text("Processing text")
            
            # Extract text
            extracted_text, status_message = self.ocr_engine.extract_text(frame)
            
            # Handle results
            if extracted_text:
                self.logger.info(f"Text extracted: {extracted_text[:100]}...")
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text(extracted_text)
            else:
                self.logger.info(f"No text found: {status_message}")
                if not self.audio_manager.is_busy():
                    self.audio_manager.speak_text(status_message)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in OCR processing: {e}")
            if not self.audio_manager.is_busy():
                self.audio_manager.speak_text("OCR processing failed")
            return False


# Factory function
def create_ocr_processor(ocr_engine: OCREngine, 
                        audio_manager: AudioManager, 
                        threaded: bool = True) -> OCRProcessor:
    """
    Factory function to create OCR processor.
    
    Args:
        ocr_engine: OCR engine instance
        audio_manager: Audio manager instance
        threaded: Whether to use threaded processor
        
    Returns:
        Configured OCR processor
    """
    if threaded:
        return OCRProcessor(ocr_engine, audio_manager)
    else:
        return SimpleOCRProcessor(ocr_engine, audio_manager)


if __name__ == "__main__":
    # Simple test
    import sys
    import cv2
    import os
    
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    logging.basicConfig(level=logging.INFO)
    
    print("Testing OCR processor...")
    
    try:
        # Create test components
        from src.ocr import create_ocr_engine
        from src.audio import AudioManager
        
        ocr_engine = create_ocr_engine()
        audio_manager = AudioManager()
        processor = create_ocr_processor(ocr_engine, audio_manager, threaded=True)
        
        # Start processor
        processor.start_processor()
        
        # Create test image with text
        test_image = np.ones((200, 600, 3), dtype=np.uint8) * 255
        cv2.putText(test_image, "Hello World Test", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        # Process test image
        print("Processing test image...")
        success = processor.process_frame(test_image)
        print(f"Processing queued: {success}")
        
        # Wait for processing to complete
        time.sleep(5)
        
        # Stop processor
        processor.stop_processor()
        print("Test complete")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)