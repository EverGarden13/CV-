# VisionMate-Lite Usage Guide

## Overview

VisionMate-Lite is an assistive vision system designed to help visually impaired users navigate their environment using a standard laptop webcam. The system provides real-time object detection alerts and on-demand OCR text reading through audio feedback.

## System Requirements

### Hardware Requirements
- **Camera**: Standard USB webcam or built-in laptop camera
- **Audio**: Built-in speakers or headphones for audio feedback
- **Processing**: Modern laptop with CPU (GPU acceleration not required)
- **Memory**: Minimum 4GB RAM, 8GB recommended

### Software Requirements
- **Operating System**: Windows 10/11 or macOS 10.14+
- **Python**: Python 3.8 or higher
- **Dependencies**: See `requirements.txt`

### Additional Software
- **Tesseract OCR**: Required for text reading functionality
  - **Windows**: Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: Install via Homebrew: `brew install tesseract`

## Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd visionmate-lite
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR
Follow the platform-specific instructions above for Tesseract installation.

### 4. Verify Installation
```bash
python validate_system.py
```

This will check all dependencies and system requirements.

## Getting Started

### 1. Basic System Check
Before first use, run the system validation:
```bash
python validate_system.py
```

### 2. Start VisionMate-Lite
```bash
python main.py
```

### 3. Using the System
- **Object Detection**: Automatic - the system continuously monitors for objects
- **Text Reading**: Press **SPACEBAR** to capture and read text from the current view
- **Exit**: Press **ESC** or **Q** to quit the application

## Features and Usage

### Object Detection
The system automatically detects and announces:
- **Person**: "Person ahead" when someone is nearby
- **Chair**: "Chair detected" for navigation obstacles
- **Car**: "Car nearby" for vehicle awareness
- **Door**: "Door detected" for navigation landmarks

**How it works:**
- Continuous monitoring through webcam
- Audio alerts when objects are in close proximity (>15% of camera view)
- 5-second cooldown prevents repetitive alerts
- Processes every 3rd frame for optimal performance

### Text Reading (OCR)
On-demand text reading for signs, documents, and labels:

**How to use:**
1. Point camera at text you want to read
2. Press **SPACEBAR** to trigger OCR
3. Wait for "Processing text" notification
4. Listen to the extracted text being read aloud

**Tips for better OCR:**
- Ensure good lighting
- Hold camera steady
- Position text clearly in view
- Avoid glare and shadows

### Audio Feedback
- **Object Alerts**: Short, clear announcements (e.g., "Person ahead")
- **Text Reading**: Full text content read at adjustable speed
- **System Status**: Notifications for processing states and errors

## Configuration

### Basic Configuration
Edit `config.py` to customize:

```python
# Detection sensitivity
CONFIDENCE_THRESHOLD = 0.5  # Lower = more sensitive
PROXIMITY_THRESHOLD = 0.15  # Proximity detection sensitivity

# Audio settings
SPEECH_RATE = 200  # Words per minute

# Performance settings
FRAME_SKIP = 3  # Process every Nth frame (higher = better performance)
```

### Environment Variables
Set these for advanced configuration:

```bash
# Test data location
export TEST_DATA_PATH="path/to/test/data"

# Enable debug logging
export ENABLE_LOGGING="true"

# Enable frame saving for debugging
export ENABLE_FRAME_SAVING="true"
```

## Performance Optimization

### For Better Detection Performance
- **Lighting**: Ensure adequate lighting for camera
- **Camera Position**: Position camera at eye level when possible
- **Background**: Avoid cluttered backgrounds when possible

### For Better OCR Performance
- **Text Quality**: Use high-contrast text (black on white)
- **Distance**: Position text 1-3 feet from camera
- **Stability**: Hold camera steady during OCR processing
- **Lighting**: Avoid glare and ensure even lighting

### System Performance
- **CPU Usage**: System uses ~20-30% CPU during normal operation
- **Memory Usage**: Typically uses 500MB-1GB RAM
- **Battery**: Continuous camera use will drain laptop battery faster

## Troubleshooting

### Common Issues

