import os
import platform

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
TARGET_CLASSES = {
    0: "person",
    56: "chair", 
    2: "car",
    # Door will need custom mapping as it's not in standard COCO
}

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