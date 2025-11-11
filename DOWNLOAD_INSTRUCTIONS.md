# Quick Download Instructions

## Install tqdm (Optional but Recommended)

For nice progress bars:
```bash
pip install tqdm
```

## Download Test Data

```bash
python3 scripts/download_test_images_simple.py
```

## What It Does

Downloads ~120 images automatically:
- ✅ 60 detection images (person, chair, car, door)
- ✅ 30 OCR images (signs, labels, screens, documents)
- ✅ 20 scene images (indoor, outdoor)

## Features

- ✅ Progress bars (with tqdm)
- ✅ Retry logic (3 attempts per image)
- ✅ Skip existing files
- ✅ Detailed logging
- ✅ Error handling
- ✅ Summary statistics

## Time Estimate

- With good internet: 5-10 minutes
- With slow internet: 10-15 minutes

## After Download

1. Check data status:
   ```bash
   python3 test_data/collect_data.py
   ```

2. Run evaluation:
   ```bash
   python3 scripts/run_evaluation_example.py
   ```

3. Update report with real results

4. Regenerate figures:
   ```bash
   python3 scripts/generate_report_figures.py
   ```

## Troubleshooting

### "ModuleNotFoundError: No module named 'tqdm'"
```bash
pip install tqdm
```
Or just run without it - script works fine without tqdm, just no progress bars.

### Some downloads fail
- Normal! Some Unsplash URLs may be unavailable
- Script retries 3 times automatically
- As long as you get 80+ images, you're good

### Slow downloads
- Unsplash images are larger than COCO
- Script waits 0.8s between downloads to be nice to servers
- Be patient!

### Want to re-download
Delete the test_data folders and run again:
```bash
rm -rf test_data/detection/* test_data/ocr/* test_data/scenes/*
python3 scripts/download_test_images_simple.py
```

## What You'll See

With tqdm:
```
🚀 VisionMate-Lite Test Data Downloader
...
📁 Category: person (15 images)
  person: 100%|████████████| 15/15 [00:25<00:00]
  ✓ person: 15/15 images
...
```

Without tqdm:
```
📁 Category: person (15 images)
  ↓ 01/15: 000000000139.jpg... ✓
  ↓ 02/15: 000000000285.jpg... ✓
  ...
```

## Summary Output

```
📊 Download Summary
✓ New downloads:      95 images
○ Already existed:    25 images
✗ Failed downloads:    0 images

📁 Dataset Overview
  person      :  15 images
  chair       :  15 images
  car         :  15 images
  door        :  15 images
  signs       :  10 images
  labels      :  10 images
  screens     :  10 images
  documents   :  10 images
  indoor      :  10 images
  outdoor     :  10 images

📈 Category Totals
  Detection   :  60 images
  Ocr         :  40 images
  Scenes      :  20 images

  TOTAL       : 120 images
  TARGET      : ~120 images

✓✓ Excellent! You have enough data for comprehensive evaluation
```

Ready to start? Run:
```bash
python3 scripts/download_test_images_simple.py
```