#### "Camera not found" Error
**Cause**: Camera not connected or in use by another application
**Solution**: 
- Check camera connection
- Close other applications using the camera
- Try different camera index in config.py

#### "Tesseract not found" Error
**Cause**: Tesseract OCR not installed or not in system PATH
**Solution**:
- Install Tesseract following platform instructions
- Verify installation: `tesseract --version`
- Add Tesseract to system PATH if needed

#### Poor OCR Accuracy
**Cause**: Poor image quality, lighting, or text clarity
**Solution**:
- Improve lighting conditions
- Move closer to text
- Ensure text is clearly visible and in focus
- Try different angles

#### Slow Performance
**Cause**: System resources or hardware limitations
**Solution**:
- Close other applications
- Increase FRAME_SKIP value in config.py
- Ensure adequate system memory
- Check CPU usage

#### No Audio Output
**Cause**: Audio system issues or TTS engine problems
**Solution**:
- Check system audio settings
- Verify speakers/headphones are working
- Restart the application
- Check platform-specific TTS settings

### Getting Help

1. **Check Logs**: Enable logging with `ENABLE_LOGGING=true`
2. **Run Validation**: Use `python validate_system.py`
3. **Check Configuration**: Verify config.py settings
4. **Test Components**: Run individual component tests

## System Limitations

### Detection Limitations
- **Object Classes**: Limited to 4 object types (person, chair, car, door)
- **Proximity**: Uses simple bounding box size, not actual distance
- **Accuracy**: ~70-85% detection accuracy depending on conditions
- **Lighting**: Performance degrades in poor lighting
- **Angle**: Works best with objects facing the camera

### OCR Limitations
- **Languages**: English text only
- **Fonts**: Works best with standard fonts
- **Handwriting**: Cannot read handwritten text
- **Image Quality**: Requires clear, high-contrast text
- **Processing Time**: 3-10 seconds per OCR request

### Technical Limitations
- **CPU Only**: No GPU acceleration (by design for compatibility)
- **Single Camera**: Uses one camera input only
- **Offline Only**: No internet connectivity required or used
- **Platform**: Optimized for Windows and macOS

### Privacy and Security
- **Local Processing**: All processing happens on-device
- **No Data Transmission**: No data sent to external servers
- **Frame Storage**: Frames not saved by default (configurable)
- **Audio Recording**: System does not record audio

## Performance Targets

The system is designed to meet these performance targets:

- **Detection Latency**: <500ms average
- **OCR Processing**: <10 seconds end-to-end
- **Startup Time**: <30 seconds
- **Memory Usage**: <1GB RAM
- **CPU Usage**: <50% on modern laptops

## Demonstration Mode

For demonstrations or testing:

1. **Prepare Environment**: Ensure good lighting and clear camera view
2. **Test Objects**: Have test objects ready (person, chair, etc.)
3. **Test Text**: Prepare printed text samples for OCR testing
4. **Audio Check**: Verify audio output is working
5. **Run Integration Test**: Use `python test_system_integration.py`

## Evaluation and Metrics

### Running Evaluation
```bash
python run_evaluation_example.py
```

This generates:
- Performance metrics (latency, accuracy)
- Manual testing scenarios
- Evaluation reports for project documentation

### Manual Testing Scenarios
The system includes 5 predefined testing scenarios:
1. Person detection and proximity alerts
2. Object detection for navigation obstacles
3. OCR text reading functionality
4. Error handling and system reliability
5. Performance target validation

## Support and Maintenance

### Regular Maintenance
- **Update Dependencies**: Periodically update Python packages
- **Clean Test Data**: Remove old test data and logs
- **Check Performance**: Monitor system performance over time

### Backup and Recovery
- **Configuration**: Backup custom config.py settings
- **Test Data**: Backup any custom test datasets
- **Logs**: Archive important log files

## Future Enhancements

Potential improvements for future versions:
- Additional object classes
- Multi-language OCR support
- Scene classification
- Distance estimation
- Mobile platform support
- Voice commands

---

**Note**: This system is designed as a proof-of-concept for the COMP5523 course project. For production use, additional testing, optimization, and safety considerations would be required.