"""
Download OCR dataset from Kaggle for evaluation
"""
import kagglehub
import shutil
from pathlib import Path

print("Downloading OCR dataset from Kaggle...")
print("-" * 50)

# Download latest version
path = kagglehub.dataset_download("preatcher/standard-ocr-dataset")
print(f"✓ Path to dataset files: {path}")

# Create target directory
target_dir = Path("test_data/ocr")
target_dir.mkdir(parents=True, exist_ok=True)

# Copy files to our test_data directory
source_path = Path(path)
print(f"\nCopying files from {source_path} to {target_dir}...")

# List what we got
files = list(source_path.rglob("*"))
print(f"Found {len(files)} files in dataset")

# Copy image files (limit to 100)
MAX_IMAGES = 100
image_count = 0
for file in files:
    if image_count >= MAX_IMAGES:
        break
    if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        dest = target_dir / file.name
        shutil.copy2(file, dest)
        image_count += 1
        if image_count <= 5:
            print(f"  Copied: {file.name}")

print(f"\n✓ Copied {image_count} images to {target_dir} (limited to {MAX_IMAGES})")
print("\nDataset ready for OCR evaluation!")
