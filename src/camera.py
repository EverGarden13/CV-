"""
Camera interface module for VisionMate-Lite.
Provides webcam access and frame capture functionality with graceful error handling.
"""

import cv2
import numpy as np
import logging
from typing import Optional, Tuple
from .error_handler import get_error_handler, get_graceful_shutdown


class CameraInterface:
    """
    Manages webcam access and frame capture for the VisionMate-Lite system.
    
    Provides methods to initialize camera, capture frames, and properly release resources
    with comprehensive error handling for common camera access issues.
    """
    
    def __init__(self):
        """Initialize the camera interface."""
        self.camera: Optional[cv2.VideoCapture] = None
        self.is_initialized = False
        self.camera_index = 0
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def initialize_camera(self, camera_index: int = 0) -> bool:
        """
        Initialize the camera using OpenCV VideoCapture with comprehensive error handling.
        
        Args:
            camera_index (int): Camera index to use (default: 0 for primary camera)
            
        Returns:
            bool: True if camera initialized successfully, False otherwise
        """
        error_handler = get_error_handler()
        
        try:
            self.camera_index = camera_index
            self.logger.info(f"Attempting to initialize camera with index {camera_index}")
            
            # Create VideoCapture object
            self.camera = cv2.VideoCapture(camera_index)
            
            # Check if camera opened successfully
            if not self.camera.isOpened():
                self.logger.error(f"Failed to open camera with index {camera_index}")
                self.camera = None
                
                # Try error recovery
                context = {"camera_index": camera_index}
                if error_handler.handle_error("camera_error", Exception("Camera not opened"), context):
                    recovered_index = context.get("recovered_camera_index", camera_index)
                    if recovered_index != camera_index:
                        return self.initialize_camera(recovered_index)
                
                return False
            
            # Test frame capture to ensure camera is working
            ret, test_frame = self.camera.read()
            if not ret or test_frame is None:
                self.logger.error("Camera opened but failed to capture test frame")
                self.camera.release()
                self.camera = None
                
                # Try error recovery
                context = {"camera_index": camera_index, "issue": "frame_capture_failed"}
                if error_handler.handle_error("camera_error", Exception("Frame capture failed"), context):
                    recovered_index = context.get("recovered_camera_index", camera_index)
                    if recovered_index != camera_index:
                        return self.initialize_camera(recovered_index)
                
                return False
            
            # Set camera properties for better performance
            try:
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.camera.set(cv2.CAP_PROP_FPS, 30)
            except Exception as e:
                self.logger.warning(f"Could not set camera properties: {e}")
                # Continue anyway as this is not critical
            
            self.is_initialized = True
            self.logger.info("Camera initialized successfully")
            
            # Register cleanup with shutdown handler
            shutdown_handler = get_graceful_shutdown()
            shutdown_handler.register_shutdown_handler(self.release)
            
            return True
            
        except cv2.error as e:
            self.logger.error(f"OpenCV error during camera initialization: {e}")
            self.camera = None
            error_handler.handle_error("camera_error", e, {"camera_index": camera_index})
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during camera initialization: {e}")
            self.camera = None
            error_handler.handle_error("camera_error", e, {"camera_index": camera_index})
            return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture and return the current webcam frame with error handling and recovery.
        
        Returns:
            Optional[np.ndarray]: Current frame as numpy array, or None if capture fails
        """
        if not self.is_initialized or self.camera is None:
            self.logger.warning("Camera not initialized. Call initialize_camera() first.")
            return None
        
        error_handler = get_error_handler()
        
        try:
            ret, frame = self.camera.read()
            
            if not ret:
                self.logger.warning("Failed to capture frame from camera")
                
                # Try error recovery
                context = {"camera_index": self.camera_index, "issue": "frame_read_failed"}
                if error_handler.handle_error("camera_error", Exception("Frame read failed"), context):
                    # Try to reinitialize camera
                    if self.initialize_camera(self.camera_index):
                        # Retry frame capture once
                        ret, frame = self.camera.read()
                        if ret and frame is not None:
                            return frame
                
                return None
            
            if frame is None:
                self.logger.warning("Captured frame is None")
                return None
            
            return frame
            
        except cv2.error as e:
            self.logger.error(f"OpenCV error during frame capture: {e}")
            error_handler.handle_error("camera_error", e, {"camera_index": self.camera_index})
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during frame capture: {e}")
            error_handler.handle_error("camera_error", e, {"camera_index": self.camera_index})
            return None
    
    def release(self) -> None:
        """
        Properly release camera resources and cleanup.
        
        Should be called when done using the camera to free system resources.
        """
        try:
            if self.camera is not None:
                self.logger.info("Releasing camera resources")
                self.camera.release()
                self.camera = None
            
            self.is_initialized = False
            
            # Destroy any OpenCV windows that might be open
            cv2.destroyAllWindows()
            
        except Exception as e:
            self.logger.error(f"Error during camera resource cleanup: {e}")
    
    def get_camera_info(self) -> dict:
        """
        Get information about the current camera configuration.
        
        Returns:
            dict: Camera properties and status information
        """
        if not self.is_initialized or self.camera is None:
            return {
                'initialized': False,
                'camera_index': self.camera_index,
                'width': None,
                'height': None,
                'fps': None
            }
        
        try:
            return {
                'initialized': True,
                'camera_index': self.camera_index,
                'width': int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': int(self.camera.get(cv2.CAP_PROP_FPS))
            }
        except Exception as e:
            self.logger.error(f"Error getting camera info: {e}")
            return {'error': str(e)}
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures proper cleanup."""
        self.release()


def test_camera_interface():
    """
    Simple test function to verify camera interface functionality.
    """
    print("Testing CameraInterface...")
    
    with CameraInterface() as camera:
        # Test initialization
        if camera.initialize_camera():
            print("✓ Camera initialized successfully")
            
            # Test camera info
            info = camera.get_camera_info()
            print(f"✓ Camera info: {info}")
            
            # Test frame capture
            frame = camera.get_frame()
            if frame is not None:
                print(f"✓ Frame captured successfully: shape {frame.shape}")
            else:
                print("✗ Failed to capture frame")
        else:
            print("✗ Failed to initialize camera")


if __name__ == "__main__":
    test_camera_interface()