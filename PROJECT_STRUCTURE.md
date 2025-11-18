# VisionMate-Lite Project Structure

## Directory Organization

```
VisionMate-Lite/
├── src/                          # Source code
│   ├── camera/                   # Camera interface
│   ├── detection/                # Object detection
│   ├── ocr/                      # OCR processing
│   ├── scene/                    # Scene classification
│   ├── audio/                    # Audio feedback
│   └── utils/                    # Utilities
│
├── models/                       # Model files
│   └── yolov8n.pt               # YOLOv8 nano model
│
├── evaluation/                   # Evaluation results
│   ├── evaluation_results.json   # Main evaluation metrics
│   ├── ocr_evaluation_results.json  # OCR evaluation details
│   ├── evaluation.py             # Evaluation script
│   └── README.md                 # Evaluation documentation
│
├── scripts/                      # Utility scripts
│   ├── download_coco_test_data.py      # Download COCO test images
│   ├── download_ocr_dataset.py         # Download OCR dataset
│   ├── evaluate_ocr.py                 # Run OCR evaluation
│   ├── generate_report_figures.py      # Generate report figures
│   ├── simple_evaluation.py            # Run simple evaluation
│   └── validate_system.py              # System validation
│
├── test_data/                    # Test datasets
│   ├── detection/                # Object detection test images
│   │   ├── person/              # Person images (15)
│   │   ├── chair/               # Chair images (15)
│   │   └── car/                 # Car images (15)
│   └── ocr/                     # OCR test images (100)
│
├── docs/                         # Documentation
│   ├── COMP5523_Project_Report_REFINED.md  # Final project report
│   ├── VERIFICATION_COMPLETE.md            # Verification status
│   ├── USAGE_GUIDE.md                      # Usage instructions
│   ├── VisionMate_Project_Concept.md       # Project concept
│   └── report_figures/                     # Report figures and tables
│       ├── figure1_performance_comparison.png
│       ├── figure2_detection_accuracy.png
│       ├── figure3_ocr_performance.png
│       ├── figure4_latency_distribution.png
│       ├── table1_performance_summary.csv
│       ├── table2_detection_accuracy.csv
│       ├── table3_testing_scenarios.csv
│       └── table4_ocr_performance.csv
│
├── tests/                        # Unit tests
│   └── test_*.py                # Test files
│
├── demos/                        # Demo scripts
│
├── config.py                     # Configuration
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # Project README
```

## Key Files

### Source Code
- `main.py` - Main application entry point
- `config.py` - Configuration settings
- `src/` - All source code modules

### Evaluation
- `evaluation/evaluation_results.json` - Main evaluation metrics (145 images)
- `evaluation/ocr_evaluation_results.json` - Detailed OCR results (100 images)

### Documentation
- `docs/COMP5523_Project_Report_REFINED.md` - Final project report
- `docs/VERIFICATION_COMPLETE.md` - Verification status
- `docs/USAGE_GUIDE.md` - How to use the system

### Scripts
- `scripts/evaluate_ocr.py` - Run OCR evaluation
- `scripts/generate_report_figures.py` - Generate report figures
- `scripts/simple_evaluation.py` - Run object detection evaluation

## Running the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Main Application
```bash
python main.py
```

### 3. Run Evaluations
```bash
# Object detection evaluation
python scripts/simple_evaluation.py

# OCR evaluation
python scripts/evaluate_ocr.py

# Generate report figures
python scripts/generate_report_figures.py
```

## Evaluation Results

### Object Detection (45 images)
- Person: 85% precision, 78% recall
- Chair: 72% precision, 65% recall
- Car: 88% precision, 82% recall
- Overall: 82% precision, 75% recall

### OCR (100 images)
- Total images: 100
- Text detected: 44 images
- Success rate: 44%
- Processing success: 100%

## File Locations

All evaluation results are stored in `evaluation/`:
- Main metrics: `evaluation/evaluation_results.json`
- OCR details: `evaluation/ocr_evaluation_results.json`

All report figures are in `docs/report_figures/`:
- Figures: PNG format
- Tables: CSV and TXT formats

## Notes

- Model file (`yolov8n.pt`) is in `models/` directory
- Test data is organized by type in `test_data/`
- All scripts reference the correct paths in `evaluation/`
