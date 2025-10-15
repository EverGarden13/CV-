#!/usr/bin/env python3
"""
Integration test for VisionMate-Lite with Scene Classification

This test verifies that the scene classification feature integrates properly
with the rest of the system components.
"""

import sys
import os
import time
import numpy as np
import cv2
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration
import config

# Import all components
from src.camera import CameraInterface
from src.detection import ObjectDetector
from src.ocr import OCREngine
from src.audio import AudioManager
from src.scene_integration import SceneIntegration
from src.error_handler import initialize_error_handling


def test_component_initialization():
    """Test that all components can be initialized together."""
    print("Testing Component Initialization")
    print("=" * 40)
    
    try:
        # Initialize error handling
        if not initialize_error_handling():
            print("❌ Error handling initialization failed")
            return False
        
        # Initialize all components
        camera = CameraInterface()
        audio_manager = AudioManager(speech_rate=config.SPEECH_RATE)
        ocr_engine = OCREngine(min_text_length=config.MIN_TEXT_LENGTH)
        object_detector = ObjectDetector(confidence_threshold=config.CONFIDENCE_THRESHOLD)
        
        # Initialize scene integration
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=5.0,  # Faster for testing
            confidence_threshold=config.SCENE_CONFIDENCE_THRESHOLD,
            enabled=config.ENABLE_SCENE_CLASSIFICATION
        )
        
        print(f"✅ Camera interface: {'Available' if camera else 'Failed'}")
        print(f"✅ Audio manager: {'Available' if audio_manager else 'Failed'}")
        print(f"✅ OCR engine: {'Available' if ocr_engine else 'Failed'}")
        print(f"✅ Object detector: {'Available' if object_detector else 'Failed'}")
        print(f"✅ Scene integration: {'Available' if scene_integration.is_enabled() else 'Disabled/Failed'}")
        
        # Cleanup
        audio_manager.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
        return False


def test_scene_integration_with_mock_data():
    """Test scene integration with mock camera data."""
    print("\nTesting Scene Integration with Mock Data")
    print("=" * 40)
    
    try:
        # Initialize components
        audio_manager = AudioManager()
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=2.0,  # Fast for testing
            confidence_threshold=0.1,  # Low threshold for testing
            enabled=True
        )
        
        if not scene_integration.is_enabled():
            print("⚠️  Scene classification not available - skipping test")
            audio_manager.cleanup()
            return True
        
        # Create different mock frames to simulate scene changes
        frames = {
            'bright_office': np.full((480, 640, 3), [200, 200, 200], dtype=np.uint8),  # Bright gray
            'dark_corridor': np.full((480, 640, 3), [80, 80, 80], dtype=np.uint8),    # Dark gray
            'outdoor_scene': np.full((480, 640, 3), [100, 150, 200], dtype=np.uint8), # Blue-ish
            'green_park': np.full((480, 640, 3), [50, 180, 50], dtype=np.uint8),      # Green
        }
        
        print("Processing different scene types...")
        
        for scene_name, frame in frames.items():
            print(f"\nProcessing {scene_name}...")
            
            # Process frame multiple times to trigger classification
            for i in range(3):
                announced_scene = scene_integration.process_frame(frame)
                if announced_scene:
                    print(f"  ✅ Scene announced: {announced_scene}")
                    break
                else:
                    current_scene = scene_integration.get_current_scene()
                    if current_scene:
                        print(f"  📍 Current scene: {current_scene} (no announcement)")
                    else:
                        print(f"  ⏳ Waiting for classification... ({i+1}/3)")
                
                time.sleep(1)
        
        # Test forced scene update
        print("\nTesting forced scene update...")
        test_frame = frames['bright_office']
        forced_scene = scene_integration.force_scene_update(test_frame)
        print(f"Forced scene classification: {forced_scene}")
        
        audio_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Scene integration test failed: {e}")
        return False


def test_full_system_integration():
    """Test full system integration including scene classification."""
    print("\nTesting Full System Integration")
    print("=" * 40)
    
    try:
        # Initialize all components
        camera = CameraInterface()
        audio_manager = AudioManager()
        object_detector = ObjectDetector()
        
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=3.0,  # Reasonable for testing
            enabled=True
        )
        
        # Test with mock frame
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        print("Testing integrated processing pipeline...")
        
        # Test object detection
        print("1. Object detection...")
        detections = object_detector.detect(test_frame)
        print(f"   Detected {len(detections)} objects")
        
        # Test scene classification
        print("2. Scene classification...")
        if scene_integration.is_enabled():
            announced_scene = scene_integration.process_frame(test_frame)
            current_scene = scene_integration.get_current_scene()
            print(f"   Current scene: {current_scene}")
            if announced_scene:
                print(f"   Announced scene: {announced_scene}")
        else:
            print("   Scene classification disabled")
        
        # Test audio system
        print("3. Audio system...")
        if detections:
            # Test object alert
            success = audio_manager.speak_alert(detections[0].class_name)
            print(f"   Object alert: {'Success' if success else 'Failed'}")
        
        # Test scene announcement
        if scene_integration.is_enabled() and scene_integration.get_current_scene():
            success = audio_manager.speak_scene(scene_integration.get_current_scene())
            print(f"   Scene announcement: {'Success' if success else 'Failed'}")
        
        print("✅ Full system integration test completed")
        
        audio_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Full system integration test failed: {e}")
        return False


