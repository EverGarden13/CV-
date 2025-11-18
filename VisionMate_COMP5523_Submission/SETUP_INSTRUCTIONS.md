# VisionMate-Lite Setup Instructions for Graders

## Quick Start (5 Minutes)

This guide will help you set up and run VisionMate-Lite for evaluation.

---

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11, macOS Monterey/Ventura, or Linux
- **Hardware**: 
  - Webcam (built-in or USB)
  - Speakers or headphones
  - Minimum 4GB RAM
  - Dual-core CPU or better
- **Internet**: Required for initial setup only (model downloads)

---

## Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
# or
python3 --version
```

Should show Python 3.8 or higher.

### Step 2: Install Dependencies

**Option A: Automatic Installation (Recommended)**

```bash
pip install -r requirements.txt
```

**Option B: Manual Installation**

```bash
pip install ultralytics opencv-python pytesseract pyttsx3 easyocr torch torchvision pillow numpy
```

### Step 3: Install Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default path: `C:\Program Files\Tesseract-OCR`)
3. Add to PATH or the system will auto-detect

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 4: Verify Installation

Run the validation script:

```bash
python scripts/validate_system.py
```

This will check:
- ✓ Python version
- ✓ All dependencies installed
- ✓ Tesseract OCR available
- ✓ Camera access
- ✓ TTS engine working

---

## Running the Application

### Basic Usage

```bash
python main.py
```

### Controls

- **Spacebar**: Trigger OCR text reading
- **Ctrl+C** or **Q**: Exit application

### What to Expect

1. **Startup**: System initializes (15-20 seconds)
   - Loads YOLOv8n model (auto-downloads on first run)
   - Initializes camera
   - Sets up audio system

2. **Object Detection**: Runs continuously
   - Announces detected objects: "Person ahead", "Chair detected", etc.
   - 5-second cooldown prevents repetitive alerts

3. **OCR**: Press spacebar to read text
   - System says "Processing text..."
   - Reads detected text aloud
   - Provides feedback if no text found

---

## Testing the System

### Quick Demo (2 Minutes)

1. **Test Object Detection**:
   - Run `python main.py`
   - Move in front of camera
   - Should hear "Person ahead"

2. **Test OCR**:
   - Hold printed text to camera
   - Press spacebar
   - Should hear text read aloud

3. **Test Multiple Objects**:
   - Place chair in view
   - Should hear "Chair detected"

### Run Evaluation Scripts

```bash
# Run simple evaluation
python scripts/simple_evaluation.py

# Run OCR evaluation
python scripts/evaluate_ocr.py

# Generate report figures
python scripts/generate_report_figures.py
```

---

## Troubleshooting

### Camera Not Found

**Problem**: "Camera not accessible" error

**Solutions**:
1. Check camera permissions in system settings
2. Close other applications using camera (Zoom, Skype, etc.)
3. Try different camera index in `config.py`:
   ```python
   CAMERA_INDEX = 1  # Try 0, 1, or 2
   ```

### Tesseract Not Found

**Problem**: "Tesseract not installed" error

**Windows Solution**:
```python
# Edit config.py, add:
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**macOS/Linux Solution**:
```bash
which tesseract  # Find path
# Add to config.py if needed
```

### TTS Not Working

**Problem**: No audio output

**Solutions**:
1. Check system volume
2. Verify speakers/headphones connected
3. Test TTS separately:
   ```python
   python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
   ```

### Model Download Issues

**Problem**: YOLOv8n model not downloading

**Solution**:
```bash
# Manual download
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Slow Performance

**Problem**: Detection latency > 1 second

**Solutions**:
1. Close other applications
2. Reduce frame processing in `config.py`:
   ```python
   FRAME_SKIP = 5  # Process every 5th frame instead of 3rd
   ```

---

## File Structure

```
VisionMate-Lite/
├── main.py                 # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── SETUP_INSTRUCTIONS.md  # This file
├── src/                   # Source code modules
│   ├── camera.py          # Camera interface
│   ├── detection.py       # Object detection
│   ├── ocr.py            # OCR processing
│   ├── audio.py          # Audio feedback
│   └── ...
├── scripts/               # Utility scripts
│   ├── validate_system.py # System validation
│   ├── simple_evaluation.py # Performance evaluation
│   └── ...
├── docs/                  # Documentation
│   ├── COMP5523_Project_Report_REFINED.md
│   ├── VisionMate-Lite Project Presentation.pdf
│   └── ...
├── evaluation/            # Evaluation results
│   └── evaluation_results.json
└── models/               # Model files (auto-downloaded)
    └── yolov8n.pt
```

---

## Expected Performance

- **Detection Latency**: ~428ms average
- **OCR Processing**: 5-8 seconds
- **System Startup**: 15-20 seconds
- **Memory Usage**: 500-800MB
- **Detection Accuracy**: 82% precision, 75% recall
- **OCR Success Rate**: 44% on standard dataset

---

## Demonstration Features

### 1. Real-time Object Detection
- Detects person, chair, car, door
- Proximity alerts for close objects
- 5-second cooldown mechanism

### 2. OCR Text Reading
- Press spacebar to capture and read text
- Preprocessing for better accuracy
- Audio feedback for results

### 3. Audio Feedback
- Clear, concise announcements
- Non-overlapping speech
- Platform-specific TTS

### 4. Error Recovery
- Automatic camera reconnection
- Graceful degradation
- Clear error messages

### 5. Cross-Platform
- Works on Windows, macOS, Linux
- Automatic platform detection
- Consistent behavior

---

## Evaluation Data

### Object Detection
- **Dataset**: 45 images from COCO (15 per class)
- **Classes**: Person, Chair, Car
- **Results**: See `evaluation/evaluation_results.json`

### OCR
- **Dataset**: 100 images from standard OCR dataset
- **Results**: See `evaluation/ocr_evaluation_results.json`

### Figures and Tables
- **Location**: `docs/report_figures/`
- **Generated by**: `scripts/generate_report_figures.py`

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review `README.md` for detailed documentation
3. Check `docs/USAGE_GUIDE.md` for usage examples
4. Review project report in `docs/` folder

---

## Grading Notes

**What to Evaluate:**
1. ✓ System runs without errors
2. ✓ Object detection works in real-time
3. ✓ OCR reads text when triggered
4. ✓ Audio feedback is clear
5. ✓ Performance meets targets
6. ✓ Error handling works
7. ✓ Cross-platform compatibility

**Evaluation Scripts:**
- `scripts/simple_evaluation.py` - Performance metrics
- `scripts/evaluate_ocr.py` - OCR evaluation
- `scripts/generate_report_figures.py` - Generate visualizations

**Documentation:**
- Project Report: `docs/COMP5523_Project_Report_REFINED.md`
- Presentation: `docs/VisionMate-Lite Project Presentation.pdf`
- Evaluation Results: `evaluation/evaluation_results.json`

---

## Quick Validation Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tesseract OCR installed
- [ ] Camera accessible
- [ ] Validation script passes (`python scripts/validate_system.py`)
- [ ] Main application runs (`python main.py`)
- [ ] Object detection announces objects
- [ ] OCR reads text (spacebar)
- [ ] Audio feedback works
- [ ] System exits cleanly (Ctrl+C)

---

**Estimated Setup Time**: 5-10 minutes
**Estimated Testing Time**: 5 minutes
**Total Time**: 15 minutes maximum

Thank you for evaluating VisionMate-Lite!
