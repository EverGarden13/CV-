# Quick Guide: Get Test Data Using COCO API

## TL;DR - Fastest Way

```bash
# Download ALL test images (no setup required!)
python3 scripts/download_test_images_simple.py
```

This downloads ~120 images in 5-10 minutes. Everything you need! ✅

## Option 1: Complete Download (Recommended) ⭐

**What it does:** Downloads ~120 images from COCO + Unsplash  
**Time:** 5-10 minutes  
**Setup:** None required

```bash
python3 scripts/download_test_images_simple.py
```

Downloads EVERYTHING:
- ✅ 15 person images (COCO)
- ✅ 15 chair images (COCO)
- ✅ 15 car images (COCO)
- ✅ 15 door images (Unsplash)
- ✅ 30 OCR images (Unsplash - signs, labels, screens, documents)
- ✅ 20 scene images (Unsplash - indoor/outdoor)

**Total: ~120 images - Complete dataset ready for evaluation!**

## Option 2: Full COCO Download

**What it does:** Downloads any number of images using COCO API  
**Time:** 10-15 minutes (first time setup)  
**Setup:** Requires COCO annotations

### Step 1: Install COCO API
```bash
pip install pycocotools
```

### Step 2: Download Annotations (one time, ~250MB)
```bash
python3 scripts/download_coco_test_data.py --download-annotations
```

Or manually:
```bash
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip annotations_trainval2017.zip
mv annotations/instances_val2017.json coco_annotations/
```

### Step 3: Download Images
```bash
# Default: 30 images per class
python3 scripts/download_coco_test_data.py

# Or specify number
python3 scripts/download_coco_test_data.py --images-per-class 50
```

Downloads:
- ✅ 30-50 person images
- ✅ 30-50 chair images
- ✅ 30-50 car images

## What's Included

The simple download script gets you EVERYTHING:

### Detection Images (60 total)
- ✅ **Person** (15): Various poses, distances, lighting
- ✅ **Chair** (15): Different types and settings
- ✅ **Car** (15): Various angles and distances
- ✅ **Door** (15): Wooden, glass, metal doors

### OCR Images (30 total)
- ✅ **Signs** (10): Street signs, store signs, warning signs
- ✅ **Labels** (10): Product labels, text on objects
- ✅ **Screens** (10): Computer screens, displays
- ✅ **Documents** (10): Handwritten notes, forms

### Scene Images (20 total)
- ✅ **Indoor** (10): Office, kitchen, bedroom, living room
- ✅ **Outdoor** (10): Street, park, outdoor locations

**No manual collection needed!** Everything downloads automatically.

## After Downloading

### Check what you have:
```bash
python3 test_data/collect_data.py
```

### Run evaluation:
```bash
python3 scripts/run_evaluation_example.py
```

### Generate report figures:
```bash
python3 scripts/generate_report_figures.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'pycocotools'"
```bash
pip install pycocotools
```

### "COCO annotations not found"
Run:
```bash
python3 scripts/download_coco_test_data.py --download-annotations
```

### "Failed to download image"
- Check internet connection
- Some COCO images may be unavailable
- Script will skip failed downloads and continue

### "No test data found"
Make sure you're running from project root:
```bash
cd /path/to/visionmate-lite
python3 scripts/download_test_images_simple.py
```

## Time Estimates

| Method | Setup Time | Download Time | Total Images |
|--------|------------|---------------|--------------|
| Simple download | 0 min | 2-3 min | 45 |
| Full COCO (first time) | 10 min | 5-10 min | 90-150 |
| Full COCO (after setup) | 0 min | 5-10 min | 90-150 |
| Manual collection | 0 min | 60-120 min | 90-200 |

## Recommendation

1. **Download complete dataset** (5-10 min)
   ```bash
   python3 scripts/download_test_images_simple.py
   ```

2. **Check what you have** (1 min)
   ```bash
   python3 test_data/collect_data.py
   ```

3. **Run evaluation** (5-10 min)
   ```bash
   python3 scripts/run_evaluation_example.py
   ```

4. **Update report with real results** (30 min)
   - Edit `docs/COMP5523_Project_Report_REFINED.md`
   - Update performance numbers in Section 6

5. **Regenerate figures** (2 min)
   ```bash
   python3 scripts/generate_report_figures.py
   ```

**Total time: ~45-60 minutes for complete, honest evaluation!**

## Need More Help?

- **Data collection guide:** `test_data/DATA_COLLECTION_GUIDE.md`
- **Evaluation guide:** `docs/HONEST_EVALUATION_GUIDE.md`
- **Scripts README:** `scripts/README.md`
