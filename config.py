import os
import platform
import json
import logging

# Platform detection
PLATFORM = platform.system()
IS_WINDOWS = PLATFORM == "Windows"
IS_MACOS = PLATFORM == "Darwin"

# Object detection configuration
CONFIDENCE_THRESHOLD = 0.5
PROXIMITY_THRESHOLD = 0.15  # 15% of frame area
ALERT_COOLDOWN_SECONDS = 5
CAMERA_INDEX = 0

# Target object classes (COCO class IDs)
# Can be overridden via TARGET_CLASSES environment variable as JSON
# Example: export TARGET_CLASSES='{"0":"person","56":"chair","2":"car","62":"door"}'
DEFAULT_TARGET_CLASSES = {
    0: "person",
    56: "chair", 
    2: "car",
    # Door will need custom mapping as it's not in standard COCO
}

# Load target classes from environment or use defaults
try:
    target_classes_json = os.getenv('TARGET_CLASSES')
    if target_classes_json:
        TARGET_CLASSES = {int(k): v for k, v in json.loads(target_classes_json).items()}
    else:
        TARGET_CLASSES = DEFAULT_TARGET_CLASSES
except (json.JSONDecodeError, ValueError) as e:
    logging.warning(f"Failed to parse TARGET_CLASSES from environment: {e}. Using defaults.")
    TARGET_CLASSES = DEFAULT_TARGET_CLASSES

# TTS configuration based on platform
if IS_WINDOWS:
    TTS_ENGINE = "sapi5"  # Windows SAPI
    SPEECH_RATE = 200
elif IS_MACOS:
    TTS_ENGINE = "nsss"   # macOS built-in
    SPEECH_RATE = 200
else:
    TTS_ENGINE = "espeak"  # Linux fallback
    SPEECH_RATE = 150

# OCR configuration
OCR_TRIGGER_KEY = 'space'  # Spacebar to trigger OCR
OCR_TIMEOUT_SECONDS = 10
MIN_TEXT_LENGTH = 3
OCR_PROCESSING_COOLDOWN = 2.0  # Minimum seconds between OCR requests

# Environment variables
TEST_DATA_PATH = os.getenv('TEST_DATA_PATH', 'test_data/')
ENABLE_LOGGING = os.getenv('ENABLE_LOGGING', 'false').lower() == 'true'
ENABLE_FRAME_SAVING = os.getenv('ENABLE_FRAME_SAVING', 'false').lower() == 'true'

# Alert messages
ALERT_MESSAGES = {
    'person': 'Person ahead',
    'chair': 'Chair detected', 
    'car': 'Car nearby',
    'door': 'Door detected'
}

# Scene classification configuration
ENABLE_SCENE_CLASSIFICATION = os.getenv('ENABLE_SCENE_CLASSIFICATION', 'true').lower() == 'true'
SCENE_UPDATE_INTERVAL = 15.0  # Seconds between scene classifications (low frequency)
SCENE_CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence for scene announcements
SCENE_ANNOUNCEMENT_FORMAT = "Environment: {scene}"

# Performance settings
FRAME_SKIP = 3  # Process every 3rd frame for performance
MAX_DETECTION_LATENCY_MS = 500
MAX_OCR_LATENCY_SECONDS = 10

# GPU support detection
try:
    import torch
    USE_GPU = torch.cuda.is_available()
    DEVICE = 'cuda' if USE_GPU else 'cpu'
    GPU_AVAILABLE = USE_GPU
except ImportError:
    USE_GPU = False
    DEVICE = 'cpu'
    GPU_AVAILABLE = False


def validate_config():
    """
    Validate configuration values to ensure they are within acceptable ranges.
    
    Raises:
        AssertionError: If any configuration value is invalid
    """
    # Validate confidence threshold
    assert 0.0 <= CONFIDENCE_THRESHOLD <= 1.0, \
        f"CONFIDENCE_THRESHOLD must be between 0 and 1, got {CONFIDENCE_THRESHOLD}"
    
    # Validate proximity threshold
    assert 0.0 <= PROXIMITY_THRESHOLD <= 1.0, \
        f"PROXIMITY_THRESHOLD must be between 0 and 1, got {PROXIMITY_THRESHOLD}"
    
    # Validate scene confidence threshold
    assert 0.0 <= SCENE_CONFIDENCE_THRESHOLD <= 1.0, \
        f"SCENE_CONFIDENCE_THRESHOLD must be between 0 and 1, got {SCENE_CONFIDENCE_THRESHOLD}"
    
    # Validate positive integers
    assert FRAME_SKIP > 0, f"FRAME_SKIP must be positive, got {FRAME_SKIP}"
    assert ALERT_COOLDOWN_SECONDS > 0, f"ALERT_COOLDOWN_SECONDS must be positive, got {ALERT_COOLDOWN_SECONDS}"
    assert CAMERA_INDEX >= 0, f"CAMERA_INDEX must be non-negative, got {CAMERA_INDEX}"
    assert SPEECH_RATE > 0, f"SPEECH_RATE must be positive, got {SPEECH_RATE}"
    assert MIN_TEXT_LENGTH > 0, f"MIN_TEXT_LENGTH must be positive, got {MIN_TEXT_LENGTH}"
    assert OCR_PROCESSING_COOLDOWN > 0, f"OCR_PROCESSING_COOLDOWN must be positive, got {OCR_PROCESSING_COOLDOWN}"
    assert SCENE_UPDATE_INTERVAL > 0, f"SCENE_UPDATE_INTERVAL must be positive, got {SCENE_UPDATE_INTERVAL}"
    
    # Validate latency limits
    assert MAX_DETECTION_LATENCY_MS > 0, f"MAX_DETECTION_LATENCY_MS must be positive, got {MAX_DETECTION_LATENCY_MS}"
    assert MAX_OCR_LATENCY_SECONDS > 0, f"MAX_OCR_LATENCY_SECONDS must be positive, got {MAX_OCR_LATENCY_SECONDS}"
    
    # Validate target classes
    assert isinstance(TARGET_CLASSES, dict), "TARGET_CLASSES must be a dictionary"
    assert len(TARGET_CLASSES) > 0, "TARGET_CLASSES must not be empty"
    
    # Validate alert messages
    assert isinstance(ALERT_MESSAGES, dict), "ALERT_MESSAGES must be a dictionary"
    
    return True


# Run validation on import
try:
    validate_config()
except AssertionError as e:
    logging.error(f"Configuration validation failed: {e}")
    raise