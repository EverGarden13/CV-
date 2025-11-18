"""
Object detection module using YOLOv8n for VisionMate-Lite.
Provides real-time detection of key navigation objects: person, chair, car, door.
"""

from ultralytics import YOLO
import numpy as np
from typing import List, Optional
import logging
from .error_handler import get_error_handler, get_graceful_shutdown


def get_largest_detection(detections: List['Detection']) -> Optional['Detection']:
    """
    Get the detection with the largest bounding box area from a list of detections.
    
    Args:
        detections: List of Detection objects
        
    Returns:
        Detection with largest area, or None if list is empty
    """
    if not detections:
        return None
    
    return max(detections, key=lambda d: d.get_area())


class Detection:
    """Represents a single object detection with class, confidence, and bounding box."""
    
    def __init__(self, class_name: str, confidence: float, bbox: tuple):
        """
        Initialize a detection object.
        
        Args:
            class_name: Name of the detected object class
            confidence: Detection confidence score (0.0 to 1.0)
            bbox: Bounding box coordinates as (x1, y1, x2, y2)
        """
        self.class_name = class_name
        self.confidence = confidence
        self.bbox = bbox  # (x1, y1, x2, y2)
    
    def get_area(self) -> float:
        """Calculate the area of the bounding box."""
        return (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])
    
    def is_close(self, frame_width: int, frame_height: int, threshold: float = 0.15) -> bool:
        """
        Determine if object is in close proximity based on bounding box size.
        
        Args:
            frame_width: Width of the video frame
            frame_height: Height of the video frame
            threshold: Proximity threshold (default 0.15 = 15% of frame area)
            
        Returns:
            True if object is considered close (bbox area > threshold * frame area)
        """
        frame_area = frame_width * frame_height
        return self.get_area() / frame_area > threshold


class ObjectDetector:
    """Object detector using YOLOv8n for detecting navigation-relevant objects."""
    
    # COCO class IDs for target objects
    TARGET_CLASSES = {
        0: 'person',    # COCO class 0
        56: 'chair',    # COCO class 56
        2: 'car',       # COCO class 2
        # Note: 'door' is not in COCO dataset, would need custom mapping
        # For now, we'll focus on the 3 available COCO classes
    }
    
    def __init__(self, confidence_threshold: float = 0.5, model_name: str = 'yolov8n.pt'):
        """
        Initialize the object detector with comprehensive error handling.
        
        Args:
            confidence_threshold: Minimum confidence score for detections (default 0.5)
            model_name: YOLOv8 model variant to use (default 'yolov8n.pt' for nano)
        
        Raises:
            ValueError: If confidence_threshold is not between 0 and 1
        """
        # Validate confidence threshold
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError(f"confidence_threshold must be between 0 and 1, got {confidence_threshold}")
        
        self.confidence_threshold = confidence_threshold
        self.model_name = model_name
        self.model = None
        self.logger = logging.getLogger(__name__)
        
        error_handler = get_error_handler()
        
        try:
            # Initialize YOLOv8n model - will download if not present
            self.model = YOLO(model_name)
            self.logger.info(f"YOLOv8 model {model_name} loaded successfully")
            
            # Register cleanup with shutdown handler
            shutdown_handler = get_graceful_shutdown()
            shutdown_handler.register_shutdown_handler(self._cleanup)
            
        except Exception as e:
            self.logger.error(f"Failed to load YOLOv8 model: {e}")
            
            # Try error recovery
            context = {"model_name": model_name}
            if error_handler.handle_error("model_error", e, context):
                recovered_model = context.get("recovered_model")
                if recovered_model:
                    self.model = recovered_model
                    self.logger.info("Model recovery successful")
                else:
                    raise RuntimeError(f"Could not initialize YOLOv8 model: {e}")
            else:
                raise RuntimeError(f"Could not initialize YOLOv8 model: {e}")
    
    def _cleanup(self):
        """Cleanup model resources."""
        try:
            if self.model:
                # YOLO models don't need explicit cleanup, but we can clear the reference
                self.model = None
                self.logger.info("Object detector cleaned up")
        except Exception as e:
            self.logger.error(f"Error during object detector cleanup: {e}")
    
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """
        Detect objects in the given frame with comprehensive error handling.
        
        Args:
            frame: Input video frame as numpy array (BGR format from OpenCV)
            
        Returns:
            List of Detection objects for target classes above confidence threshold
        """
        if self.model is None:
            self.logger.warning("Model not initialized, returning empty detection list")
            return []
        
        if frame is None or frame.size == 0:
            self.logger.warning("Invalid frame provided, returning empty detection list")
            return []
        
        error_handler = get_error_handler()
        
        try:
            # Run YOLOv8 inference on the frame
            results = self.model(frame, verbose=False)
            
            detections = []
            
            # Process results from the first (and only) image
            if len(results) > 0:
                result = results[0]
                
                # Extract boxes, confidences, and class IDs
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes in xyxy format
                    confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
                    class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Class IDs
                    
                    # Filter detections for target classes and confidence threshold
                    for i, (box, conf, class_id) in enumerate(zip(boxes, confidences, class_ids)):
                        # Check if this is a target class and meets confidence threshold
                        if class_id in self.TARGET_CLASSES and conf >= self.confidence_threshold:
                            class_name = self.TARGET_CLASSES[class_id]
                            bbox = tuple(box)  # Convert to (x1, y1, x2, y2) tuple
                            
                            detection = Detection(class_name, float(conf), bbox)
                            detections.append(detection)
            
            self.logger.debug(f"Detected {len(detections)} objects above threshold")
            return detections
            
        except RuntimeError as e:
            # Model-specific errors
            self.logger.error(f"Model runtime error during detection: {e}")
            context = {"model_name": self.model_name, "frame_shape": frame.shape if frame is not None else None}
            error_handler.handle_error("model_error", e, context)
            return []
        except Exception as e:
            self.logger.error(f"Error during object detection: {e}")
            context = {"model_name": self.model_name, "frame_shape": frame.shape if frame is not None else None}
            error_handler.handle_error("general_error", e, context)
            return []
    
    def get_largest_detection(self, detections: List[Detection]) -> Optional[Detection]:
        """
        Get the detection with the largest bounding box area.
        
        Args:
            detections: List of Detection objects
            
        Returns:
            Detection with largest area, or None if list is empty
        """
        if not detections:
            return None
        
        return max(detections, key=lambda d: d.get_area())
    
    def filter_close_detections(self, detections: List[Detection], 
                              frame_width: int, frame_height: int) -> List[Detection]:
        """
        Filter detections to only include those in close proximity.
        
        Args:
            detections: List of Detection objects
            frame_width: Width of the video frame
            frame_height: Height of the video frame
            
        Returns:
            List of detections considered to be in close proximity
        """
        return [d for d in detections if d.is_close(frame_width, frame_height)]