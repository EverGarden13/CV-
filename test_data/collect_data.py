#!/usr/bin/env python3
"""
Data Collection Helper Script for VisionMate-Lite
Helps organize and validate test datasets
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

def count_images_in_directory(directory):
    """Count image files in a directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    count = 0
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if Path(file).suffix.lower() in image_extensions:
                count += 1
    return count

def validate_naming_convention(directory):
    """Check if files follow the naming convention"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    valid_files = []
    invalid_files = []
    
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if Path(file).suffix.lower() in image_extensions:
                # Expected format: category_condition_number.jpg
                parts = Path(file).stem.split('_')
                if len(parts) >= 3:
                    valid_files.append(file)
                else:
                    invalid_files.append(file)
    
    return valid_files, invalid_files

def generate_data_collection_report():
    """Generate a report on current test data status"""
    base_path = Path(__file__).parent
    
    print("VisionMate-Lite Test Data Collection Report")
    print("=" * 50)
    
    # Detection data analysis
    print("\nDETECTION DATASET:")
    detection_categories = ['person', 'chair', 'car', 'door', 'mixed']
    total_detection = 0
    
    for category in detection_categories:
        dir_path = base_path / 'detection' / category
        count = count_images_in_directory(dir_path)
        total_detection += count
        status = "✓" if count >= 25 else "⚠" if count >= 10 else "✗"
        print(f"  {category:8}: {count:3d} images {status}")
    
    print(f"  Total Detection: {total_detection} images")
    print(f"  Target: 100-200 images")
    
    # OCR data analysis  
    print("\nOCR DATASET:")
    ocr_categories = ['signs', 'labels', 'screens', 'documents']
    total_ocr = 0
    
    for category in ocr_categories:
        dir_path = base_path / 'ocr' / category
        count = count_images_in_directory(dir_path)
        total_ocr += count
        status = "✓" if count >= 15 else "⚠" if count >= 5 else "✗"
        print(f"  {category:9}: {count:3d} images {status}")
    
    print(f"  Total OCR: {total_ocr} images")
    print(f"  Target: 50-100 images")
    
    # Overall status
    print(f"\nOVERALL STATUS:")
    total_images = total_detection + total_ocr
    print(f"  Total Images: {total_images}")
    print(f"  Target Range: 150-300 images")
    
    if total_images >= 150:
        print("  Status: ✓ Sufficient data collected")
    elif total_images >= 75:
        print("  Status: ⚠ Partial data collected")
    else:
        print("  Status: ✗ More data needed")
    
    # Naming convention check
    print(f"\nNAMING CONVENTION CHECK:")
    all_categories = [(f'detection/{cat}', cat) for cat in detection_categories] + \
                    [(f'ocr/{cat}', cat) for cat in ocr_categories]
    
    total_valid = 0
    total_invalid = 0
    
    for dir_name, cat_name in all_categories:
        dir_path = base_path / dir_name
        valid, invalid = validate_naming_convention(dir_path)
        total_valid += len(valid)
        total_invalid += len(invalid)
        
        if len(invalid) > 0:
            print(f"  {cat_name}: {len(invalid)} files need renaming")
    
    if total_invalid == 0:
        print("  All files follow naming convention ✓")
    else:
        print(f"  {total_invalid} files need renaming ⚠")
    
    # Recommendations
    print(f"\nRECOMMENDations:")
    if total_detection < 100:
        needed = 100 - total_detection
        print(f"  - Collect {needed} more detection images")
    
    if total_ocr < 50:
        needed = 50 - total_ocr
        print(f"  - Collect {needed} more OCR images")
    
    if total_invalid > 0:
        print(f"  - Rename {total_invalid} files to follow convention")
    
    print(f"  - Follow ethics guidelines in test_data/README.md")
    print(f"  - Document metadata for evaluation")

def create_sample_metadata_file():
    """Create a sample metadata file for documentation"""
    metadata_content = """# Test Data Metadata

## Detection Images

### person_indoor_bright_001.jpg
- Location: Office environment
- Lighting: Bright fluorescent lighting
- Distance: Medium (3-5 meters)
- Objects: Single person standing
- Challenges: None

### chair_outdoor_dim_002.jpg  
- Location: Outdoor patio
- Lighting: Overcast, dim natural light
- Distance: Close (1-2 meters)
- Objects: Wooden chair
- Challenges: Low contrast background

## OCR Images

### sign_street_sunny_001.jpg
- Location: Street intersection
- Lighting: Bright sunlight
- Text Type: Street sign, white text on green
- Font Size: Large, sans-serif
- Challenges: Slight glare

### label_product_close_002.jpg
- Location: Indoor, kitchen
- Lighting: Mixed (natural + artificial)
- Text Type: Product label, black text on white
- Font Size: Small, serif font
- Challenges: Curved surface
"""
    
    metadata_path = Path(__file__).parent / 'metadata_sample.md'
    with open(metadata_path, 'w') as f:
        f.write(metadata_content)
    
    print(f"Sample metadata file created: {metadata_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create-metadata":
        create_sample_metadata_file()
    else:
        generate_data_collection_report()
        print(f"\nTo create sample metadata file:")
        print(f"  python collect_data.py --create-metadata")