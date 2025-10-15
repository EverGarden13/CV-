"""
Scene Classification Integration Module

This module demonstrates how to integrate scene classification into the main
VisionMate-Lite application loop. It handles the coordination between scene
classification, change detection, and audio announcements.
"""

import logging
import time
from typing import Optional
import numpy as np

from .scene_classifier import create_scene_classifier, SceneClassifier
from .audio import AudioManager


class SceneIntegration:
    """
    Integrates scene classification with the main application.
    
    Handles scene classification timing, change detection, and audio announcements
    while maintaining low update frequency to avoid information overload.
    """
    
    def __init__(self, audio_manager: AudioManager, 
                 update_interval: float = 15.0,
                 confidence_threshold: float = 0.3,
                 enabled: bool = True):
        """
        Initialize scene integration.
        
        Args:
            audio_manager: AudioManager instance for announcements
            update_interval: Seconds between scene classifications (default: 15s)
            confidence_threshold: Minimum confidence for announcements
            enabled: Whether scene classification is enabled
        """
        self.audio_manager = audio_manager
        self.enabled = enabled
        self.logger = logging.getLogger(__name__)
        
        # Initialize scene classifier
        self.scene_classifier = create_scene_classifier(
            update_interval=update_interval,
            confidence_threshold=confidence_threshold
        )
        
        # Check if scene classification is actually available
        if not self.scene_classifier.is_enabled():
            self.enabled = False
            self.logger.warning("Scene classification disabled - dependencies not available")
        
        self.logger.info(f"Scene integration initialized (enabled: {self.enabled})")
    
    def process_frame(self, frame: np.ndarray) -> Optional[str]:
        """
        Process frame for scene classification and handle announcements.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Scene label if classified and announced, None otherwise
        """
        if not self.enabled:
            return None
        
        try:
            # Classify scene (respects internal timing)
            scene = self.scene_classifier.classify_scene(frame)
            
            if scene:
                self.logger.debug(f"Scene classified as: {scene}")
                
                # Check if scene has changed and needs announcement
                announcement = self.scene_classifier.get_scene_announcement()
                
                if announcement:
                    self.logger.info(f"Scene changed, announcing: {scene}")
                    
                    # Make announcement if audio is available
                    if not self.audio_manager.is_busy():
                        success = self.audio_manager.speak_scene(scene)
                        if success:
                            return scene
                        else:
                            self.logger.warning("Failed to announce scene change")
                    else:
                        self.logger.debug("Audio busy, skipping scene announcement")
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in scene processing: {e}")
            return None
    
    def is_enabled(self) -> bool:
        """Check if scene classification is enabled and available."""
        return self.enabled and self.scene_classifier.is_enabled()
    
    def get_current_scene(self) -> Optional[str]:
        """Get the current scene label without processing."""
        if not self.enabled:
            return None
        return self.scene_classifier.current_scene
    
    def force_scene_update(self, frame: np.ndarray) -> Optional[str]:
        """
        Force a scene classification update regardless of timing.
        Useful for testing or manual triggers.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Scene label if classified, None otherwise
        """
        if not self.enabled:
            return None
        
        try:
            # Temporarily override timing
            old_time = self.scene_classifier.last_classification_time
            self.scene_classifier.last_classification_time = 0
            
            # Classify scene
            scene = self.scene_classifier.classify_scene(frame)
            
            # Restore timing
            self.scene_classifier.last_classification_time = old_time
            
            return scene
            
        except Exception as e:
            self.logger.error(f"Error in forced scene update: {e}")
            return None


def demo_scene_integration():
    """
    Demo function showing how scene integration works.
    This would typically be called from the main application loop.
    """
    print("Scene Integration Demo")
    print("=" * 40)
    
    # Initialize components
    audio_manager = AudioManager()
    scene_integration = SceneIntegration(audio_manager, update_interval=5.0)  # Faster for demo
    
    if not scene_integration.is_enabled():
        print("Scene classification not available - missing dependencies")
        return
    
    print(f"Scene integration enabled: {scene_integration.is_enabled()}")
    
    # Simulate processing frames
    print("\nSimulating frame processing...")
    
    # Create dummy frames (in reality these would come from camera)
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    for i in range(3):
        print(f"\nProcessing frame {i+1}...")
        
        # Process frame for scene classification
        announced_scene = scene_integration.process_frame(dummy_frame)
        
        if announced_scene:
            print(f"Scene announced: {announced_scene}")
        else:
            current_scene = scene_integration.get_current_scene()
            if current_scene:
                print(f"Current scene: {current_scene} (no announcement)")
            else:
                print("No scene detected")
        
        # Wait a bit between frames
        time.sleep(2)
    
    # Test forced update
    print("\nTesting forced scene update...")
    forced_scene = scene_integration.force_scene_update(dummy_frame)
    if forced_scene:
        print(f"Forced scene classification: {forced_scene}")
    else:
        print("Forced scene classification failed")
    
    # Cleanup
    audio_manager.cleanup()
    print("\nScene integration demo complete")


if __name__ == "__main__":
    demo_scene_integration()