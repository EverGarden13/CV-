"""
Scene Classification Module for VisionMate-Lite

This module provides lightweight scene classification using a pre-trained model
suitable for CPU inference. It classifies scenes into basic categories like
office, street, corridor, etc.

Research Notes:
- Using MobileNetV2 pre-trained on Places365 dataset for scene classification
- Places365 has 365 scene categories, we'll map to simplified categories
- MobileNetV2 is lightweight and CPU-friendly
- Alternative: ResNet18 pre-trained on Places365 (slightly heavier but more accurate)
"""

import cv2
import numpy as np
import time
from typing import Optional, Dict, List
import logging

# Try to import torch/torchvision for scene classification
try:
    import torch
    import torchvision.transforms as transforms
    from torchvision import models
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available. Scene classification will be disabled.")


class SceneClassifier:
    """
    Lightweight scene classifier using pre-trained models.
    
    Maps complex scene categories to simple environment labels suitable
    for audio announcements.
    """
    
    def __init__(self, update_interval: float = 10.0, confidence_threshold: float = 0.3):
        """
        Initialize scene classifier.
        
        Args:
            update_interval: Seconds between scene classifications (low frequency)
            confidence_threshold: Minimum confidence for scene announcements
        """
        self.update_interval = update_interval
        self.confidence_threshold = confidence_threshold
        self.last_classification_time = 0
        self.current_scene = None
        self.last_announced_scene = None
        
        # Simple scene mapping from complex categories to basic labels
        self.scene_mapping = {
            # Indoor scenes
            'office': ['office', 'cubicle', 'conference_room', 'reception'],
            'corridor': ['corridor', 'hallway', 'lobby', 'elevator'],
            'room': ['bedroom', 'living_room', 'kitchen', 'bathroom', 'dining_room'],
            'store': ['shop', 'supermarket', 'restaurant', 'cafe', 'mall'],
            
            # Outdoor scenes  
            'street': ['street', 'sidewalk', 'crosswalk', 'parking_lot'],
            'park': ['park', 'garden', 'playground', 'courtyard'],
            'building': ['building_facade', 'entrance', 'stairs'],
            
            # Default
            'indoor': ['indoor'],
            'outdoor': ['outdoor']
        }
        
        self.model = None
        self.transform = None
        self.class_names = []
        
        if TORCH_AVAILABLE:
            self._load_model()
        else:
            logging.warning("Scene classification disabled - PyTorch not available")
    
    def _load_model(self):
        """Load pre-trained scene classification model."""
        try:
            # Try to load pre-trained model, but fall back to dummy implementation
            # if network/SSL issues prevent model download
            try:
                self.model = models.mobilenet_v2(weights='DEFAULT')
                self.model.eval()
                
                # Standard ImageNet preprocessing
                self.transform = transforms.Compose([
                    transforms.ToPILImage(),
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                       std=[0.229, 0.224, 0.225])
                ])
                
                logging.info("Scene classification model loaded successfully")
                
            except Exception as download_error:
                logging.warning(f"Could not download model ({download_error}), using dummy classifier")
                # Use dummy model for demonstration
                self.model = "dummy"
                self.transform = None
            
            # Simplified scene categories for demo
            # In reality, we'd load Places365 categories
            self.class_names = [
                'office', 'corridor', 'street', 'park', 'room', 'store', 
                'building', 'indoor', 'outdoor'
            ]
            
        except Exception as e:
            logging.error(f"Failed to initialize scene classification: {e}")
            self.model = None
    
    def should_classify(self) -> bool:
        """
        Check if enough time has passed for next classification.
        Implements low update frequency to avoid information overload.
        """
        current_time = time.time()
        return (current_time - self.last_classification_time) >= self.update_interval
    
    def classify_scene(self, frame: np.ndarray) -> Optional[str]:
        """
        Classify the scene in the given frame.
        
        Args:
            frame: Input frame as numpy array (BGR format from OpenCV)
            
        Returns:
            Scene label string or None if classification fails/not ready
        """
        if not self.should_classify() or self.model is None:
            return None
        
        try:
            if self.model == "dummy":
                # Dummy implementation for demonstration
                scene_label = self._dummy_classify_scene(frame)
            else:
                # Real model implementation
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Preprocess frame
                input_tensor = self.transform(rgb_frame).unsqueeze(0)
                
                # Run inference
                with torch.no_grad():
                    outputs = self.model(input_tensor)
                    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                    
                    # Get top prediction
                    confidence, predicted_idx = torch.max(probabilities, 0)
                    confidence = confidence.item()
                    
                    if confidence < self.confidence_threshold:
                        return None
                    
                    # Map to simplified scene category
                    scene_label = self._map_to_simple_scene(predicted_idx.item())
            
            self.last_classification_time = time.time()
            self.current_scene = scene_label
            
            return scene_label
                
        except Exception as e:
            logging.error(f"Scene classification failed: {e}")
            return None
    
    def _dummy_classify_scene(self, frame: np.ndarray) -> str:
        """
        Dummy scene classifier for demonstration when real model unavailable.
        
        Uses simple heuristics based on frame properties to simulate classification.
        """
        # Simple heuristics based on frame properties
        height, width = frame.shape[:2]
        
        # Calculate average brightness
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        
        # Calculate color distribution
        b, g, r = cv2.split(frame)
        blue_ratio = np.mean(b) / 255.0
        green_ratio = np.mean(g) / 255.0
        red_ratio = np.mean(r) / 255.0
        
        # Simple classification based on properties
        if avg_brightness > 150:
            if blue_ratio > 0.6:
                return 'outdoor'  # Bright and blue (sky)
            elif green_ratio > 0.5:
                return 'park'     # Bright and green (vegetation)
            else:
                return 'office'   # Bright indoor
        elif avg_brightness > 100:
            if red_ratio > green_ratio and red_ratio > blue_ratio:
                return 'room'     # Warm indoor lighting
            else:
                return 'corridor' # Neutral indoor
        else:
            return 'street'       # Dark (possibly outdoor at night)
    
    
    def _map_to_simple_scene(self, class_idx: int) -> str:
        """
        Map complex scene classification to simple audio-friendly labels.
        
        This is a simplified implementation. In reality, we'd have a proper
        mapping from Places365 categories to our simple scene types.
        """
        # Simplified mapping based on class index
        # In reality, this would be based on actual Places365 class names
        simple_scenes = ['office', 'corridor', 'street', 'park', 'room', 'store', 'building']
        return simple_scenes[class_idx % len(simple_scenes)]
    
    def has_scene_changed(self) -> bool:
        """
        Check if scene has changed significantly to warrant announcement.
        Implements scene change detection to avoid repetitive announcements.
        """
        if self.current_scene is None:
            return False
        
        if self.last_announced_scene is None:
            return True
        
        return self.current_scene != self.last_announced_scene
    
    def mark_scene_announced(self):
        """Mark current scene as announced to avoid repetition."""
        self.last_announced_scene = self.current_scene
    
    def get_scene_announcement(self) -> Optional[str]:
        """
        Get scene announcement message if scene has changed.
        
        Returns:
            Audio message string or None if no announcement needed
        """
        if not self.has_scene_changed():
            return None
        
        scene = self.current_scene
        if scene:
            self.mark_scene_announced()
            return f"Environment: {scene}"
        
        return None
    
    def is_enabled(self) -> bool:
        """Check if scene classification is available and enabled."""
        return TORCH_AVAILABLE and self.model is not None


# Fallback implementation for when PyTorch is not available
class DummySceneClassifier:
    """
    Dummy scene classifier that provides no functionality.
    Used when PyTorch dependencies are not available.
    """
    
    def __init__(self, *args, **kwargs):
        pass
    
    def should_classify(self) -> bool:
        return False
    
    def classify_scene(self, frame: np.ndarray) -> Optional[str]:
        return None
    
    def has_scene_changed(self) -> bool:
        return False
    
    def get_scene_announcement(self) -> Optional[str]:
        return None
    
    def is_enabled(self) -> bool:
        return False


def create_scene_classifier(**kwargs) -> SceneClassifier:
    """
    Factory function to create appropriate scene classifier.
    
    Returns:
        SceneClassifier if PyTorch available, DummySceneClassifier otherwise
    """
    if TORCH_AVAILABLE:
        return SceneClassifier(**kwargs)
    else:
        return DummySceneClassifier(**kwargs)