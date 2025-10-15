"""
Audio management module for VisionMate-Lite.
Provides cross-platform text-to-speech functionality for object detection alerts and OCR text reading.
"""

import pyttsx3
import platform
import threading
import time
from typing import Dict, Optional


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
        
        self._initialize_engine()
    
    def _initialize_engine(self) -> None:
        """Initialize pyttsx3 engine with platform-specific settings."""
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
            
        except Exception as e:
            print(f"Warning: Failed to initialize TTS engine: {e}")
            self.engine = None
    
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
        Speak an alert message for detected objects.
        
        Args:
            object_class: The class name of the detected object
            
        Returns:
            True if alert was spoken successfully, False otherwise
        """
        if not self.engine:
            print(f"TTS engine not available. Alert: {object_class}")
            return False
        
        # Don't interrupt if already speaking
        if self.is_busy():
            return False
        
        # Get alert message for the object class
        message = self.ALERT_MESSAGES.get(object_class, f"{object_class} detected")
        
        try:
            self.engine.say(message)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking alert: {e}")
            return False
    
    def speak_text(self, text: str) -> bool:
        """
        Speak the provided text (typically from OCR).
        
        Args:
            text: The text to be spoken
            
        Returns:
            True if text was spoken successfully, False otherwise
        """
        if not self.engine:
            print(f"TTS engine not available. Text: {text}")
            return False
        
        # Don't interrupt if already speaking
        if self.is_busy():
            return False
        
        # Clean up text for better speech
        cleaned_text = text.strip()
        if not cleaned_text:
            cleaned_text = "No text found"
        
        try:
            self.engine.say(cleaned_text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error speaking text: {e}")
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
        """Clean up resources."""
        if self.engine:
            try:
                self.stop_speaking()
                # Give time for cleanup
                time.sleep(0.1)
            except Exception as e:
                print(f"Error during cleanup: {e}")


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
    
    # Test is_busy functionality
    print("Testing is_busy method...")
    print(f"Is busy: {audio_manager.is_busy()}")
    
    audio_manager.cleanup()
    print("AudioManager test complete.")


if __name__ == "__main__":
    test_audio_manager()