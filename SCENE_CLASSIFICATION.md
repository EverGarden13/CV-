# Scene Classification Feature

## Overview

The scene classification feature provides optional environment labeling for VisionMate-Lite. It classifies the current scene into basic categories like "office", "corridor", "street", etc., and announces changes at low frequency to avoid information overload.

## Features

- **Lightweight Classification**: Uses CPU-friendly models suitable for real-time processing
- **Low Update Frequency**: Classifications occur every 15 seconds by default to avoid noise
- **Scene Change Detection**: Only announces when the scene actually changes
- **Audio Integration**: Seamlessly integrates with the existing audio management system
- **Fallback Support**: Works even when PyTorch models can't be downloaded

## Supported Scene Categories

- **office**: Office spaces, cubicles, conference rooms
- **corridor**: Hallways, lobbies, elevators
- **room**: Living rooms, bedrooms, kitchens
- **store**: Shops, restaurants, cafes
- **street**: Streets, sidewalks, parking lots
- **park**: Parks, gardens, outdoor spaces
- **building**: Building facades, entrances
- **indoor/outdoor**: General indoor/outdoor classification

## Configuration

Scene classification can be configured in `config.py`:

```python
# Scene classification configuration
ENABLE_SCENE_CLASSIFICATION = True  # Enable/disable feature
SCENE_UPDATE_INTERVAL = 15.0        # Seconds between classifications
SCENE_CONFIDENCE_THRESHOLD = 0.3    # Minimum confidence for announcements
```

## Usage

### Basic Integration

```python
from src.audio import AudioManager
from src.scene_integration import SceneIntegration

# Initialize components
audio_manager = AudioManager()
scene_integration = SceneIntegration(audio_manager)

# Process frames in main loop
while True:
    frame = camera.get_frame()
    
    # Scene classification happens automatically at low frequency
    announced_scene = scene_integration.process_frame(frame)
    
    if announced_scene:
        print(f"Scene changed to: {announced_scene}")
```

### Manual Scene Classification

```python
# Force immediate scene classification
scene = scene_integration.force_scene_update(frame)
print(f"Current scene: {scene}")
```

## Implementation Details

### Model Architecture

- **Primary**: MobileNetV2 pre-trained on Places365 dataset
- **Fallback**: Dummy classifier using image properties (brightness, color distribution)
- **CPU Optimized**: Designed for real-time inference without GPU

### Change Detection

The system implements intelligent change detection to avoid repetitive announcements:

1. Scene is classified at configurable intervals (default: 15 seconds)
2. New scene is compared with previously announced scene
3. Announcement only occurs if scene has actually changed
4. Confidence threshold prevents low-confidence classifications

### Audio Integration

Scene announcements use the format: "Environment: {scene_name}"

Examples:
- "Environment: office"
- "Environment: corridor" 
- "Environment: street"

## Testing

Run the scene classification tests:

```bash
python3 test_scene_classification.py
```

This will test:
- Basic scene classifier functionality
- Audio integration
- Full scene integration module
- Optional real camera testing

## Dependencies

### Required
- OpenCV (cv2)
- NumPy
- Python logging

### Optional (for full functionality)
- PyTorch
- torchvision

If PyTorch is not available, the system falls back to a dummy classifier that still demonstrates the feature.

## Performance

- **Classification Latency**: ~100-300ms per frame (CPU)
- **Memory Usage**: ~50-100MB additional (with PyTorch model)
- **Update Frequency**: Configurable, default 15 seconds
- **CPU Impact**: Minimal due to low update frequency

## Limitations

1. **Simplified Categories**: Limited to basic scene types suitable for navigation
2. **CPU Only**: No GPU acceleration implemented
3. **Indoor Focus**: Better performance on indoor scenes
4. **Lighting Dependent**: Performance varies with lighting conditions
5. **No Custom Training**: Uses pre-trained models only

## Future Enhancements

- Custom scene categories for specific environments
- Integration with object detection for context-aware classification
- Adaptive update frequency based on scene stability
- Multi-language scene announcements
- Integration with navigation assistance

## Troubleshooting

### Scene Classification Not Working

1. Check if PyTorch is installed: `pip install torch torchvision`
2. Verify configuration: `ENABLE_SCENE_CLASSIFICATION = True`
3. Check logs for SSL/download issues (fallback will be used)

### No Scene Announcements

1. Verify audio system is working
2. Check confidence threshold (lower if needed)
3. Ensure sufficient time has passed (default 15 seconds)
4. Verify scene has actually changed

### Poor Classification Accuracy

1. Ensure good lighting conditions
2. Point camera at representative scene areas
3. Consider adjusting confidence threshold
4. Check if fallback dummy classifier is being used

## Integration with Main Application

The scene classification feature is designed to integrate seamlessly with the main VisionMate-Lite application loop. It operates independently of object detection and OCR, providing complementary environmental context.

See `src/scene_integration.py` for the main integration interface.