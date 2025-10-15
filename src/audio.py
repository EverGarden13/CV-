"""
Audio management module for VisionMate-Lite.
Provides cross-platform text-to-speech functionality for object detection alerts and OCR text reading.
"""

import pyttsx3
import platform
import threading
import time
import logging
from typing import Dict, Optional
from .error_handler import get_error_handler, get_graceful_shutdown


class AudioManager:
    """
    Cross-platform audio manager using pyttsx3 for text-to-speech functionality.
    Supports Windows SAPI and macOS built-in TTS engines.
    """
    
    # Simple alert message mapping for each object class
    ALERT_MESSAGES: Dict[str, str] = {
        'person': 'Person ahead',
        'chair': 'Chair detected',
        'car': 'Car nearby',
        'door': 'Door detected'
    }
    
    # Scene announcement message format
    SCENE_MESSAGE_FORMAT = "Environment: {scene}"
    
    def __init__(self, speech_rate: int = 200):
        """
        Initialize the AudioManager with platform-specific TTS engine.
        
        Args:
            speech_rate: Speech rate in words per minute (default: 200)
        """
        self.engine: Optional[pyttsx3.Engine] = None
        self.speech_rate = speech_rate
        self._is_speaking = False
        self._speech_lock = threading.Lock()
        self._use_fallback = False
        self.logger = logging.getLogger(__name__)
        
        self._initialize_engine()
    
    def _initialize_engine(self) -> None:
        """Initialize pyttsx3 engine with platform-specific settings and error handling."""
        error_handler = get_error_handler()
        
        try:
            self.engine = pyttsx3.init()
            
            # Set speech rate
            self.engine.setProperty('rate', self.speech_rate)
            
            # Platform-specific voice configuration
            system = platform.system()
            if system == "Windows":
                # Use Windows SAPI
                voices = self.engine.getProperty('voices')
                if voices:
                    # Use first available voice (typically Microsoft voices)
                    self.engine.setProperty('voice', voices[0].id)
            elif system == "Darwin":  # macOS
                # Use macOS built-in TTS
                voices = self.engine.getProperty('voices')
                if voices:
                    # Use default macOS voice
                    self.engine.setProperty('voice', voices[0].id)
            
            # Set up callbacks to track speaking state
            self.engine.connect('started-utterance', self._on_speech_start)
            self.engine.connect('finished-utterance', self._on_speech_end)
            
            # Register cleanup with shutdown handler
            shutdown_handler = get_graceful_shutdown()
            shutdown_handler.register_shutdown_handler(self.cleanup)
            
        except Exception as e:
            print(f"Warning: Failed to initialize TTS engine: {e}")
            
            # Try error recovery
            context = {"platform": platform.system()}
            if error_handler.handle_error("tts_error", e, context):
                recovered_tts = context.get("recovered_tts")
                if recovered_tts:
                    self.engine = recovered_tts
                    print("TTS engine recovery successful")
                else:
                    # Use fallback mode
                    self.engine = None
                    self._use_fallback = True
                    print("Using fallback mode for audio output")
            else:
                self.engine = None
                self._use_fallback = True
    
    def _on_speech_start(self, name: str) -> None:
        """Callback when speech starts."""
        with self._speech_lock:
            self._is_speaking = True
    
    def _on_speech_end(self, name: str, completed: bool) -> None:
        """Callback when speech ends."""
        with self._speech_lock:
            self._is_speaking = False
    
    def is_busy(self) -> bool:
        """
        Check if TTS is currently speaking.
        
        Returns:
            True if TTS is currently speaking, False otherwise
        """
        with self._speech_lock:
            return self._is_speaking
    
    def speak_alert(self, object_class: str) -> bool:
        """
        Speak an alert message for detected objects with error handling.
        
        Args:
            object_class: The class name of the detected object
            
        Returns:
            True if alert was spoken successfully, False otherwise
        """
        # Get alert message for the object class
        message = self.ALERT_MESSAGES.get(object_class, f"{object_class} detected")
        
        if not self.engine or self._use_fallback:
            # Use fallback output
            print(f"AUDIO ALERT: {message}")
            self.logger.info(f"Audio alert (fallback): {message}")
            return True
        
        # Don't interrupt if already speaking
        if self.is_busy():
            return False
        
        error_handler = get_error_handler()
        
        try:
            self.engine.say(message)
            self.engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"Error speaking alert: {e}")
            
            # Try error recovery
            context = {"message": message, "type": "alert"}
            if error_handler.handle_error("tts_error", e, context):
                # Try fallback
                print(f"AUDIO ALERT: {message}")
                self.logger.info(f"Audio alert (fallback after error): {message}")
                return True
            
            return False
    
    def speak_text(self, text: str) -> bool:
        """
        Speak the provided text (typically from OCR) with error handling.
        
        Args:
            text: The text to be spoken
            
        Returns:
            True if text was spoken successfully, False otherwise
        """
        # Clean up text for better speech
        cleaned_text = text.strip()
        if not cleaned_text:
            cleaned_text = "No text found"
        
        if not self.engine or self._use_fallback:
            # Use fallback output
            print(f"AUDIO TEXT: {cleaned_text}")
            self.logger.info(f"Audio text (fallback): {cleaned_text[:100]}...")
            return True
        
        # Don't interrupt if already speaking
        if self.is_busy():
            return False
        
        error_handler = get_error_handler()
        
        try:
            self.engine.say(cleaned_text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"Error speaking text: {e}")
            
            # Try error recovery
            context = {"text": cleaned_text[:100], "type": "text"}
            if error_handler.handle_error("tts_error", e, context):
                # Try fallback
                print(f"AUDIO TEXT: {cleaned_text}")
                self.logger.info(f"Audio text (fallback after error): {cleaned_text[:100]}...")
                return True
            
            return False
    
    def speak_scene(self, scene: str) -> bool:
        """
        Speak a scene classification announcement with error handling.
        
        Args:
            scene: The scene/environment label to announce
            
        Returns:
            True if scene was announced successfully, False otherwise
        """
        message = self.SCENE_MESSAGE_FORMAT.format(scene=scene)
        
        if not self.engine or self._use_fallback:
            # Use fallback output
            print(f"AUDIO SCENE: {message}")
            self.logger.info(f"Audio scene (fallback): {message}")
            return True
        
        # Don't interrupt if already speaking
        if self.is_busy():
            return False
        
        error_handler = get_error_handler()
        
        try:
            self.engine.say(message)
            self.engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"Error speaking scene: {e}")
            
            # Try error recovery
            context = {"message": message, "type": "scene"}
            if error_handler.handle_error("tts_error", e, context):
                # Try fallback
                print(f"AUDIO SCENE: {message}")
                self.logger.info(f"Audio scene (fallback after error): {message}")
                return True
            
            return False
    
    def stop_speaking(self) -> None:
        """Stop current speech if speaking."""
        if self.engine and self.is_busy():
            try:
                self.engine.stop()
            except Exception as e:
                print(f"Error stopping speech: {e}")
    
    def set_speech_rate(self, rate: int) -> None:
        """
        Update the speech rate.
        
        Args:
            rate: New speech rate in words per minute
        """
        if self.engine:
            try:
                self.engine.setProperty('rate', rate)
                self.speech_rate = rate
            except Exception as e:
                print(f"Error setting speech rate: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources with comprehensive error handling."""
        try:
            if self.engine:
                self.logger.info("Cleaning up audio manager...")
                self.stop_speaking()
                # Give time for cleanup
                time.sleep(0.1)
                
                # Try to properly shutdown the engine
                try:
                    self.engine.stop()
                except:
                    pass  # Ignore errors during shutdown
                
                self.engine = None
                self.logger.info("Audio manager cleanup complete")
        except Exception as e:
            self.logger.error(f"Error during audio cleanup: {e}")


# Convenience function for quick testing
def test_audio_manager():
    """Test function to verify AudioManager functionality."""
    print("Testing AudioManager...")
    
    audio_manager = AudioManager()
    
    # Test alert messages
    print("Testing alert messages...")
    for object_class in AudioManager.ALERT_MESSAGES.keys():
        print(f"Speaking alert for: {object_class}")
        audio_manager.speak_alert(object_class)
        time.sleep(1)  # Brief pause between alerts
    
    # Test text reading
    print("Testing text reading...")
    test_text = "This is a test of the OCR text reading functionality."
    audio_manager.speak_text(test_text)
    
    # Test scene announcements
    print("Testing scene announcements...")
    test_scenes = ["office", "corridor", "street", "park"]
    for scene in test_scenes:
        print(f"Speaking scene: {scene}")
        audio_manager.speak_scene(scene)
        time.sleep(1)  # Brief pause between announcements
    
    # Test is_busy functionality
    print("Testing is_busy method...")
    print(f"Is busy: {audio_manager.is_busy()}")
    
    audio_manager.cleanup()
    print("AudioManager test complete.")


if __name__ == "__main__":
    test_audio_manager()