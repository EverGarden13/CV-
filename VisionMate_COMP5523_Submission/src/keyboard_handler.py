"""
Keyboard input handler module for VisionMate-Lite.
Provides non-blocking keyboard input handling for OCR triggering and other user interactions.
"""

import cv2
import threading
import time
import logging
from typing import Callable, Optional
from queue import Queue, Empty


class KeyboardHandler:
    """
    Handles keyboard input for triggering OCR and other user interactions.
    Uses OpenCV's waitKey for cross-platform compatibility and non-blocking operation.
    """
    
    def __init__(self, ocr_trigger_key: str = 'space'):
        """
        Initialize keyboard handler.
        
        Args:
            ocr_trigger_key: Key to trigger OCR processing (default: 'space')
        """
        self.ocr_trigger_key = ocr_trigger_key
        self.logger = logging.getLogger(__name__)
        
        # Callback functions
        self.ocr_callback: Optional[Callable] = None
        
        # Key mapping for OpenCV waitKey
        self.key_map = {
            'space': 32,  # Space bar
            'enter': 13,  # Enter key
            'esc': 27,    # Escape key
            'q': ord('q'),
            'r': ord('r'),
            's': ord('s')
        }
        
        # Input queue for non-blocking processing
        self.input_queue = Queue()
        self.is_running = False
        self.input_thread: Optional[threading.Thread] = None
    
    def set_ocr_callback(self, callback: Callable) -> None:
        """
        Set callback function for OCR triggering.
        
        Args:
            callback: Function to call when OCR is triggered
        """
        self.ocr_callback = callback
    
    def start_input_handling(self) -> None:
        """Start keyboard input handling in a separate thread."""
        if self.is_running:
            self.logger.warning("Keyboard handler already running")
            return
        
        self.is_running = True
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()
        self.logger.info("Keyboard input handling started")
    
    def stop_input_handling(self) -> None:
        """Stop keyboard input handling."""
        self.is_running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join(timeout=1.0)
        self.logger.info("Keyboard input handling stopped")
    
    def _input_loop(self) -> None:
        """Main input handling loop running in separate thread."""
        while self.is_running:
            try:
                # Use OpenCV waitKey with short timeout for non-blocking operation
                key = cv2.waitKey(1) & 0xFF
                
                if key != 255:  # 255 means no key pressed
                    self.input_queue.put(key)
                
                # Small sleep to prevent excessive CPU usage
                time.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Error in input loop: {e}")
                time.sleep(0.1)
    
    def process_input(self) -> None:
        """
        Process any pending keyboard input.
        Should be called from the main application loop.
        """
        try:
            while True:
                try:
                    key = self.input_queue.get_nowait()
                    self._handle_key(key)
                except Empty:
                    break
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
    
    def _handle_key(self, key: int) -> None:
        """
        Handle individual key press.
        
        Args:
            key: Key code from OpenCV waitKey
        """
        try:
            # Check for OCR trigger
            if key == self.key_map.get(self.ocr_trigger_key, 32):
                self.logger.info("OCR trigger key pressed")
                if self.ocr_callback:
                    # Execute OCR callback in a separate thread to avoid blocking
                    ocr_thread = threading.Thread(target=self.ocr_callback, daemon=True)
                    ocr_thread.start()
                else:
                    self.logger.warning("OCR callback not set")
            
            # Handle other keys
            elif key == self.key_map.get('esc', 27):
                self.logger.info("Escape key pressed")
                # Could be used for graceful shutdown
            
            elif key == ord('q'):
                self.logger.info("Q key pressed - quit signal")
                # Could be used for quit signal
            
            else:
                # Log other key presses for debugging
                if key < 128:  # Printable ASCII
                    self.logger.debug(f"Key pressed: {chr(key)} (code: {key})")
                else:
                    self.logger.debug(f"Special key pressed: {key}")
                    
        except Exception as e:
            self.logger.error(f"Error handling key {key}: {e}")
    
    def check_for_ocr_trigger(self) -> bool:
        """
        Non-blocking check for OCR trigger key.
        Alternative to callback-based approach.
        
        Returns:
            True if OCR trigger key was pressed, False otherwise
        """
        try:
            while True:
                try:
                    key = self.input_queue.get_nowait()
                    if key == self.key_map.get(self.ocr_trigger_key, 32):
                        return True
                    else:
                        # Put other keys back for processing
                        self._handle_key(key)
                except Empty:
                    break
            return False
        except Exception as e:
            self.logger.error(f"Error checking for OCR trigger: {e}")
            return False
    
    def wait_for_key(self, timeout: float = 0.1) -> Optional[int]:
        """
        Wait for any key press with timeout.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            Key code if pressed, None if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return self.input_queue.get_nowait()
            except Empty:
                time.sleep(0.01)
        return None


class SimpleKeyboardHandler:
    """
    Simplified keyboard handler using OpenCV waitKey directly.
    For use in simple main loops without threading.
    """
    
    def __init__(self, ocr_trigger_key: str = 'space'):
        """
        Initialize simple keyboard handler.
        
        Args:
            ocr_trigger_key: Key to trigger OCR processing
        """
        self.ocr_trigger_key = ocr_trigger_key
        self.logger = logging.getLogger(__name__)
        
        # Key mapping
        self.key_map = {
            'space': 32,
            'enter': 13,
            'esc': 27,
            'q': ord('q')
        }
    
    def check_input(self, timeout_ms: int = 1) -> Optional[str]:
        """
        Check for keyboard input with minimal blocking.
        
        Args:
            timeout_ms: Timeout in milliseconds for waitKey
            
        Returns:
            Action string if recognized key pressed, None otherwise
        """
        try:
            key = cv2.waitKey(timeout_ms) & 0xFF
            
            if key == 255:  # No key pressed
                return None
            
            # Check for recognized keys
            if key == self.key_map.get(self.ocr_trigger_key, 32):
                self.logger.info("OCR trigger detected")
                return 'ocr_trigger'
            elif key == self.key_map.get('esc', 27) or key == ord('q'):
                self.logger.info("Quit signal detected")
                return 'quit'
            else:
                # Log other keys for debugging
                if key < 128:
                    self.logger.debug(f"Unhandled key: {chr(key)}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error checking input: {e}")
            return None


# Utility functions
def create_keyboard_handler(ocr_trigger_key: str = 'space', threaded: bool = True) -> KeyboardHandler:
    """
    Factory function to create keyboard handler.
    
    Args:
        ocr_trigger_key: Key to trigger OCR
        threaded: Whether to use threaded handler
        
    Returns:
        Configured keyboard handler
    """
    if threaded:
        return KeyboardHandler(ocr_trigger_key)
    else:
        return SimpleKeyboardHandler(ocr_trigger_key)


if __name__ == "__main__":
    # Simple test
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    print("Testing keyboard handler...")
    print("Press SPACE for OCR trigger, ESC or Q to quit")
    
    # Test simple handler
    handler = SimpleKeyboardHandler()
    
    # Create a dummy window for OpenCV key capture
    cv2.namedWindow('Keyboard Test', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Keyboard Test', 300, 100)
    
    # Create a simple image
    import numpy as np
    test_img = np.ones((100, 300, 3), dtype=np.uint8) * 128
    cv2.putText(test_img, "Press SPACE or ESC", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    try:
        while True:
            cv2.imshow('Keyboard Test', test_img)
            
            action = handler.check_input(30)  # 30ms timeout
            
            if action == 'ocr_trigger':
                print("OCR triggered!")
            elif action == 'quit':
                print("Quit signal received")
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        cv2.destroyAllWindows()
        print("Test complete")