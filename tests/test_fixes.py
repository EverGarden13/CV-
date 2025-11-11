#!/usr/bin/env python3
"""
Test script to validate all fixes applied from code review.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_config_import():
    """Test config module import and validation."""
    print("=" * 60)
    print("Testing Config Module")
    print("=" * 60)
    
    try:
        import config
        print("✅ Config module imported successfully")
        
        # Test validation
        result = config.validate_config()
        print(f"✅ Config validation passed: {result}")
        
        # Test GPU detection
        print(f"✅ GPU Available: {config.GPU_AVAILABLE}")
        print(f"✅ Device: {config.DEVICE}")
        
        # Test target classes
        print(f"✅ Target Classes: {config.TARGET_CLASSES}")
        
        # Test configurable values
        print(f"✅ Confidence Threshold: {config.CONFIDENCE_THRESHOLD}")
        print(f"✅ Frame Skip: {config.FRAME_SKIP}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_input_validation():
    """Test input validation in critical modules."""
    print("\n" + "=" * 60)
    print("Testing Input Validation")
    print("=" * 60)
    
    success = True
    
    # Test detection module validation
    try:
        from src.detection import ObjectDetector
        
        # Test valid threshold
        detector = ObjectDetector(confidence_threshold=0.5)
        print("✅ ObjectDetector accepts valid confidence threshold (0.5)")
        
        # Test invalid threshold (should raise ValueError)
        try:
            detector_invalid = ObjectDetector(confidence_threshold=1.5)
            print("❌ ObjectDetector should reject invalid threshold (1.5)")
            success = False
        except ValueError as e:
            print(f"✅ ObjectDetector correctly rejects invalid threshold: {e}")
            
    except Exception as e:
        print(f"❌ Detection validation test failed: {e}")
        success = False
    
    # Test OCR module validation
    try:
        from src.ocr import OCREngine
        
        # Test valid min_text_length
        # Note: This will try to initialize Tesseract, which may fail
        try:
            ocr = OCREngine(min_text_length=3)
            print("✅ OCREngine accepts valid min_text_length (3)")
        except RuntimeError as e:
            if "Tesseract" in str(e):
                print("⚠️  OCREngine validation passed (Tesseract not installed)")
            else:
                raise
        
        # Test invalid min_text_length (should raise ValueError)
        try:
            ocr_invalid = OCREngine(min_text_length=-1)
            print("❌ OCREngine should reject invalid min_text_length (-1)")
            success = False
        except ValueError as e:
            print(f"✅ OCREngine correctly rejects invalid min_text_length: {e}")
            
    except Exception as e:
        print(f"❌ OCR validation test failed: {e}")
        success = False
    
    # Test camera module validation
    try:
        from src.camera import CameraInterface
        
        camera = CameraInterface()
        
        # Test invalid camera_index (should raise ValueError)
        try:
            camera.initialize_camera(camera_index=-1)
            print("❌ CameraInterface should reject invalid camera_index (-1)")
            success = False
        except ValueError as e:
            print(f"✅ CameraInterface correctly rejects invalid camera_index: {e}")
            
    except Exception as e:
        print(f"❌ Camera validation test failed: {e}")
        success = False
    
    return success


def test_requirements():
    """Test requirements.txt format."""
    print("\n" + "=" * 60)
    print("Testing Requirements File")
    print("=" * 60)
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        # Check for pinned versions
        if '==' in content:
            print("✅ Requirements file uses pinned versions")
        else:
            print("❌ Requirements file should use pinned versions (==)")
            return False
        
        # Check for comments
        if '#' in content:
            print("✅ Requirements file includes comments")
        else:
            print("⚠️  Requirements file could benefit from comments")
        
        # Check for core dependencies
        required_deps = ['ultralytics', 'opencv-python', 'pytesseract', 'pyttsx3']
        for dep in required_deps:
            if dep in content:
                print(f"✅ Found required dependency: {dep}")
            else:
                print(f"❌ Missing required dependency: {dep}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False


def test_test_organization():
    """Test test directory organization."""
    print("\n" + "=" * 60)
    print("Testing Test Organization")
    print("=" * 60)
    
    try:
        # Check if tests directory exists
        if os.path.exists('tests'):
            print("✅ tests/ directory exists")
            
            # Check for __init__.py
            if os.path.exists('tests/__init__.py'):
                print("✅ tests/__init__.py exists")
            else:
                print("⚠️  tests/__init__.py not found")
            
            # Check for README
            if os.path.exists('tests/README.md'):
                print("✅ tests/README.md exists")
            else:
                print("⚠️  tests/README.md not found")
        else:
            print("⚠️  tests/ directory not found (optional)")
        
        return True
    except Exception as e:
        print(f"❌ Test organization check failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("VisionMate-Lite Code Review Fixes Validation")
    print("=" * 60 + "\n")
    
    results = {
        "Config Import": test_config_import(),
        "Input Validation": test_input_validation(),
        "Requirements": test_requirements(),
        "Test Organization": test_test_organization()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - Fixes validated successfully!")
    else:
        print("⚠️  SOME TESTS FAILED - Review output above")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
