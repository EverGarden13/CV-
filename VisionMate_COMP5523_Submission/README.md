# VisionMate-Lite

A lightweight assistive vision system for visually impaired users, designed as a solo-feasible project for COMP5523. The system provides real-time object detection alerts, on-demand OCR text reading, and optional scene labeling through audio feedback using a standard laptop webcam.

## Features

- **Real-time Object Detection**: Detects persons, chairs, cars, and doors with audio alerts
- **On-demand OCR**: Press spacebar to read text from the current camera view
- **Cross-platform Support**: Works on Windows and macOS with built-in TTS engines
- **Offline Operation**: All processing happens locally, no internet required
- **Privacy-focused**: No data transmission, optional local logging only

## System Requirements

- Python 3.8 or higher
- Webcam (built-in or USB)
- Microphone and speakers/headphones
- Windows 10+ or macOS 10.14+
- At least 4GB RAM recommended

## Installation

### 1. Clone and Setup Python Environment

```bash
git clone <repository-url>
cd visionmate-lite
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

Tesseract is required for text recognition functionality.

#### Windows Installation

**Option 1: Using Windows Installer (Recommended)**
1. Download the latest Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and follow the setup wizard
3. During installation, note the installation path (usually `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to your system PATH:
   - Open System Properties → Advanced → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to your PATH variable
5. Restart your command prompt/terminal

**Option 2: Using Package Manager**
```bash
# Using Chocolatey
choco install tesseract

# Using Scoop
scoop install tesseract
```

**Verify Installation:**
```bash
tesseract --version
```

#### macOS Installation

**Option 1: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract
brew install tesseract
```

**Option 2: Using MacPorts**
```bash
sudo port install tesseract
```

**Verify Installation:**
```bash
tesseract --version
```

### 3. Configure Environment Variables (Optional)

```bash
# Set custom test data path
export TEST_DATA_PATH="/path/to/your/test/data"

# Enable debug logging
export ENABLE_LOGGING="true"

# Enable frame saving for debugging (use with caution)
export ENABLE_FRAME_SAVING="false"
```

## Usage

### Basic Usage

```bash
python main.py
```

### Configuration

Edit `config.py` to customize:
- Detection confidence threshold
- Audio settings (speech rate, volume)
- Alert cooldown periods
- Camera settings

### Controls

- **Spacebar**: Trigger OCR text reading
- **Ctrl+C**: Exit application

## Project Structure

```
visionmate-lite/
├── src/                    # Source code modules
├── test_data/             # Test datasets
│   ├── detection/         # Object detection test images
│   └── ocr/              # OCR test images
├── tests/                 # Unit and integration tests
├── demos/                 # Demo scripts and examples
├── scripts/              # Utility and validation scripts
├── docs/                 # Documentation and reports
├── evaluation/           # Performance evaluation scripts
├── models/              # Model files (auto-downloaded)
├── config.py           # Configuration settings
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Troubleshooting

### Common Issues

**Camera not detected:**
- Ensure no other applications are using the webcam
- Try changing `CAMERA_INDEX` in `config.py` (try 0, 1, 2)
- Check camera permissions in system settings

**Tesseract not found:**
- Verify Tesseract is installed: `tesseract --version`
- On Windows, ensure Tesseract is in your PATH
- Try setting explicit path in code if needed

**Audio not working:**
- Check system audio settings and volume
- Ensure speakers/headphones are connected
- On macOS, grant microphone permissions if prompted

**Poor OCR accuracy:**
- Ensure good lighting conditions
- Hold text steady and at appropriate distance
- Try with high-contrast text (black text on white background)

### Performance Optimization

- Close unnecessary applications to free up CPU
- Reduce `CONFIDENCE_THRESHOLD` if too many false positives
- Increase `FRAME_SKIP` value if detection is too slow
- Lower camera resolution in `config.py` if needed

## Development

### Running Tests

```bash
# Performance evaluation
python -m evaluation.simple_evaluator

# Manual testing scenarios
python main.py --test-mode
```

### Adding Test Data

1. Place detection test images in `test_data/detection/`
2. Place OCR test images in `test_data/ocr/`
3. Follow naming convention: `category_condition_number.jpg`

## Privacy and Ethics

- All processing happens locally on your device
- No data is transmitted over the network
- Frame logging is disabled by default
- When enabled, logs are stored locally and can be deleted anytime
- Follow ethical guidelines when collecting test data

## License

This project is developed for educational purposes as part of COMP5523 coursework.

## Quick Navigation

- 📚 **[Documentation](docs/)** - All project reports, guides, and technical docs
- 🎮 **[Demos](demos/)** - Interactive demonstrations and examples  
- 🧪 **[Tests](tests/)** - Test suite and validation scripts
- 🔧 **[Scripts](scripts/)** - Utility and evaluation scripts
- 💻 **[Source Code](src/)** - Core application modules
- 📊 **[Test Data](test_data/)** - Sample images for testing
- 📈 **[Evaluation](evaluation/)** - Performance evaluation tools

## Support

For issues related to:
- **Installation**: Check the troubleshooting section above
- **Performance**: Adjust settings in `config.py`
- **Tesseract**: Refer to official Tesseract documentation
- **Course project**: Contact course instructors

## Acknowledgments

- YOLOv8 by Ultralytics for object detection
- Tesseract OCR by Google for text recognition
- OpenCV for computer vision utilities
- pyttsx3 for cross-platform text-to-speech