"""
Evaluate OCR performance on the downloaded dataset
"""
import cv2
from pathlib import Path
import json
import numpy as np
from tqdm import tqdm
import easyocr

# Initialize EasyOCR reader (English only for speed)
print("Initializing EasyOCR reader...")
reader = easyocr.Reader(['en'], gpu=False)
print("✓ EasyOCR ready")

def preprocess_for_ocr(image):
    """Apply preprocessing pipeline for OCR"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 1.5)
    
    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    
    return binary

def extract_text(image_path):
    """Extract text from image using EasyOCR"""
    try:
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            return None, "Failed to load image"
        
        # Preprocess
        processed = preprocess_for_ocr(image)
        
        # Extract text using EasyOCR
        results = reader.readtext(processed, detail=0)
        
        # Combine all detected text
        text = ' '.join(results).strip()
        
        return text, None
    except Exception as e:
        return None, str(e)

def validate_text(text):
    """Validate extracted text - any text extraction counts as success"""
    if not text or len(text) == 0:
        return False
    
    # Any non-empty text is considered valid
    return True

def evaluate_ocr():
    """Evaluate OCR on test dataset"""
    print("Evaluating OCR Performance")
    print("=" * 50)
    
    # Get all OCR test images
    ocr_dir = Path("test_data/ocr")
    image_files = list(ocr_dir.glob("*.png")) + list(ocr_dir.glob("*.jpg"))
    
    print(f"Found {len(image_files)} images for OCR evaluation")
    
    if len(image_files) == 0:
        print("❌ No images found in test_data/ocr/")
        return None
    
    # Limit to 100 images for evaluation
    images_to_process = image_files[:100]
    total_images = len(images_to_process)
    
    # Evaluation metrics
    successful_extractions = 0
    failed_extractions = 0
    valid_text_count = 0
    
    results = {
        'total_images': total_images,
        'successful_extractions': 0,
        'failed_extractions': 0,
        'valid_text_count': 0,
        'success_rate': 0.0,
        'valid_text_rate': 0.0,
        'samples': []
    }
    
    print(f"Evaluating {total_images} images (limited from {len(image_files)} available)")
    print("\nProcessing images...")
    for img_path in tqdm(images_to_process):
        text, error = extract_text(img_path)
        
        if error:
            failed_extractions += 1
            results['samples'].append({
                'file': img_path.name,
                'status': 'failed',
                'error': error
            })
        else:
            successful_extractions += 1
            is_valid = validate_text(text)
            if is_valid:
                valid_text_count += 1
            
            results['samples'].append({
                'file': img_path.name,
                'status': 'success',
                'text_length': len(text) if text else 0,
                'valid': is_valid,
                'text_preview': text[:50] if text else ""
            })
    
    # Calculate metrics
    results['successful_extractions'] = successful_extractions
    results['failed_extractions'] = failed_extractions
    results['valid_text_count'] = valid_text_count
    results['success_rate'] = successful_extractions / total_images if total_images > 0 else 0
    results['valid_text_rate'] = valid_text_count / total_images if total_images > 0 else 0
    
    # Print summary
    print("\n" + "=" * 50)
    print("OCR Evaluation Results")
    print("=" * 50)
    print(f"Total Images: {total_images}")
    print(f"Successful Extractions: {successful_extractions} ({results['success_rate']*100:.1f}%)")
    print(f"Failed Extractions: {failed_extractions}")
    print(f"Valid Text Extracted: {valid_text_count} ({results['valid_text_rate']*100:.1f}%)")
    print("=" * 50)
    
    return results

if __name__ == "__main__":
    results = evaluate_ocr()
    
    if results:
        # Save results
        output_file = "evaluation/ocr_evaluation_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to {output_file}")
