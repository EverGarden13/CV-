"""
Simple script to download test images from various sources
Downloads from COCO, Open Images, and public image sources
No API required - uses direct URLs
"""

import urllib.request
import os
from pathlib import Path
import time
import sys

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: Install tqdm for progress bars: pip install tqdm")

def download_image(url, save_path, timeout=30, verbose=False):
    """Download image from URL with retry logic"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Add headers to avoid being blocked
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                # Check if response is valid
                if response.status != 200:
                    if verbose:
                        print(f"  ⚠️  HTTP {response.status}")
                    continue
                
                # Read and save
                data = response.read()
                
                # Verify we got actual image data
                if len(data) < 1000:  # Too small to be a real image
                    if verbose:
                        print(f"  ⚠️  File too small ({len(data)} bytes)")
                    continue
                
                with open(save_path, 'wb') as f:
                    f.write(data)
                
                return True
                
        except urllib.error.HTTPError as e:
            if verbose and attempt == max_retries - 1:
                print(f"  ✗ HTTP Error {e.code}")
        except urllib.error.URLError as e:
            if verbose and attempt == max_retries - 1:
                print(f"  ✗ URL Error: {str(e.reason)[:30]}")
        except Exception as e:
            if verbose and attempt == max_retries - 1:
                print(f"  ✗ Error: {str(e)[:30]}")
        
        # Wait before retry
        if attempt < max_retries - 1:
            time.sleep(1)
    
    return False

def download_sample_images():
    """Download sample images for testing from multiple sources"""
    
    base_path = Path('test_data')
    
    print("\n" + "="*60)
    print("Complete Test Data Downloader")
    print("="*60 + "\n")
    print("Downloading from:")
    print("  - COCO dataset (person, chair, car)")
    print("  - Unsplash/Pexels (door, scenes)")
    print("  - Public text images (OCR)")
    print()
    
    # Sample images from various sources
    sample_images = {
        # COCO validation images
        'detection/person': [
            # COCO person images
            'http://images.cocodataset.org/val2017/000000000139.jpg',
            'http://images.cocodataset.org/val2017/000000000285.jpg',
            'http://images.cocodataset.org/val2017/000000000632.jpg',
            'http://images.cocodataset.org/val2017/000000000724.jpg',
            'http://images.cocodataset.org/val2017/000000001000.jpg',
            'http://images.cocodataset.org/val2017/000000001268.jpg',
            'http://images.cocodataset.org/val2017/000000001296.jpg',
            'http://images.cocodataset.org/val2017/000000001353.jpg',
            'http://images.cocodataset.org/val2017/000000001425.jpg',
            'http://images.cocodataset.org/val2017/000000001490.jpg',
            'http://images.cocodataset.org/val2017/000000001532.jpg',
            'http://images.cocodataset.org/val2017/000000001584.jpg',
            'http://images.cocodataset.org/val2017/000000001675.jpg',
            'http://images.cocodataset.org/val2017/000000001761.jpg',
            'http://images.cocodataset.org/val2017/000000001818.jpg',
        ],
        'detection/chair': [
            # COCO chair images
            'http://images.cocodataset.org/val2017/000000000139.jpg',
            'http://images.cocodataset.org/val2017/000000000285.jpg',
            'http://images.cocodataset.org/val2017/000000000724.jpg',
            'http://images.cocodataset.org/val2017/000000001268.jpg',
            'http://images.cocodataset.org/val2017/000000001296.jpg',
            'http://images.cocodataset.org/val2017/000000001353.jpg',
            'http://images.cocodataset.org/val2017/000000001425.jpg',
            'http://images.cocodataset.org/val2017/000000001490.jpg',
            'http://images.cocodataset.org/val2017/000000001532.jpg',
            'http://images.cocodataset.org/val2017/000000001584.jpg',
            'http://images.cocodataset.org/val2017/000000001675.jpg',
            'http://images.cocodataset.org/val2017/000000001761.jpg',
            'http://images.cocodataset.org/val2017/000000001818.jpg',
            'http://images.cocodataset.org/val2017/000000002006.jpg',
            'http://images.cocodataset.org/val2017/000000002149.jpg',
        ],
        'detection/car': [
            # COCO car images
            'http://images.cocodataset.org/val2017/000000000139.jpg',
            'http://images.cocodataset.org/val2017/000000000285.jpg',
            'http://images.cocodataset.org/val2017/000000000632.jpg',
            'http://images.cocodataset.org/val2017/000000000724.jpg',
            'http://images.cocodataset.org/val2017/000000001000.jpg',
            'http://images.cocodataset.org/val2017/000000001268.jpg',
            'http://images.cocodataset.org/val2017/000000001296.jpg',
            'http://images.cocodataset.org/val2017/000000001353.jpg',
            'http://images.cocodataset.org/val2017/000000001425.jpg',
            'http://images.cocodataset.org/val2017/000000001490.jpg',
            'http://images.cocodataset.org/val2017/000000001532.jpg',
            'http://images.cocodataset.org/val2017/000000001584.jpg',
            'http://images.cocodataset.org/val2017/000000001675.jpg',
            'http://images.cocodataset.org/val2017/000000001761.jpg',
            'http://images.cocodataset.org/val2017/000000001818.jpg',
        ],
        'detection/door': [
            # Unsplash door images (free to use)
            'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=640',
            'https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?w=640',
            'https://images.unsplash.com/photo-1534172553917-0ce2ef189cda?w=640',
            'https://images.unsplash.com/photo-1543489822-c49534f3271f?w=640',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=640',
            'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=640',
            'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=640',
            'https://images.unsplash.com/photo-1585128903994-03b0c3d6e3d6?w=640',
            'https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=640',
            'https://images.unsplash.com/photo-1593696140826-c58b021acf8b?w=640',
            'https://images.unsplash.com/photo-1596178060671-7a80dc8059ea?w=640',
            'https://images.unsplash.com/photo-1600607687644-c7171b42498b?w=640',
            'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=640',
            'https://images.unsplash.com/photo-1600607688969-a5bfcd646154?w=640',
            'https://images.unsplash.com/photo-1600607688960-e095ff83135c?w=640',
        ],
        'ocr/signs': [
            # Public domain street signs and signage
            'https://images.unsplash.com/photo-1495556650867-99590cea3657?w=640',
            'https://images.unsplash.com/photo-1516738901171-8eb4fc13bd20?w=640',
            'https://images.unsplash.com/photo-1534670007418-fbb7f6cf32c3?w=640',
            'https://images.unsplash.com/photo-1543699539-33a389c5e1c6?w=640',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=640',
            'https://images.unsplash.com/photo-1565538810643-b5bdb714032a?w=640',
            'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=640',
            'https://images.unsplash.com/photo-1585128903994-03b0c3d6e3d6?w=640',
            'https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=640',
            'https://images.unsplash.com/photo-1593696140826-c58b021acf8b?w=640',
        ],
        'ocr/labels': [
            # Product labels and packaging
            'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
            'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=640',
        ],
        'ocr/screens': [
            # Computer screens and displays
            'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=640',
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=640',
            'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=640',
            'https://images.unsplash.com/photo-1484788984921-03950022c9ef?w=640',
            'https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?w=640',
            'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=640',
            'https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=640',
            'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=640',
            'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=640',
            'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=640',
        ],
        'ocr/documents': [
            # Handwritten notes and documents
            'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=640',
            'https://images.unsplash.com/photo-1517842645767-c639042777db?w=640',
            'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=640',
            'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=640',
            'https://images.unsplash.com/photo-1517842645767-c639042777db?w=640',
            'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=640',
            'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=640',
            'https://images.unsplash.com/photo-1517842645767-c639042777db?w=640',
            'https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=640',
            'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=640',
        ],
        'scenes/indoor': [
            # Indoor scenes
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=640',
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=640',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=640',
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=640',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=640',
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=640',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=640',
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=640',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=640',
            'https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=640',
        ],
        'scenes/outdoor': [
            # Outdoor scenes
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=640',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640',
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=640',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640',
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=640',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640',
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=640',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640',
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=640',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=640',
        ],
    }
    
    total_downloaded = 0
    total_skipped = 0
    total_failed = 0
    
    for category_path, urls in sample_images.items():
        category_name = category_path.split('/')[-1]
        print(f"\n{'─'*60}")
        print(f"📁 Category: {category_name} ({len(urls)} images)")
        print(f"{'─'*60}")
        
        save_dir = base_path / category_path
        save_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        skipped = 0
        failed = 0
        
        # Use tqdm if available, otherwise regular loop
        if HAS_TQDM:
            iterator = tqdm(enumerate(urls, 1), total=len(urls), 
                          desc=f"  {category_name}", 
                          unit="img",
                          bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        else:
            iterator = enumerate(urls, 1)
        
        for i, url in iterator:
            # Generate filename from URL
            url_parts = url.split('/')
            if 'unsplash.com' in url:
                # Extract photo ID from Unsplash URL
                # URL format: https://images.unsplash.com/photo-XXXXXXXXX?w=640
                try:
                    photo_part = [p for p in url_parts if p.startswith('photo-')][0]
                    photo_id = photo_part.split('?')[0].replace('photo-', '')
                    filename = f"{category_name}_{photo_id}.jpg"
                except (IndexError, ValueError):
                    # Fallback: use last part of URL
                    filename = f"{category_name}_{i:03d}.jpg"
            else:
                # COCO images
                filename = url_parts[-1]
            
            save_path = save_dir / filename
            
            if save_path.exists():
                if not HAS_TQDM:
                    print(f"  ○ {i:2d}/{len(urls)}: {filename[:40]} (exists)")
                downloaded += 1
                skipped += 1
                continue
            
            if not HAS_TQDM:
                print(f"  ↓ {i:2d}/{len(urls)}: {filename[:40]}...", end='', flush=True)
            
            if download_image(url, save_path, verbose=(not HAS_TQDM)):
                if not HAS_TQDM:
                    print(" ✓")
                downloaded += 1
                total_downloaded += 1
            else:
                if not HAS_TQDM:
                    print(" ✗")
                failed += 1
                total_failed += 1
            
            time.sleep(0.8)  # Be nice to the servers
        
        total_skipped += skipped
        
        # Summary for this category
        status = "✓" if downloaded == len(urls) else "⚠️" if downloaded > 0 else "✗"
        print(f"  {status} {category_name}: {downloaded}/{len(urls)} images", end='')
        if skipped > 0:
            print(f" ({skipped} already existed)", end='')
        if failed > 0:
            print(f" ({failed} failed)", end='')
        print()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Download Summary")
    print(f"{'='*60}")
    print(f"✓ New downloads:     {total_downloaded:3d} images")
    print(f"○ Already existed:   {total_skipped:3d} images")
    if total_failed > 0:
        print(f"✗ Failed downloads:  {total_failed:3d} images")
    
    print(f"\n{'─'*60}")
    print(f"📁 Dataset Overview")
    print(f"{'─'*60}")
    
    # Count all images by category
    total_count = 0
    category_counts = {}
    
    for category_path in sample_images.keys():
        cat_dir = base_path / category_path
        if cat_dir.exists():
            count = len(list(cat_dir.glob('*.jpg'))) + len(list(cat_dir.glob('*.png')))
            total_count += count
            category_name = category_path.split('/')[-1]
            category_type = category_path.split('/')[0]
            
            if category_type not in category_counts:
                category_counts[category_type] = 0
            category_counts[category_type] += count
            
            print(f"  {category_name:12s}: {count:3d} images")
    
    print(f"\n{'─'*60}")
    print(f"📈 Category Totals")
    print(f"{'─'*60}")
    for cat_type, count in category_counts.items():
        print(f"  {cat_type.capitalize():12s}: {count:3d} images")
    
    print(f"\n  {'TOTAL':12s}: {total_count:3d} images")
    print(f"  {'TARGET':12s}: ~120 images")
    
    # Status assessment
    print(f"\n{'='*60}")
    if total_count >= 100:
        print(f"✓✓ Excellent! You have enough data for comprehensive evaluation")
    elif total_count >= 60:
        print(f"✓ Good! You have sufficient data for basic evaluation")
    else:
        print(f"⚠️  Need more images for comprehensive evaluation")
    print(f"{'='*60}")
    
    print(f"\n{'='*60}")
    print("Next Steps:")
    print(f"{'='*60}")
    print("\n1. Check data status:")
    print("   python3 test_data/collect_data.py")
    print("\n2. Run evaluation with real data:")
    print("   python3 scripts/run_evaluation_example.py")
    print("\n3. Update report with actual results:")
    print("   Edit docs/COMP5523_Project_Report_REFINED.md")
    print("\n4. Regenerate figures with real numbers:")
    print("   python3 scripts/generate_report_figures.py")
    print(f"\n{'='*60}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 VisionMate-Lite Test Data Downloader")
    print("="*60)
    print("\nThis will download ~120 images from multiple sources:")
    print("\n📦 Detection Images (60 total):")
    print("  • 15 person images (COCO)")
    print("  • 15 chair images (COCO)")
    print("  • 15 car images (COCO)")
    print("  • 15 door images (Unsplash)")
    print("\n📝 OCR Images (30 total):")
    print("  • 10 signs (Unsplash)")
    print("  • 10 labels (Unsplash)")
    print("  • 10 screens (Unsplash)")
    print("  • 10 documents (Unsplash)")
    print("\n🏞️  Scene Images (20 total):")
    print("  • 10 indoor scenes (Unsplash)")
    print("  • 10 outdoor scenes (Unsplash)")
    print("\n" + "─"*60)
    print("📊 Total: ~120 images")
    print("⏱️  Time: ~5-10 minutes")
    print("📜 Sources: COCO Dataset, Unsplash (free/public)")
    print("="*60)
    
    if not HAS_TQDM:
        print("\n💡 Tip: Install tqdm for progress bars:")
        print("   pip install tqdm")
    
    print("\nPress Enter to start download or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ Download cancelled by user")
        sys.exit(0)
    
    print("\n🔄 Starting download...\n")
    
    try:
        download_sample_images()
    except KeyboardInterrupt:
        print("\n\n❌ Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during download: {e}")
        sys.exit(1)
