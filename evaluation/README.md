# VisionMate-Lite Evaluation Module

This module provides comprehensive evaluation and metrics collection for the VisionMate-Lite assistive vision system, designed for the COMP5523 course project.

## Overview

The evaluation module implements the `SimpleEvaluator` class which provides:

- **Performance Metrics**: Latency measurement for object detection and OCR operations
- **Accuracy Assessment**: Precision/recall calculation for object detection classes
- **Manual Testing Scenarios**: 5 comprehensive testing scenarios for system validation
- **Metrics Logging**: JSON and Markdown report generation for project documentation

## Usage

### Basic Usage

```python
from evaluation import SimpleEvaluator

# Initialize evaluator
evaluator = SimpleEvaluator()

# Run complete evaluation suite
results = evaluator.run_complete_evaluation()
```

### Individual Metrics

```python
# Measure detection latency
detection_results = evaluator.measure_detection_latency(num_frames=100)
print(f"Average detection latency: {detection_results['average_ms']}ms")

# Measure OCR latency
ocr_results = evaluator.measure_ocr_latency(num_samples=20)
print(f"Average OCR latency: {ocr_results['average_s']}s")

# Calculate precision/recall
accuracy_results = evaluator.calculate_precision_recall()
for class_name, metrics in accuracy_results.items():
    print(f"{class_name}: P={metrics['precision']:.3f}, R={metrics['recall']:.3f}")
```

### Manual Testing Scenarios

```python
# Generate manual testing documentation
scenarios = evaluator.run_manual_testing_scenarios()
# Creates: evaluation_results/manual_testing_scenarios.md
```

## Performance Targets

The evaluation module validates against these performance targets:

- **Detection Latency**: < 500ms average (CPU-only operation)
- **OCR Processing**: < 10 seconds end-to-end
- **Memory Usage**: < 1GB RAM during operation
- **Startup Time**: < 30 seconds to initialize

## Manual Testing Scenarios

The module documents 5 comprehensive testing scenarios:

1. **Person Approaching Warning**: Tests proximity detection and audio alerts
2. **Navigation Obstacle Detection**: Tests object detection for chairs, doors, cars
3. **Text Reading on Demand**: Tests OCR functionality and text-to-speech
4. **System Reliability**: Tests error handling and graceful degradation
5. **Performance Validation**: Tests system performance against targets

## Output Files

The evaluator creates the following files in `evaluation_results/`:

- `complete_evaluation_results.json`: Complete metrics in JSON format
- `evaluation_summary.md`: Human-readable summary report
- `manual_testing_scenarios.json`: Structured scenario data
- `manual_testing_scenarios.md`: Readable testing procedures
- `performance_metrics_[timestamp].json`: Timestamped metrics logs

## Requirements Coverage

This module addresses the following project requirements:

- **7.1**: Performance metrics logging (latency, detection counts)
- **7.2**: Accuracy evaluation on curated test dataset
- **7.4**: Task-based evaluation scenarios
- **7.5**: Metrics export for project report inclusion

## Test Data Structure

Expected test data directory structure:

```
test_data/
├── detection/
│   ├── person/
│   ├── chair/
│   ├── car/
│   ├── door/
│   └── mixed/
└── ocr/
    ├── documents/
    ├── signs/
    ├── labels/
    └── screens/
```

## Environment Variables

- `TEST_DATA_PATH`: Path to test data directory (default: 'test_data/')
- `ENABLE_LOGGING`: Enable detailed logging ('true'/'false')

## Dependencies

The evaluation module requires the same dependencies as the main VisionMate-Lite system:

- OpenCV (cv2)
- NumPy
- Ultralytics (YOLO)
- pytesseract
- pyttsx3

## Integration with Main System

The evaluation module is designed to work with the existing VisionMate-Lite components:

- `src.detection.ObjectDetector`: For detection latency measurement
- `src.ocr.OCREngine`: For OCR latency measurement
- `src.audio.AudioManager`: For TTS timing estimation
- `src.camera.CameraInterface`: For frame capture testing

## Project Report Integration

The generated reports are designed for direct inclusion in the 8-page COMP5523 project report:

- Performance metrics tables
- Accuracy assessment results
- Manual testing scenario documentation
- System limitation analysis
- Optimization recommendations