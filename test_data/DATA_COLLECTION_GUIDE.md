# Test Data Collection Guide

## Current Status
❌ **No test data currently exists** - The test_data folders are empty.

## What You Need

To properly evaluate the system and validate the report numbers, you need to collect real test images.

### Option 1: Collect Your Own Images (Recommended for Academic Honesty)

This is the best approach since the report says "I curated over 200 images specifically for this project."

#### What to Photograph:

**For Object Detection (120 images total):**
- **Person** (30 images): People at different distances, angles, lighting conditions
- **Chair** (30 images): Different types of chairs (office, dining, folding) in various settings
- **Car** (30 images): Cars from different angles, distances, in parking lots or streets
- **Door** (30 images): Different doors (wooden, glass, metal) open and closed

**For OCR Testing (60 images total):**
- **High-contrast printed text** (15 images): Books, printed signs, labels
- **Low-contrast text** (15 images): Faded signs, light text on light backgrounds
- **Screen displays** (15 images): Computer screens, phone displays, digital signs
- **Handwritten notes** (15 images): Various handwriting samples

**For Scene Classification (40 images total):**
- **Indoor scenes** (20 images): Office, kitchen, bedroom, living room
- **Outdoor scenes** (20 images): Street, park, parking lot, building exterior

#### How to Collect:
1. Use your phone or webcam
2. Take photos at 640×480 resolution or higher (will be resized)
3. Vary lighting conditions (bright, dim, natural, artificial)
4. Vary distances and angles
5. Ensure no identifiable personal information (faces, license plates)

#### Where to Save:
```
test_data/
├── detection/
│   ├── person/     (30 images)
│   ├── chair/      (30 images)
│   ├── car/        (30 images)
│   ├── door/       (30 images)
│   └── mixed/      (optional: multiple objects in one image)
├── ocr/
│   ├── signs/      (15 high-contrast)
│   ├── labels/     (15 low-contrast)
│   ├── screens/    (15 screen displays)
│   └── documents/  (15 handwritten)
└── scenes/
    ├── indoor/     (20 images)
    └── outdoor/    (20 images)
```

### Option 2: Download from Public Datasets

If you need data quickly, you can sample from public datasets:

#### COCO Dataset (for object detection)
- **Website:** https://cocodataset.org/
- **What to download:** COCO 2017 Val images (1GB)
- **Direct link:** http://images.cocodataset.org/#download
- **How to use:**
  1. Download val2017.zip
  2. Extract and filter for classes: person (0), chair (56), car (2)
  3. Manually select ~30 images per class
  4. Copy to appropriate test_data/detection/ folders

#### For OCR Testing
- **ICDAR Dataset:** https://rrc.cvc.uab.es/ (scene text)
- **Or just photograph:** Signs, labels, screens around you (easier and more realistic)

#### For Scene Classification
- **Places365:** http://places2.csail.mit.edu/download.html
- **Or just photograph:** Different rooms and outdoor locations

### Option 3: Use the Webcam Collection Script

I can create a script to help you collect data using your webcam:

```bash
python test_data/collect_data.py
```

This will let you:
- Capture images directly from webcam
- Organize them into correct folders
- Label them as you go

## After Collecting Data

Once you have real test data, you need to:

1. **Run actual evaluation:**
```bash
python scripts/run_evaluation_example.py
```

2. **Update report numbers** with real results in:
   - Section 6.1: Performance Metrics
   - Section 6.2: Detection Accuracy
   - Section 6.3: OCR Performance
   - Table 1, 2, 3

3. **Regenerate figures** with real data:
```bash
python scripts/generate_report_figures.py
```

## Realistic Expectations

When you run with real data, expect:

**Detection Accuracy:**
- Person: 70-85% precision, 65-80% recall (depends on lighting)
- Chair: 60-75% precision, 55-70% recall
- Car: 75-90% precision, 70-85% recall
- Door: 50-70% precision, 45-65% recall (hardest, not in COCO)

**OCR Accuracy:**
- High-contrast: 85-95% word accuracy
- Low-contrast: 60-80% word accuracy
- Screens: 75-90% word accuracy
- Handwritten: 30-50% word accuracy (Tesseract struggles here)

**Performance:**
- Detection latency: 350-500ms (depends on your CPU)
- OCR processing: 3-10s (depends on image complexity)

## Important Note

The current report numbers are **estimates** based on typical YOLOv8n and Tesseract performance. You should:

1. Collect real test data
2. Run actual evaluations
3. Update the report with real numbers
4. Be honest about actual performance

This is more academically honest and your assessors will appreciate real experimental results over theoretical estimates.

## Quick Start (Minimal Dataset)

If you're short on time, collect at least:
- 50 detection images (12-13 per class)
- 20 OCR images (5 per type)
- 20 scene images (10 indoor, 10 outdoor)

This gives you 90 images total - enough to get real performance numbers.

## Need Help?

Run the collection script:
```bash
python test_data/collect_data.py --help
```

Or just start photographing with your phone and organize the images into the folders above!
