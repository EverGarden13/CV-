"""
Download test images from COCO dataset using COCO API
This will download images for person, chair, and car classes
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
from collections import defaultdict

try:
    from pycocotools.coco import COCO
except ImportError:
    print("Installing pycocotools...")
    os.system("pip install pycocotools")
    from pycocotools.coco import COCO

# COCO class IDs for our target objects
COCO_CLASSES = {
    'person': 1,
    'chair': 62,
    'car': 3
}

def download_image(img_url, save_path):
    """Download image from URL"""
    try:
        urllib.request.urlretrieve(img_url, save_path)
        return True
    except Exception as e:
        print(f"  ✗ Failed to download: {e}")
        return False

def download_coco_images(data_dir='test_data', images_per_class=30, use_val=True):
    """
    Download images from COCO dataset
    
    Args:
        data_dir: Base directory for test data
        images_per_class: Number of images to download per class
        use_val: Use validation set (smaller, faster) vs train set
    """
    
    # Setup paths
    base_path = Path(data_dir)
    
    # COCO annotation URLs
    if use_val:
        ann_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
        ann_file = 'instances_val2017.json'
        img_url_template = 'http://images.cocodataset.org/val2017/{}'
        print("Using COCO 2017 Validation set (smaller, faster)")
    else:
        ann_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
        ann_file = 'instances_train2017.json'
        img_url_template = 'http://images.cocodataset.org/train2017/{}'
        print("Using COCO 2017 Training set (larger)")
    
    print(f"\n{'='*60}")
    print("COCO Test Data Downloader")
    print(f"{'='*60}\n")
    
    # Check if we need to download annotations
    ann_path = Path('coco_annotations')
    ann_path.mkdir(exist_ok=True)
    
    ann_file_path = ann_path / ann_file
    
    if not ann_file_path.exists():
        print("⚠️  COCO annotations not found.")
        print("\nYou need to download COCO annotations first:")
        print(f"1. Download: {ann_url}")
        print(f"2. Extract {ann_file} to: {ann_path}/")
        print("\nOr run:")
        print(f"  wget {ann_url}")
        print(f"  unzip annotations_trainval2017.zip")
        print(f"  mv annotations/{ann_file} {ann_path}/")
        return
    
    print(f"✓ Found annotations: {ann_file_path}\n")
    
    # Initialize COCO API
    print("Loading COCO annotations...")
    coco = COCO(str(ann_file_path))
    print("✓ Annotations loaded\n")
    
    # Download images for each class
    total_downloaded = 0
    
    for class_name, class_id in COCO_CLASSES.items():
        print(f"\n{'─'*60}")
        print(f"Downloading {class_name} images (class_id={class_id})")
        print(f"{'─'*60}")
        
        # Get category info
        cat_ids = coco.getCatIds(catNms=[class_name])
        if not cat_ids:
            print(f"  ✗ Category '{class_name}' not found in COCO")
            continue
        
        # Get image IDs containing this category
        img_ids = coco.getImgIds(catIds=cat_ids)
        print(f"  Found {len(img_ids)} images with {class_name}")
        
        # Create save directory
        save_dir = base_path / 'detection' / class_name
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Download images
        downloaded = 0
        attempted = 0
        
        for img_id in img_ids[:images_per_class * 2]:  # Try 2x in case some fail
            if downloaded >= images_per_class:
                break
            
            attempted += 1
            
            # Get image info
            img_info = coco.loadImgs(img_id)[0]
            img_url = img_url_template.format(img_info['file_name'])
            
            # Save path
            save_path = save_dir / img_info['file_name']
            
            # Skip if already exists
            if save_path.exists():
                print(f"  ○ {downloaded+1}/{images_per_class}: {img_info['file_name']} (already exists)")
                downloaded += 1
                continue
            
            # Download
            print(f"  ↓ {downloaded+1}/{images_per_class}: {img_info['file_name']}...", end='')
            if download_image(img_url, save_path):
                print(" ✓")
                downloaded += 1
                total_downloaded += 1
            else:
                print(" ✗")
        
        print(f"\n  ✓ Downloaded {downloaded}/{images_per_class} {class_name} images")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Download Complete!")
    print(f"{'='*60}")
    print(f"Total images downloaded: {total_downloaded}")
    print(f"\nImages saved to:")
    for class_name in COCO_CLASSES.keys():
        class_dir = base_path / 'detection' / class_name
        if class_dir.exists():
            count = len(list(class_dir.glob('*.jpg')))
            print(f"  {class_name:10s}: {count:3d} images in {class_dir}")
    
    print(f"\n{'='*60}")
    print("Next Steps:")
    print(f"{'='*60}")
    print("1. For door images: Take photos yourself (not in COCO)")
    print("2. For OCR images: Take photos of text/signs/screens")
    print("3. For scene images: Take photos of indoor/outdoor scenes")
    print("\nSee test_data/DATA_COLLECTION_GUIDE.md for details")
    print("\nRun evaluation:")
    print("  python scripts/run_evaluation_example.py")

def download_annotations():
    """Helper to download COCO annotations"""
    print("Downloading COCO 2017 annotations...")
    ann_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
    
    ann_path = Path('coco_annotations')
    ann_path.mkdir(exist_ok=True)
    
    zip_path = ann_path / 'annotations_trainval2017.zip'
    
    if zip_path.exists():
        print(f"✓ Annotations already downloaded: {zip_path}")
        return
    
    print(f"Downloading from: {ann_url}")
    print("This is ~250MB and may take a few minutes...")
    
    try:
        urllib.request.urlretrieve(ann_url, zip_path)
        print(f"✓ Downloaded to: {zip_path}")
        print("\nNow extract the annotations:")
        print(f"  unzip {zip_path} -d {ann_path}")
    except Exception as e:
        print(f"✗ Download failed: {e}")
        print("\nManual download:")
        print(f"  wget {ann_url}")
        print(f"  unzip annotations_trainval2017.zip")
        print(f"  mv annotations/* {ann_path}/")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Download COCO test images')
    parser.add_argument('--images-per-class', type=int, default=30,
                       help='Number of images per class (default: 30)')
    parser.add_argument('--train', action='store_true',
                       help='Use training set instead of validation set')
    parser.add_argument('--download-annotations', action='store_true',
                       help='Download COCO annotations')
    
    args = parser.parse_args()
    
    if args.download_annotations:
        download_annotations()
    else:
        download_coco_images(
            images_per_class=args.images_per_class,
            use_val=not args.train
        )
