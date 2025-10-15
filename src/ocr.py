"""
OCR Engine module for VisionMate-Lite
Provides offline text extraction using Tesseract OCR with image preprocessing
"""

import cv2
import numpy as np
import pytesseract
import logging
from typing import Optional, Tuple
import platform
import os
from .error_handler import get_error_handler, get_graceful_shutdown

class OCREngine:
    """
    OCR Engine class that handles text extraction from images using Tesseract.
    Includes image preprocessing and text validation for better accuracy.
    """
    
    def __init__(self, min_text_length: int = 3):
        """
        Initialize OCR Engine with configuration.
        
        Args:
            min_text_length: Minimum length for valid text (default: 3 characters)
        """
        self.min_text_length = min_text_length
        self.logger = logging.getLogger(__name__)
        
        # Configure Tesseract path for cross-platform compatibility
        self._configure_tesseract()
        
        # Test Tesseract availability
        self._test_tesseract()
    
    def _configure_tesseract(self):
        """Configure Tesseract executable path for Windows and macOS."""
        system = platform.system()
        
        if system == "Windows":
            # Common Windows installation paths
            possible_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', ''))
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    self.logger.info(f"Found Tesseract at: {path}")
                    return
                    
        elif system == "Darwin":  # macOS
            # Common macOS installation paths (Homebrew, MacPorts)
            possible_paths = [
                "/usr/local/bin/tesseract",
                "/opt/homebrew/bin/tesseract",
                "/opt/local/bin/tesseract"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    self.logger.info(f"Found Tesseract at: {path}")
                    return
        
        # If no specific path found, assume it's in PATH
        self.logger.info("Using Tesseract from system PATH")
    
    def _test_tesseract(self):
        """Test if Tesseract is properly installed and accessible with error handling."""
        error_handler = get_error_handler()
        
        try:
            # Create a simple test image with text
            test_image = np.ones((100, 300, 3), dtype=np.uint8) * 255
            cv2.putText(test_image, "TEST", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Try to extract text
            result = pytesseract.image_to_string(test_image)
            
            if "TEST" in result.upper():
                self.logger.info("Tesseract is working correctly")
            else:
                self.logger.warning("Tesseract test returned unexpected result")
                
        except Exception as e:
            self.logger.error(f"Tesseract test failed: {e}")
            
            # Try error recovery
            context = {"platform": platform.system()}
            if not error_handler.handle_error("ocr_error", e, context):
                raise RuntimeError(
                    "Tesseract OCR is not properly installed or configured. "
                    "Please install Tesseract OCR:\n"
                    "Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "macOS: brew install tesseract"
                )
    
    def preprocess_image(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy.
        
        Args:
            frame: Input image as numpy array
            
        Returns:
            Preprocessed image optimized for OCR
        """
        try:
            # Convert to grayscale if needed
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame.copy()
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(blurred)
            
            # Apply threshold to get binary image
            # Use adaptive threshold for better results with varying lighting
            binary = cv2.adaptiveThreshold(
                enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up the image
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            # Return original frame if preprocessing fails
            return frame
    
    def validate_text(self, text: str) -> bool:
        """
        Validate extracted text to filter out noise and garbled results.
        
        Args:
            text: Extracted text string
            
        Returns:
            True if text appears to be valid, False otherwise
        """
        if not text or not isinstance(text, str):
            return False
        
        # Remove whitespace and newlines for length check
        cleaned_text = text.strip().replace('\n', ' ').replace('\r', '')
        
        # Check minimum length
        if len(cleaned_text) < self.min_text_length:
            return False
        
        # Check if text contains mostly printable characters
        printable_chars = sum(1 for c in cleaned_text if c.isprintable())
        if len(cleaned_text) > 0 and printable_chars / len(cleaned_text) < 0.7:
            return False
        
        # Check for reasonable character distribution (not all special characters)
        alphanumeric_chars = sum(1 for c in cleaned_text if c.isalnum())
        if len(cleaned_text) > 0 and alphanumeric_chars / len(cleaned_text) < 0.3:
            return False
        
        return True
    
    def extract_text(self, frame: np.ndarray) -> Tuple[Optional[str], str]:
        """
        Extract text from image frame using Tesseract OCR with comprehensive error handling.
        
        Args:
            frame: Input image as numpy array
            
        Returns:
            Tuple of (extracted_text, status_message)
            - extracted_text: The extracted text if successful, None if failed
            - status_message: Status message for user feedback
        """
        error_handler = get_error_handler()
        
        try:
            if frame is None or frame.size == 0:
                return None, "Invalid image provided"
            
            # Preprocess the image for better OCR accuracy
            processed_frame = self.preprocess_image(frame)
            
            # Configure Tesseract for better text detection
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,!?-'
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(processed_frame, config=custom_config)
            
            # Clean up the extracted text
            cleaned_text = extracted_text.strip()
            
            # Validate the extracted text
            if self.validate_text(cleaned_text):
                self.logger.info(f"Successfully extracted text: {cleaned_text[:50]}...")
                return cleaned_text, "Text extracted successfully"
            else:
                self.logger.info("No valid text found in image")
                return None, "No readable text found. Try better lighting or move closer to the text."
                
        except pytesseract.TesseractNotFoundError as e:
            error_msg = (
                "Tesseract OCR not found. Please install Tesseract:\n"
                "Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n"
                "macOS: brew install tesseract"
            )
            self.logger.error(error_msg)
            
            # Try error recovery
            context = {"error_type": "tesseract_not_found"}
            error_handler.handle_error("ocr_error", e, context)
            
            return None, "OCR engine not available"
            
        except pytesseract.TesseractError as e:
            self.logger.error(f"Tesseract processing error: {e}")
            
            # Try error recovery
            context = {"error_type": "tesseract_processing", "frame_shape": frame.shape if frame is not None else None}
            if error_handler.handle_error("ocr_error", e, context):
                # Retry with simpler configuration
                try:
                    simple_config = r'--oem 3 --psm 8'
                    extracted_text = pytesseract.image_to_string(processed_frame, config=simple_config)
                    cleaned_text = extracted_text.strip()
                    
                    if self.validate_text(cleaned_text):
                        self.logger.info("OCR recovery successful with simpler config")
                        return cleaned_text, "Text extracted successfully (recovery mode)"
                except:
                    pass
            
            return None, "OCR processing failed. Try better lighting or clearer text."
            
        except Exception as e:
            self.logger.error(f"Unexpected error during OCR: {e}")
            
            # Try error recovery
            context = {"error_type": "unexpected", "frame_shape": frame.shape if frame is not None else None}
            error_handler.handle_error("ocr_error", e, context)
            
            return None, "OCR processing failed. Please try again."
    
    def get_text_confidence(self, frame: np.ndarray) -> float:
        """
        Get confidence score for text detection (optional utility method).
        
        Args:
            frame: Input image as numpy array
            
        Returns:
            Confidence score between 0 and 1
        """
        try:
            processed_frame = self.preprocess_image(frame)
            
            # Get detailed OCR data including confidence
            data = pytesseract.image_to_data(processed_frame, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence for detected text
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            if confidences:
                return sum(confidences) / len(confidences) / 100.0
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating text confidence: {e}")
            return 0.0


# Utility function for easy integration
def create_ocr_engine(min_text_length: int = 3) -> OCREngine:
    """
    Factory function to create and configure OCR engine.
    
    Args:
        min_text_length: Minimum length for valid text
        
    Returns:
        Configured OCREngine instance
    """
    return OCREngine(min_text_length=min_text_length)


if __name__ == "__main__":
    # Simple test when run directly
    import sys
    
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Create OCR engine
        ocr = create_ocr_engine()
        print("OCR Engine initialized successfully!")
        
        # Test with a simple image if OpenCV is available
        test_image = np.ones((100, 400, 3), dtype=np.uint8) * 255
        cv2.putText(test_image, "Hello World!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
        text, status = ocr.extract_text(test_image)
        print(f"Test result: {text}")
        print(f"Status: {status}")
        
    except Exception as e:
        print(f"OCR Engine test failed: {e}")
        sys.exit(1)