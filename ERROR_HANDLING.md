# Error Handling and Troubleshooting Guide

VisionMate-Lite includes comprehensive error handling and graceful degradation features to ensure reliable operation even when components fail.

## System Validation

Before running the application, validate your system setup:

```bash
python validate_system.py
```

This will check:
- Platform compatibility (Windows/macOS preferred)
- Camera access and permissions
- Tesseract OCR installation
- Text-to-speech engine availability
- YOLO model loading
- Required directories and permissions

## Error Handling Features

### 1. Startup Validation
- Comprehensive dependency checking
- Clear error messages with installation instructions
- Graceful fallback when non-critical components fail

### 2. Camera Error Handling
- Automatic retry with different camera indices
- Recovery from temporary camera disconnections
- Graceful degradation when camera becomes unavailable

### 3. Model Loading Recovery
- Automatic model reloading on failures
- Fallback to alternative model configurations
- Clear error reporting for model issues

### 4. Audio System Fallback
- Automatic fallback to text output when TTS fails
- Cross-platform TTS engine selection
- Recovery from audio device issues

### 5. OCR Error Recovery
- Retry with simpler OCR configurations
- Image preprocessing adjustments
- Clear user feedback for OCR failures

### 6. Privacy Safeguards
- Frame logging disabled by default
- User control over debug frame saving
- Clear privacy status reporting

## Environment Variables

Control error handling behavior with these environment variables:

```bash
# Enable debug frame saving (disabled by default for privacy)
export ENABLE_FRAME_SAVING=true

# Enable detailed logging
export ENABLE_LOGGING=true

# Set custom test data path
export TEST_DATA_PATH=/path/to/test/data

# Enable debug mode
export DEBUG_MODE=true
```

## Common Issues and Solutions

### Camera Issues

**Problem**: "Cannot access camera - check permissions and availability"
**Solutions**:
- Check camera permissions in system settings
- Close other applications using the camera
- Try different camera indices (0, 1, 2)
- Restart the application

**Problem**: "Camera accessible but cannot capture frames"
**Solutions**:
- Check camera drivers
- Try different camera resolutions
- Restart the camera service

### OCR Issues

**Problem**: "Tesseract OCR not found"
**Solutions**:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

**Problem**: "OCR processing failed"
**Solutions**:
- Ensure better lighting conditions
- Move closer to text
- Check text clarity and contrast
- Try different text orientations

### Audio Issues

**Problem**: "TTS engine not available"
**Solutions**:
- Check system audio settings
- Verify pyttsx3 installation: `pip install pyttsx3`
- Use fallback text output mode
- Check audio device availability

### Model Loading Issues

**Problem**: "Could not initialize YOLOv8 model"
**Solutions**:
- Check internet connection (for first-time download)
- Verify ultralytics installation: `pip install ultralytics`
- Clear model cache and retry
- Check available disk space

## Graceful Shutdown

The application handles shutdown gracefully:
- **Ctrl+C**: Initiates graceful shutdown
- **ESC or Q**: Quit from main loop
- Automatic resource cleanup
- Proper camera and audio resource release

## Privacy Controls

### Frame Logging
By default, no frames are saved to disk for privacy. To enable debug frame saving:

```bash
export ENABLE_FRAME_SAVING=true
python main.py
```

### Clearing Debug Data
To clear any saved debug frames:

```python
from src.error_handler import get_privacy_manager
privacy_manager = get_privacy_manager()
privacy_manager.clear_saved_frames()
```

## Error Recovery Strategies

### Automatic Recovery
- Camera reconnection attempts
- Model reloading on failures
- TTS engine reinitialization
- OCR configuration adjustments

### Fallback Modes
- Text output when TTS fails
- Simplified OCR when advanced processing fails
- Continue operation with reduced functionality

### User Feedback
- Clear error messages
- Suggested solutions
- Status indicators in UI
- Comprehensive logging

## Monitoring and Debugging

### Error Tracking
The system tracks error counts and provides summaries:
- Error counts by type
- Recovery success rates
- Performance impact assessment

### Debug Information
Enable detailed logging for troubleshooting:

```bash
export ENABLE_LOGGING=true
python main.py
```

### System Status
Check system status during runtime:
- Camera connection status
- Model loading status
- Audio system availability
- OCR engine status

## Performance Considerations

### Error Handling Overhead
- Minimal performance impact
- Efficient error detection
- Quick recovery mechanisms
- Resource-conscious fallbacks

### Memory Management
- Automatic cleanup on errors
- Resource leak prevention
- Graceful degradation under memory pressure

## Support and Troubleshooting

### Log Analysis
Check logs for detailed error information:
- Error types and frequencies
- Recovery attempts and success rates
- Performance metrics
- System resource usage

### System Information
The validation script provides comprehensive system information:
- Platform details
- Dependency versions
- Hardware capabilities
- Configuration status

### Getting Help
1. Run system validation: `python validate_system.py`
2. Check error logs for specific issues
3. Verify environment variable settings
4. Test individual components separately
5. Review privacy and security settings

## Best Practices

### Development
- Test error conditions regularly
- Validate recovery mechanisms
- Monitor resource usage
- Implement comprehensive logging

### Deployment
- Run system validation before deployment
- Configure appropriate privacy settings
- Set up monitoring and alerting
- Plan for graceful degradation scenarios

### Maintenance
- Regular dependency updates
- System validation checks
- Error log analysis
- Performance monitoring