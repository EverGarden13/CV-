# Scripts Directory

This directory contains utility scripts for the VisionMate-Lite project.

## Available Scripts

### Test Data Collection

#### download_test_images_simple.py ⭐ (Easiest)
Downloads ~45 sample images from COCO dataset (no API required).

```bash
python scripts/download_test_images_simple.py
```

Downloads:
- 15 person images
- 15 chair images  
- 15 car images

**Pros:** Simple, no setup required, fast  
**Cons:** Limited images, still need door/OCR/scene images

#### download_coco_test_data.py (Full COCO)
Downloads images using COCO API (more images, more control).

```bash
# First install pycocotools
pip install pycocotools

# Download annotations (one time, ~250MB)
python scripts/download_coco_test_data.py --download-annotations

# Then download images (default: 30 per class)
python scripts/download_coco_test_data.py

# Or specify number of images
python scripts/download_coco_test_data.py --images-per-class 50
```

**Pros:** More images, better variety  
**Cons:** Requires setup, larger download

### Evaluation and Testing

#### run_evaluation_example.py
Runs comprehensive evaluation of the system.

```bash
python scripts/run_evaluation_example.py
```

Measures:
- Detection latency and accuracy
- OCR processing time and accuracy
- System resource usage
- Overall performance metrics

**Note:** Requires test data in test_data/ folder

#### validate_system.py
Validates system installation and configuration.

```bash
python scripts/validate_system.py
```

Checks:
- Python dependencies
- Model files
- Camera access
- Tesseract installation
- TTS engine

### Report Generation

#### generate_report_figures.py
Generates figures and tables for the project report.

```bash
python scripts/generate_report_figures.py
```

Creates:
- 4 performance charts (PNG)
- 3 data tables (CSV + TXT)
- Saves to docs/report_figures/

## Quick Start Workflow

### 1. Download Test Data
```bash
# Easiest: Download sample images
python3 scripts/download_test_images_simple.py

# Or: Use full COCO downloader
python3 scripts/download_coco_test_data.py
```

### 2. Check Data Status
```bash
python3 test_data/collect_data.py
```

### 3. Validate System
```bash
python3 scripts/validate_system.py
```

### 4. Run Evaluation
```bash
python3 scripts/run_evaluation_example.py
```

### 5. Generate Report Figures
```bash
python3 scripts/generate_report_figures.py
```

## Notes

- All scripts should be run from the project root directory
- Test data is required for evaluation scripts
- See test_data/DATA_COLLECTION_GUIDE.md for data collection details
- See docs/HONEST_EVALUATION_GUIDE.md for evaluation guidance
