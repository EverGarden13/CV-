#!/usr/bin/env python3
"""
Test script for scene classification functionality.

This script tests the scene classification module to ensure it works correctly
with the VisionMate-Lite system.
"""

import sys
import os
import numpy as np
import cv2
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scene_classifier import create_scene_classifier, TORCH_AVAILABLE
from src.audio import AudioManager
from src.scene_integration import SceneIntegration


def test_scene_classifier():
    """Test basic scene classifier functionality."""
    print("Testing Scene Classifier")
    print("=" * 40)
    
    # Check if PyTorch is available
    print(f"PyTorch available: {TORCH_AVAILABLE}")
    
    # Create scene classifier
    classifier = create_scene_classifier(update_interval=2.0)  # Fast for testing
    
    print(f"Scene classifier enabled: {classifier.is_enabled()}")
    
    if not classifier.is_enabled():
        print("Scene classification not available - skipping tests")
        return False
    
    # Create test frame
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test classification timing
    print("\nTesting classification timing...")
    print(f"Should classify: {classifier.should_classify()}")
    
    # Test scene classification
    print("\nTesting scene classification...")
    scene = classifier.classify_scene(test_frame)
    print(f"Classified scene: {scene}")
    
    # Test change detection
    print(f"Scene changed: {classifier.has_scene_changed()}")
    
    # Test announcement
    announcement = classifier.get_scene_announcement()
    print(f"Scene announcement: {announcement}")
    
    return True


def test_audio_scene_integration():
    """Test scene classification integration with audio."""
    print("\nTesting Audio Scene Integration")
    print("=" * 40)
    
    # Initialize audio manager
    audio_manager = AudioManager()
    
    # Test scene announcement
    test_scenes = ["office", "corridor", "street"]
    
    for scene in test_scenes:
        print(f"Testing scene announcement: {scene}")
        success = audio_manager.speak_scene(scene)
        print(f"Announcement success: {success}")
        time.sleep(1)  # Brief pause
    
    audio_manager.cleanup()
    return True


def test_scene_integration():
    """Test full scene integration module."""
    print("\nTesting Scene Integration Module")
    print("=" * 40)
    
    # Initialize components
    audio_manager = AudioManager()
    scene_integration = SceneIntegration(
        audio_manager, 
        update_interval=3.0,  # Fast for testing
        enabled=True
    )
    
    print(f"Scene integration enabled: {scene_integration.is_enabled()}")
    
    if not scene_integration.is_enabled():
        print("Scene integration not available - skipping tests")
        audio_manager.cleanup()
        return False
    
    # Create test frame
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Test frame processing
    print("\nTesting frame processing...")
    for i in range(3):
        print(f"Processing frame {i+1}...")
        announced_scene = scene_integration.process_frame(test_frame)
        
        if announced_scene:
            print(f"Scene announced: {announced_scene}")
        else:
            current_scene = scene_integration.get_current_scene()
            print(f"Current scene: {current_scene} (no announcement)")
        
        time.sleep(1)
    
    # Test forced update
    print("\nTesting forced scene update...")
    forced_scene = scene_integration.force_scene_update(test_frame)
    print(f"Forced scene: {forced_scene}")
    
    audio_manager.cleanup()
    return True


def test_with_real_camera():
    """Test scene classification with real camera feed."""
    print("\nTesting with Real Camera (if available)")
    print("=" * 40)
    
    try:
        # Try to initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Camera not available - skipping real camera test")
            return False
        
        # Initialize scene integration
        audio_manager = AudioManager()
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=5.0,  # Reasonable interval
            enabled=True
        )
        
        if not scene_integration.is_enabled():
            print("Scene integration not available")
            cap.release()
            audio_manager.cleanup()
            return False
        
        print("Press 'q' to quit, 's' to force scene classification")
        print("Scene classification will happen automatically every 5 seconds")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process frame for scene classification
            if frame_count % 30 == 0:  # Every 30 frames (~1 second at 30fps)
                announced_scene = scene_integration.process_frame(frame)
                if announced_scene:
                    print(f"Scene announced: {announced_scene}")
            
            # Display frame
            cv2.imshow('VisionMate Scene Classification Test', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # Force scene classification
                forced_scene = scene_integration.force_scene_update(frame)
                print(f"Forced scene classification: {forced_scene}")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        audio_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"Error in camera test: {e}")
        return False


def main():
    """Run all scene classification tests."""
    print("VisionMate-Lite Scene Classification Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Basic scene classifier
    total_tests += 1
    if test_scene_classifier():
        tests_passed += 1
        print("✓ Scene classifier test passed")
    else:
        print("✗ Scene classifier test failed")
    
    # Test 2: Audio integration
    total_tests += 1
    if test_audio_scene_integration():
        tests_passed += 1
        print("✓ Audio scene integration test passed")
    else:
        print("✗ Audio scene integration test failed")
    
    # Test 3: Full integration
    total_tests += 1
    if test_scene_integration():
        tests_passed += 1
        print("✓ Scene integration test passed")
    else:
        print("✗ Scene integration test failed")
    
    # Test 4: Real camera (optional)
    print("\nOptional: Test with real camera? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response == 'y':
            total_tests += 1
            if test_with_real_camera():
                tests_passed += 1
                print("✓ Real camera test passed")
            else:
                print("✗ Real camera test failed")
    except KeyboardInterrupt:
        print("\nSkipping real camera test")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("All tests passed! Scene classification is working correctly.")
        return 0
    else:
        print("Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())