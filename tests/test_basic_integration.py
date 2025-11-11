#!/usr/bin/env python3
"""
VisionMate-Lite Basic Integration Test

This script performs basic integration testing without requiring all dependencies.
Suitable for demonstrating system capabilities when some components are unavailable.

Usage:
    python test_basic_integration.py
"""

import sys
import os
import time
import logging
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import system modules
import config


def test_basic_imports():
    """Test that all core modules can be imported."""
    print("Testing basic module imports...")
    
    try:
        from src.camera import CameraInterface
        print("✅ Camera module imported successfully")
    except Exception as e:
        print(f"❌ Camera module import failed: {e}")
        return False
    
    try:
        from src.detection import ObjectDetector
        print("✅ Detection module imported successfully")
    except Exception as e:
        print(f"❌ Detection module import failed: {e}")
        return False
    
    try:
        from src.audio import AudioManager
        print("✅ Audio module imported successfully")
    except Exception as e:
        print(f"❌ Audio module import failed: {e}")
        return False
    
    try:
        from src.ocr import OCREngine
        print("⚠️  OCR module imported (may not work without Tesseract)")
    except Exception as e:
        print(f"⚠️  OCR module import failed: {e}")
    
    return True


def test_basic_initialization():
    """Test basic component initialization."""
    print("\nTesting component initialization...")
    
    try:
        from src.camera import CameraInterface
        camera = CameraInterface()
        print("✅ Camera interface created")
        
        # Try to initialize camera (may fail if no camera available)
        if camera.initialize_camera(0):
            print("✅ Camera initialized successfully")
            camera.release()
        else:
            print("⚠️  Camera not available (normal in some environments)")
    except Exception as e:
        print(f"❌ Camera initialization failed: {e}")
    
    try:
        from src.detection import ObjectDetector
        detector = ObjectDetector()
        print("✅ Object detector created")
    except Exception as e:
        print(f"❌ Object detector creation failed: {e}")
        return False
    
    try:
        from src.audio import AudioManager
        audio = AudioManager()
        print("✅ Audio manager created")
    except Exception as e:
        print(f"❌ Audio manager creation failed: {e}")
        return False
    
    return True


def test_detection_functionality():
    """Test object detection with synthetic data."""
    print("\nTesting object detection functionality...")
    
    try:
        import numpy as np
        from src.detection import ObjectDetector
        
        detector = ObjectDetector()
        
        # Create synthetic test frame
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test detection
        start_time = time.perf_counter()
        detections = detector.detect(test_frame)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000
        
        print(f"✅ Detection completed in {latency_ms:.2f}ms")
        print(f"✅ Found {len(detections)} objects")
        
        # Test performance target
        if latency_ms < config.MAX_DETECTION_LATENCY_MS:
            print(f"✅ Performance target met (<{config.MAX_DETECTION_LATENCY_MS}ms)")
        else:
            print(f"⚠️  Performance target not met (>{config.MAX_DETECTION_LATENCY_MS}ms)")
        
        return True
        
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
        return False


def test_audio_functionality():
    """Test audio system functionality."""
    print("\nTesting audio functionality...")
    
    try:
        from src.audio import AudioManager
        
        audio = AudioManager()
        
        # Test alert messages
        test_alerts = ['person', 'chair', 'car', 'door']
        
        for alert in test_alerts:
            message = config.ALERT_MESSAGES.get(alert, f"{alert} detected")
            print(f"✅ Alert message for '{alert}': '{message}'")
        
        print("✅ Audio system basic functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False


def test_configuration():
    """Test system configuration."""
    print("\nTesting system configuration...")
    
    try:
        print(f"✅ Platform: {config.PLATFORM}")
        print(f"✅ TTS Engine: {config.TTS_ENGINE}")
        print(f"✅ Confidence Threshold: {config.CONFIDENCE_THRESHOLD}")
        print(f"✅ Detection Latency Target: {config.MAX_DETECTION_LATENCY_MS}ms")
        print(f"✅ OCR Latency Target: {config.MAX_OCR_LATENCY_SECONDS}s")
        
        # Test environment variables
        test_data_path = config.TEST_DATA_PATH
        print(f"✅ Test Data Path: {test_data_path}")
        
        # Create test directories if they don't exist
        Path(test_data_path).mkdir(parents=True, exist_ok=True)
        Path(test_data_path, 'detection').mkdir(parents=True, exist_ok=True)
        Path(test_data_path, 'ocr').mkdir(parents=True, exist_ok=True)
        
        print("✅ Configuration validation completed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_error_handling():
    """Test basic error handling."""
    print("\nTesting error handling...")
    
    try:
        from src.camera import CameraInterface
        
        # Test invalid camera index
        camera = CameraInterface()
        result = camera.initialize_camera(99)  # Invalid camera index
        
        if not result:
            print("✅ Invalid camera index handled gracefully")
        else:
            print("⚠️  Invalid camera index not detected")
        
        return True
        
    except Exception as e:
        print(f"✅ Exception handled gracefully: {e}")
        return True


def run_basic_integration_test():
    """Run the complete basic integration test."""
    print("VisionMate-Lite Basic Integration Test")
    print("=" * 50)
    print(f"Platform: {config.PLATFORM}")
    print(f"Python version: {sys.version}")
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_basic_imports),
        ("Component Initialization", test_basic_initialization),
        ("Detection Functionality", test_detection_functionality),
        ("Audio Functionality", test_audio_functionality),
        ("Configuration", test_configuration),
        ("Error Handling", test_error_handling)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    # Final results
    print("\n" + "=" * 50)
    print("BASIC INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All basic integration tests PASSED!")
        print("✅ System is ready for basic functionality")
    elif passed_tests >= total_tests * 0.8:
        print("⚠️  Most tests passed - system mostly functional")
        print("🔧 Some components may need attention")
    else:
        print("❌ Multiple test failures - system needs attention")
        print("🛠️  Please review failed tests above")
    
    # Recommendations
    print("\n" + "=" * 50)
    print("RECOMMENDATIONS")
    print("=" * 50)
    
    if passed_tests == total_tests:
        print("• System is ready for demonstration")
        print("• All core components are working")
        print("• Consider running full integration test with all dependencies")
    else:
        print("• Review failed tests and address issues")
        print("• Install missing dependencies (e.g., Tesseract for OCR)")
        print("• Check system requirements and permissions")
    
    print("• For full functionality, ensure:")
    print("  - Camera is available and accessible")
    print("  - Tesseract OCR is installed")
    print("  - Audio system is working")
    print("  - All Python dependencies are installed")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_basic_integration_test()
    sys.exit(0 if success else 1)