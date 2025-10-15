"""
Error handling and graceful degradation module for VisionMate-Lite.
Provides comprehensive error handling, startup validation, and graceful shutdown procedures.
"""

import logging
import sys
import os
import platform
import traceback
import signal
import atexit
from typing import Optional, Dict, Any, Callable, List
from pathlib import Path
import threading
import time


class SystemValidator:
    """Validates system dependencies and requirements at startup."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_results: Dict[str, Dict[str, Any]] = {}
    
    def validate_all(self) -> bool:
        """
        Run all system validations.
        
        Returns:
            True if all critical validations pass, False otherwise
        """
        self.logger.info("Starting system validation...")
        
        validations = [
            ("platform", self._validate_platform),
            ("camera", self._validate_camera_access),
            ("tesseract", self._validate_tesseract),
            ("tts", self._validate_tts_engine),
            ("models", self._validate_models),
            ("directories", self._validate_directories),
            ("permissions", self._validate_permissions)
        ]
        
        all_passed = True
        for name, validator in validations:
            try:
                result = validator()
                self.validation_results[name] = result
                
                if result["status"] == "critical_failure":
                    all_passed = False
                    self.logger.error(f"Critical validation failure: {name} - {result['message']}")
                elif result["status"] == "warning":
                    self.logger.warning(f"Validation warning: {name} - {result['message']}")
                else:
                    self.logger.info(f"Validation passed: {name}")
                    
            except Exception as e:
                self.logger.error(f"Validation error for {name}: {e}")
                self.validation_results[name] = {
                    "status": "critical_failure",
                    "message": f"Validation failed with exception: {e}",
                    "details": traceback.format_exc()
                }
                all_passed = False
        
        if all_passed:
            self.logger.info("All system validations passed")
        else:
            self.logger.error("Some critical validations failed")
        
        return all_passed
    
    def _validate_platform(self) -> Dict[str, Any]:
        """Validate platform compatibility."""
        system = platform.system()
        
        if system in ["Windows", "Darwin"]:
            return {
                "status": "success",
                "message": f"Platform {system} is fully supported",
                "details": {
                    "platform": system,
                    "version": platform.version(),
                    "architecture": platform.architecture()[0]
                }
            }
        elif system == "Linux":
            return {
                "status": "warning",
                "message": "Linux platform has limited support - some features may not work optimally",
                "details": {"platform": system}
            }
        else:
            return {
                "status": "critical_failure",
                "message": f"Platform {system} is not supported",
                "details": {"platform": system}
            }
    
    def _validate_camera_access(self) -> Dict[str, Any]:
        """Validate camera access."""
        try:
            import cv2
            
            # Try to initialize camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    "status": "critical_failure",
                    "message": "Cannot access camera - check permissions and availability",
                    "details": {"camera_index": 0}
                }
            
            # Try to capture a frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret or frame is None:
                return {
                    "status": "critical_failure",
                    "message": "Camera accessible but cannot capture frames",
                    "details": {"camera_index": 0}
                }
            
            return {
                "status": "success",
                "message": "Camera access validated successfully",
                "details": {
                    "camera_index": 0,
                    "frame_shape": frame.shape if frame is not None else None
                }
            }
            
        except ImportError:
            return {
                "status": "critical_failure",
                "message": "OpenCV not available - cannot access camera",
                "details": {"missing_dependency": "opencv-python"}
            }
        except Exception as e:
            return {
                "status": "critical_failure",
                "message": f"Camera validation failed: {e}",
                "details": {"error": str(e)}
            }
    
    def _validate_tesseract(self) -> Dict[str, Any]:
        """Validate Tesseract OCR installation."""
        try:
            import pytesseract
            import cv2
            import numpy as np
            
            # Create test image
            test_image = np.ones((100, 300, 3), dtype=np.uint8) * 255
            cv2.putText(test_image, "TEST", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Try OCR
            result = pytesseract.image_to_string(test_image)
            
            if "TEST" in result.upper():
                return {
                    "status": "success",
                    "message": "Tesseract OCR is working correctly",
                    "details": {"test_result": result.strip()}
                }
            else:
                return {
                    "status": "warning",
                    "message": "Tesseract installed but may have accuracy issues",
                    "details": {"test_result": result.strip()}
                }
                
        except pytesseract.TesseractNotFoundError:
            system = platform.system()
            install_msg = {
                "Windows": "Download from https://github.com/UB-Mannheim/tesseract/wiki",
                "Darwin": "Install with: brew install tesseract",
                "Linux": "Install with: sudo apt-get install tesseract-ocr"
            }.get(system, "Please install Tesseract OCR")
            
            return {
                "status": "critical_failure",
                "message": f"Tesseract OCR not found. {install_msg}",
                "details": {"platform": system, "install_instructions": install_msg}
            }
        except ImportError as e:
            return {
                "status": "critical_failure",
                "message": f"Missing dependency for OCR: {e}",
                "details": {"missing_dependency": str(e)}
            }
        except Exception as e:
            return {
                "status": "critical_failure",
                "message": f"Tesseract validation failed: {e}",
                "details": {"error": str(e)}
            }
    
    def _validate_tts_engine(self) -> Dict[str, Any]:
        """Validate text-to-speech engine."""
        try:
            import pyttsx3
            
            # Try to initialize TTS engine
            engine = pyttsx3.init()
            
            # Test basic properties
            voices = engine.getProperty('voices')
            rate = engine.getProperty('rate')
            
            # Try a quick test (without actually speaking)
            engine.say("test")
            # Don't run runAndWait() to avoid actual speech during validation
            
            return {
                "status": "success",
                "message": "TTS engine initialized successfully",
                "details": {
                    "voices_available": len(voices) if voices else 0,
                    "current_rate": rate,
                    "platform": platform.system()
                }
            }
            
        except ImportError:
            return {
                "status": "critical_failure",
                "message": "pyttsx3 not available - TTS functionality disabled",
                "details": {"missing_dependency": "pyttsx3"}
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"TTS engine has issues but may still work: {e}",
                "details": {"error": str(e)}
            }
    
    def _validate_models(self) -> Dict[str, Any]:
        """Validate YOLO model availability."""
        try:
            from ultralytics import YOLO
            
            # Try to load YOLOv8n model
            model = YOLO('yolov8n.pt')
            
            return {
                "status": "success",
                "message": "YOLO model loaded successfully",
                "details": {"model": "yolov8n.pt"}
            }
            
        except ImportError:
            return {
                "status": "critical_failure",
                "message": "ultralytics package not available",
                "details": {"missing_dependency": "ultralytics"}
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"Model loading issue (may download on first use): {e}",
                "details": {"error": str(e)}
            }
    
    def _validate_directories(self) -> Dict[str, Any]:
        """Validate required directories exist or can be created."""
        required_dirs = [
            "test_data",
            "test_data/detection",
            "test_data/ocr",
            "evaluation",
            "models"
        ]
        
        created_dirs = []
        failed_dirs = []
        
        for dir_path in required_dirs:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                if not Path(dir_path).exists():
                    failed_dirs.append(dir_path)
                else:
                    created_dirs.append(dir_path)
            except Exception as e:
                failed_dirs.append(f"{dir_path} ({e})")
        
        if failed_dirs:
            return {
                "status": "warning",
                "message": f"Some directories could not be created: {failed_dirs}",
                "details": {"failed": failed_dirs, "created": created_dirs}
            }
        else:
            return {
                "status": "success",
                "message": "All required directories validated",
                "details": {"directories": created_dirs}
            }
    
    def _validate_permissions(self) -> Dict[str, Any]:
        """Validate file system permissions."""
        try:
            # Test write permissions in current directory
            test_file = Path("test_permissions.tmp")
            test_file.write_text("test")
            test_file.unlink()
            
            return {
                "status": "success",
                "message": "File system permissions validated",
                "details": {"write_access": True}
            }
            
        except Exception as e:
            return {
                "status": "warning",
                "message": f"Permission issues detected: {e}",
                "details": {"error": str(e)}
            }
    
    def get_validation_report(self) -> str:
        """Generate a human-readable validation report."""
        report = ["System Validation Report", "=" * 30]
        
        for name, result in self.validation_results.items():
            status = result["status"]
            message = result["message"]
            
            status_symbol = {
                "success": "✓",
                "warning": "⚠",
                "critical_failure": "✗"
            }.get(status, "?")
            
            report.append(f"{status_symbol} {name.upper()}: {message}")
        
        return "\n".join(report)


class ErrorHandler:
    """Centralized error handling and recovery system."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_counts: Dict[str, int] = {}
        self.recovery_strategies: Dict[str, Callable] = {}
        self.max_retries = 3
        
        # Register default recovery strategies
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """Register default error recovery strategies."""
        self.recovery_strategies.update({
            "camera_error": self._recover_camera,
            "model_error": self._recover_model,
            "tts_error": self._recover_tts,
            "ocr_error": self._recover_ocr,
            "general_error": self._recover_general
        })
    
    def handle_error(self, error_type: str, exception: Exception, context: Dict[str, Any] = None) -> bool:
        """
        Handle an error with appropriate recovery strategy.
        
        Args:
            error_type: Type of error for recovery strategy selection
            exception: The exception that occurred
            context: Additional context information
            
        Returns:
            True if error was handled and recovery attempted, False otherwise
        """
        context = context or {}
        
        # Log the error
        self.logger.error(f"Error occurred: {error_type} - {exception}")
        if context:
            self.logger.error(f"Context: {context}")
        
        # Track error count
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Check if we've exceeded retry limit
        if self.error_counts[error_type] > self.max_retries:
            self.logger.error(f"Max retries exceeded for {error_type}")
            return False
        
        # Attempt recovery
        recovery_func = self.recovery_strategies.get(error_type, self.recovery_strategies["general_error"])
        
        try:
            return recovery_func(exception, context)
        except Exception as recovery_error:
            self.logger.error(f"Recovery strategy failed: {recovery_error}")
            return False
    
    def _recover_camera(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for camera errors."""
        self.logger.info("Attempting camera recovery...")
        
        # Wait a moment before retry
        time.sleep(1.0)
        
        # Try different camera indices
        for camera_index in [0, 1, 2]:
            try:
                import cv2
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret and frame is not None:
                        self.logger.info(f"Camera recovery successful with index {camera_index}")
                        context["recovered_camera_index"] = camera_index
                        return True
            except Exception as e:
                self.logger.debug(f"Camera index {camera_index} failed: {e}")
        
        self.logger.error("Camera recovery failed")
        return False
    
    def _recover_model(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for model loading errors."""
        self.logger.info("Attempting model recovery...")
        
        # Try to reload the model
        try:
            from ultralytics import YOLO
            model = YOLO('yolov8n.pt')
            self.logger.info("Model recovery successful")
            context["recovered_model"] = model
            return True
        except Exception as e:
            self.logger.error(f"Model recovery failed: {e}")
            return False
    
    def _recover_tts(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for TTS errors."""
        self.logger.info("Attempting TTS recovery...")
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            self.logger.info("TTS recovery successful")
            context["recovered_tts"] = engine
            return True
        except Exception as e:
            self.logger.error(f"TTS recovery failed: {e}")
            # Fallback to print-based output
            context["tts_fallback"] = "print"
            self.logger.info("Using print fallback for TTS")
            return True
    
    def _recover_ocr(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for OCR errors."""
        self.logger.info("Attempting OCR recovery...")
        
        # Wait a moment
        time.sleep(0.5)
        
        try:
            import pytesseract
            import cv2
            import numpy as np
            
            # Test with simple image
            test_image = np.ones((50, 200, 3), dtype=np.uint8) * 255
            cv2.putText(test_image, "TEST", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            result = pytesseract.image_to_string(test_image)
            self.logger.info("OCR recovery successful")
            return True
        except Exception as e:
            self.logger.error(f"OCR recovery failed: {e}")
            return False
    
    def _recover_general(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """General recovery strategy."""
        self.logger.info("Attempting general recovery...")
        
        # Wait a moment and return True to continue
        time.sleep(0.1)
        return True
    
    def reset_error_count(self, error_type: str):
        """Reset error count for a specific error type."""
        if error_type in self.error_counts:
            del self.error_counts[error_type]
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of error counts."""
        return self.error_counts.copy()


class GracefulShutdown:
    """Handles graceful shutdown of the application."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.shutdown_handlers: List[Callable] = []
        self.is_shutting_down = False
        self.shutdown_lock = threading.Lock()
        
        # Register signal handlers
        self._register_signal_handlers()
        
        # Register atexit handler
        atexit.register(self.shutdown)
    
    def _register_signal_handlers(self):
        """Register signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.shutdown()
        
        # Register handlers for common termination signals
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, signal_handler)
    
    def register_shutdown_handler(self, handler: Callable):
        """
        Register a function to be called during shutdown.
        
        Args:
            handler: Function to call during shutdown
        """
        self.shutdown_handlers.append(handler)
    
    def shutdown(self):
        """Perform graceful shutdown."""
        with self.shutdown_lock:
            if self.is_shutting_down:
                return
            
            self.is_shutting_down = True
        
        self.logger.info("Starting graceful shutdown...")
        
        # Call all registered shutdown handlers
        for i, handler in enumerate(self.shutdown_handlers):
            try:
                self.logger.info(f"Calling shutdown handler {i+1}/{len(self.shutdown_handlers)}")
                handler()
            except Exception as e:
                self.logger.error(f"Error in shutdown handler {i+1}: {e}")
        
        self.logger.info("Graceful shutdown complete")
    
    def is_shutdown_requested(self) -> bool:
        """Check if shutdown has been requested."""
        return self.is_shutting_down


class PrivacyManager:
    """Manages privacy safeguards and frame logging controls."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.frame_logging_enabled = False
        self.debug_mode = False
        self.saved_frames_dir = Path("debug_frames")
        
        # Load settings from environment
        self._load_privacy_settings()
    
    def _load_privacy_settings(self):
        """Load privacy settings from environment variables."""
        # Frame logging (disabled by default)
        frame_logging = os.getenv('ENABLE_FRAME_SAVING', 'false').lower()
        self.frame_logging_enabled = frame_logging in ['true', '1', 'yes']
        
        # Debug mode
        debug_mode = os.getenv('DEBUG_MODE', 'false').lower()
        self.debug_mode = debug_mode in ['true', '1', 'yes']
        
        if self.frame_logging_enabled:
            self.logger.warning("Frame logging is ENABLED - frames will be saved to disk")
            self.saved_frames_dir.mkdir(exist_ok=True)
        else:
            self.logger.info("Frame logging is disabled (default)")
    
    def can_save_frame(self) -> bool:
        """Check if frame saving is allowed."""
        return self.frame_logging_enabled
    
    def save_debug_frame(self, frame, filename: str = None):
        """
        Save a frame for debugging purposes (only if enabled).
        
        Args:
            frame: Image frame to save
            filename: Optional filename, auto-generated if not provided
        """
        if not self.can_save_frame():
            return
        
        try:
            import cv2
            
            if filename is None:
                timestamp = int(time.time() * 1000)
                filename = f"debug_frame_{timestamp}.jpg"
            
            filepath = self.saved_frames_dir / filename
            cv2.imwrite(str(filepath), frame)
            self.logger.debug(f"Debug frame saved: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save debug frame: {e}")
    
    def clear_saved_frames(self):
        """Clear all saved debug frames."""
        try:
            if self.saved_frames_dir.exists():
                for frame_file in self.saved_frames_dir.glob("*.jpg"):
                    frame_file.unlink()
                self.logger.info("All saved debug frames cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear saved frames: {e}")
    
    def get_privacy_status(self) -> Dict[str, Any]:
        """Get current privacy settings status."""
        return {
            "frame_logging_enabled": self.frame_logging_enabled,
            "debug_mode": self.debug_mode,
            "saved_frames_dir": str(self.saved_frames_dir),
            "saved_frames_count": len(list(self.saved_frames_dir.glob("*.jpg"))) if self.saved_frames_dir.exists() else 0
        }


# Global instances
_system_validator = None
_error_handler = None
_graceful_shutdown = None
_privacy_manager = None


def get_system_validator() -> SystemValidator:
    """Get global system validator instance."""
    global _system_validator
    if _system_validator is None:
        _system_validator = SystemValidator()
    return _system_validator


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance."""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler


def get_graceful_shutdown() -> GracefulShutdown:
    """Get global graceful shutdown instance."""
    global _graceful_shutdown
    if _graceful_shutdown is None:
        _graceful_shutdown = GracefulShutdown()
    return _graceful_shutdown


def get_privacy_manager() -> PrivacyManager:
    """Get global privacy manager instance."""
    global _privacy_manager
    if _privacy_manager is None:
        _privacy_manager = PrivacyManager()
    return _privacy_manager


def initialize_error_handling() -> bool:
    """
    Initialize all error handling components.
    
    Returns:
        True if initialization successful, False otherwise
    """
    try:
        # Initialize all components
        validator = get_system_validator()
        error_handler = get_error_handler()
        shutdown_handler = get_graceful_shutdown()
        privacy_manager = get_privacy_manager()
        
        # Run system validation
        validation_passed = validator.validate_all()
        
        if not validation_passed:
            print("System validation failed. Check logs for details.")
            print(validator.get_validation_report())
        
        return validation_passed
        
    except Exception as e:
        logging.error(f"Failed to initialize error handling: {e}")
        return False


if __name__ == "__main__":
    # Test the error handling system
    logging.basicConfig(level=logging.INFO)
    
    print("Testing error handling system...")
    
    if initialize_error_handling():
        print("✓ Error handling system initialized successfully")
        
        validator = get_system_validator()
        print("\n" + validator.get_validation_report())
        
        privacy = get_privacy_manager()
        print(f"\nPrivacy status: {privacy.get_privacy_status()}")
        
    else:
        print("✗ Error handling system initialization failed")