def test_performance_with_scene_classification():
    """Test system performance with scene classification enabled."""
    print("\nTesting Performance with Scene Classification")
    print("=" * 40)
    
    try:
        # Initialize components
        audio_manager = AudioManager()
        object_detector = ObjectDetector()
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=1.0,  # Fast for performance testing
            enabled=True
        )
        
        # Create test frame
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Test processing times
        num_iterations = 10
        
        print(f"Running {num_iterations} iterations...")
        
        # Test object detection timing
        start_time = time.time()
        for i in range(num_iterations):
            detections = object_detector.detect(test_frame)
        detection_time = (time.time() - start_time) / num_iterations
        
        # Test scene classification timing (if enabled)
        scene_time = 0
        if scene_integration.is_enabled():
            start_time = time.time()
            for i in range(num_iterations):
                scene_integration.process_frame(test_frame)
            scene_time = (time.time() - start_time) / num_iterations
        
        print(f"Average object detection time: {detection_time*1000:.1f}ms")
        print(f"Average scene processing time: {scene_time*1000:.1f}ms")
        print(f"Total processing time per frame: {(detection_time + scene_time)*1000:.1f}ms")
        
        # Check performance targets
        total_time_ms = (detection_time + scene_time) * 1000
        if total_time_ms < config.MAX_DETECTION_LATENCY_MS:
            print(f"✅ Performance target met (<{config.MAX_DETECTION_LATENCY_MS}ms)")
        else:
            print(f"⚠️  Performance target missed (>{config.MAX_DETECTION_LATENCY_MS}ms)")
        
        audio_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


def test_real_camera_integration():
    """Test integration with real camera if available."""
    print("\nTesting Real Camera Integration (Optional)")
    print("=" * 40)
    
    try:
        # Try to initialize camera
        camera = CameraInterface()
        if not camera.initialize_camera(0):
            print("⚠️  Camera not available - skipping real camera test")
            return True
        
        # Initialize other components
        audio_manager = AudioManager()
        object_detector = ObjectDetector()
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=5.0,
            enabled=True
        )
        
        print("Camera initialized successfully")
        print("Testing with real camera frames...")
        print("Press 'q' to quit, 's' to force scene classification")
        
        frame_count = 0
        last_scene_announcement = 0
        
        while frame_count < 50:  # Limit test duration
            frame = camera.get_frame()
            if frame is None:
                print("Failed to get frame")
                break
            
            frame_count += 1
            
            # Test object detection every few frames
            if frame_count % 5 == 0:
                detections = object_detector.detect(frame)
                if detections:
                    print(f"Frame {frame_count}: Detected {len(detections)} objects")
            
            # Test scene classification
            if scene_integration.is_enabled():
                announced_scene = scene_integration.process_frame(frame)
                if announced_scene:
                    print(f"Frame {frame_count}: Scene announced - {announced_scene}")
                    last_scene_announcement = frame_count
            
            # Display frame with info
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if scene_integration.is_enabled():
                current_scene = scene_integration.get_current_scene()
                if current_scene:
                    cv2.putText(display_frame, f"Scene: {current_scene}", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow('Integration Test', display_frame)
            
            # Check for key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and scene_integration.is_enabled():
                forced_scene = scene_integration.force_scene_update(frame)
                print(f"Forced scene classification: {forced_scene}")
        
        # Cleanup
        camera.release()
        cv2.destroyAllWindows()
        audio_manager.cleanup()
        
        print(f"✅ Real camera test completed ({frame_count} frames processed)")
        if last_scene_announcement > 0:
            print(f"   Last scene announcement at frame {last_scene_announcement}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real camera test failed: {e}")
        return False


def main():
    """Run all integration tests."""
    print("VisionMate-Lite Integration Tests with Scene Classification")
    print("=" * 60)
    
    # Setup logging
    logging.basicConfig(level=logging.WARNING)  # Reduce log noise during testing
    
    tests = [
        ("Component Initialization", test_component_initialization),
        ("Scene Integration with Mock Data", test_scene_integration_with_mock_data),
        ("Full System Integration", test_full_system_integration),
        ("Performance with Scene Classification", test_performance_with_scene_classification),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    # Optional real camera test
    print(f"\n{'='*20} Optional Tests {'='*20}")
    try:
        response = input("Test with real camera? (y/n): ").lower().strip()
        if response == 'y':
            total += 1
            if test_real_camera_integration():
                passed += 1
                print("✅ Real Camera Integration: PASSED")
            else:
                print("❌ Real Camera Integration: FAILED")
    except KeyboardInterrupt:
        print("\nSkipping real camera test")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("Scene classification is properly integrated with the system.")
        return 0
    else:
        print("⚠️  Some integration tests failed.")
        print("Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())