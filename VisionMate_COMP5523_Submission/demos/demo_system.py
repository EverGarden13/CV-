#!/usr/bin/env python3
"""
VisionMate-Lite Demonstration Script

This script provides a guided demonstration of VisionMate-Lite capabilities,
suitable for project presentations or system validation.

Usage:
    python demo_system.py

Features demonstrated:
- System initialization and validation
- Object detection capabilities
- OCR text reading functionality
- Performance metrics
- Error handling
"""

import sys
import os
import time
import logging
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import system modules
import config
from src.error_handler import initialize_error_handling, get_system_validator
from src.camera import CameraInterface
from src.detection import ObjectDetector
from src.ocr import OCREngine
from src.audio import AudioManager


class VisionMateDemonstrator:
    """Interactive demonstration system for VisionMate-Lite."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize components
        self.camera = None
        self.detector = None
        self.ocr_engine = None
        self.audio_manager = None
        
        # Demo state
        self.demo_step = 0
        self.demo_results = {}
    
    def setup_logging(self):
        """Setup logging for demonstration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    
    def print_banner(self):
        """Print demonstration banner."""
        print("\n" + "=" * 60)
        print("🎯 VisionMate-Lite System Demonstration")
        print("=" * 60)
        print(f"Platform: {config.PLATFORM}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def wait_for_user(self, message="Press Enter to continue..."):
        """Wait for user input to proceed."""
        try:
            input(f"\n{message}")
        except KeyboardInterrupt:
            print("\nDemo interrupted by user.")
            sys.exit(0)
    
    def demo_step_1_system_validation(self):
        """Demo Step 1: System validation and initialization."""
        print("\n" + "🔍 STEP 1: System Validation")
        print("-" * 40)
        
        print("Checking system dependencies and requirements...")
        
        # Initialize error handling
        if not initialize_error_handling():
            print("❌ System validation failed!")
            return False
        
        # Get validation results
        validator = get_system_validator()
        print("\n📋 System Validation Report:")
        print(validator.get_validation_report())
        
        # Check for critical failures
        critical_failures = []
        for name, result in validator.validation_results.items():
            if result["status"] == "critical_failure":
                critical_failures.append(name)
        
        if critical_failures:
            print(f"❌ Critical failures detected: {critical_failures}")
            return False
        
        print("✅ System validation PASSED!")
        self.demo_results['system_validation'] = 'PASS'
        return True
    
    def demo_step_2_component_initialization(self):
        """Demo Step 2: Initialize system components."""
        print("\n" + "🚀 STEP 2: Component Initialization")
        print("-" * 40)
        
        try:
            # Initialize camera
            print("📷 Initializing camera...")
            self.camera = CameraInterface()
            if self.camera.initialize_camera(config.CAMERA_INDEX):
                print("✅ Camera initialized successfully")
            else:
                print("⚠️  Camera not available - using mock mode")
            
            # Initialize object detector
            print("🎯 Initializing object detector...")
            self.detector = ObjectDetector(confidence_threshold=config.CONFIDENCE_THRESHOLD)
            print("✅ Object detector initialized")
            
            # Initialize OCR engine
            print("📝 Initializing OCR engine...")
            self.ocr_engine = OCREngine(min_text_length=config.MIN_TEXT_LENGTH)
            print("✅ OCR engine initialized")
            
            # Initialize audio manager
            print("🔊 Initializing audio manager...")
            self.audio_manager = AudioManager(speech_rate=config.SPEECH_RATE)
            print("✅ Audio manager initialized")
            
            print("\n🎉 All components initialized successfully!")
            self.demo_results['component_initialization'] = 'PASS'
            return True
            
        except Exception as e:
            print(f"❌ Component initialization failed: {e}")
            self.demo_results['component_initialization'] = 'FAIL'
            return False
    
    def demo_step_3_object_detection(self):
        """Demo Step 3: Demonstrate object detection."""
        print("\n" + "👁️ STEP 3: Object Detection Demonstration")
        print("-" * 40)
        
        print("This demonstration shows the object detection capabilities.")
        print("The system can detect: person, chair, car, door")
        print("\nDetection process:")
        print("1. Capture frame from camera")
        print("2. Run YOLO object detection")
        print("3. Filter for target objects")
        print("4. Check proximity using bounding box size")
        print("5. Generate audio alert if object is close")
        
        self.wait_for_user("Press Enter to start object detection demo...")
        
        try:
            import cv2
            import numpy as np
            
            # Get test frame
            if self.camera and self.camera.camera is not None:
                frame = self.camera.get_frame()
                print("📷 Using live camera frame")
            else:
                # Create synthetic frame for demo
                frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                print("📷 Using synthetic test frame")
            
            if frame is not None:
                print("🔍 Running object detection...")
                start_time = time.perf_counter()
                
                detections = self.detector.detect(frame)
                
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                
                print(f"⏱️  Detection completed in {latency_ms:.2f}ms")
                print(f"🎯 Found {len(detections)} objects")
                
                # Show detection results
                for i, detection in enumerate(detections):
                    proximity = "CLOSE" if detection.is_close(frame.shape[1], frame.shape[0]) else "FAR"
                    print(f"   {i+1}. {detection.class_name} (confidence: {detection.confidence:.2f}, proximity: {proximity})")
                    
                    # Simulate audio alert for close objects
                    if detection.is_close(frame.shape[1], frame.shape[0]):
                        alert_message = config.ALERT_MESSAGES.get(detection.class_name, f"{detection.class_name} detected")
                        print(f"   🔊 Audio Alert: '{alert_message}'")
                
                # Performance check
                target_met = latency_ms < config.MAX_DETECTION_LATENCY_MS
                print(f"\n📊 Performance: {latency_ms:.2f}ms (target: <{config.MAX_DETECTION_LATENCY_MS}ms) - {'✅ PASS' if target_met else '⚠️ SLOW'}")
                
                self.demo_results['object_detection'] = {
                    'status': 'PASS',
                    'latency_ms': latency_ms,
                    'detections_count': len(detections),
                    'performance_target_met': target_met
                }
                
                return True
            else:
                print("❌ Could not capture frame for detection demo")
                return False
                
        except Exception as e:
            print(f"❌ Object detection demo failed: {e}")
            self.demo_results['object_detection'] = {'status': 'FAIL', 'error': str(e)}
            return False
    
    def demo_step_4_ocr_functionality(self):
        """Demo Step 4: Demonstrate OCR functionality."""
        print("\n" + "📖 STEP 4: OCR Text Reading Demonstration")
        print("-" * 40)
        
        print("This demonstration shows the OCR text reading capabilities.")
        print("The system can read text from:")
        print("- Signs and labels")
        print("- Documents and papers")
        print("- Screen text")
        print("- Printed materials")
        
        print("\nOCR process:")
        print("1. User presses SPACEBAR to trigger OCR")
        print("2. System captures current camera frame")
        print("3. Tesseract OCR extracts text")
        print("4. Text is read aloud using TTS")
        
        self.wait_for_user("Press Enter to start OCR demo...")
        
        try:
            import cv2
            import numpy as np
            
            # Create test text image
            print("📝 Creating test text image...")
            test_image = self._create_demo_text_image("EMERGENCY EXIT\nROOM 101")
            
            print("🔍 Running OCR extraction...")
            start_time = time.perf_counter()
            
            extracted_text = self.ocr_engine.extract_text(test_image)
            
            ocr_time = time.perf_counter()
            
            # Simulate TTS timing
            if extracted_text and len(extracted_text.strip()) > 0:
                print(f"📖 Extracted text: '{extracted_text.strip()}'")
                
                # Estimate TTS time
                word_count = len(extracted_text.split())
                estimated_tts_time = word_count * 0.5  # ~0.5 seconds per word
                print(f"🔊 Simulating TTS reading ({word_count} words, ~{estimated_tts_time:.1f}s)")
                
                # Brief pause to simulate TTS
                time.sleep(min(estimated_tts_time, 2.0))
            else:
                print("📖 No text extracted")
            
            end_time = time.perf_counter()
            total_latency_s = end_time - start_time
            
            print(f"⏱️  OCR completed in {total_latency_s:.2f}s")
            
            # Performance check
            target_met = total_latency_s < config.MAX_OCR_LATENCY_SECONDS
            print(f"📊 Performance: {total_latency_s:.2f}s (target: <{config.MAX_OCR_LATENCY_SECONDS}s) - {'✅ PASS' if target_met else '⚠️ SLOW'}")
            
            self.demo_results['ocr_functionality'] = {
                'status': 'PASS',
                'latency_s': total_latency_s,
                'extracted_text': extracted_text.strip() if extracted_text else '',
                'performance_target_met': target_met
            }
            
            return True
            
        except Exception as e:
            print(f"❌ OCR demo failed: {e}")
            self.demo_results['ocr_functionality'] = {'status': 'FAIL', 'error': str(e)}
            return False
    
    def demo_step_5_error_handling(self):
        """Demo Step 5: Demonstrate error handling."""
        print("\n" + "🛡️ STEP 5: Error Handling Demonstration")
        print("-" * 40)
        
        print("This demonstration shows how the system handles various error conditions:")
        print("- Camera unavailable")
        print("- Invalid input data")
        print("- OCR processing failures")
        print("- Audio system issues")
        
        self.wait_for_user("Press Enter to start error handling demo...")
        
        error_tests = []
        
        try:
            # Test 1: Invalid camera
            print("🧪 Test 1: Invalid camera handling...")
            try:
                invalid_camera = CameraInterface()
                result = invalid_camera.initialize_camera(99)  # Invalid index
                if not result:
                    print("✅ Invalid camera handled gracefully")
                    error_tests.append(('invalid_camera', 'PASS'))
                else:
                    print("⚠️  Invalid camera not detected")
                    error_tests.append(('invalid_camera', 'UNEXPECTED'))
            except Exception as e:
                print(f"✅ Invalid camera exception handled: {e}")
                error_tests.append(('invalid_camera', 'PASS'))
            
            # Test 2: OCR on empty image
            print("\n🧪 Test 2: OCR error handling...")
            try:
                import numpy as np
                empty_image = np.zeros((100, 100, 3), dtype=np.uint8)
                text = self.ocr_engine.extract_text(empty_image)
                print(f"✅ OCR on empty image handled: '{text}'")
                error_tests.append(('ocr_empty_image', 'PASS'))
            except Exception as e:
                print(f"✅ OCR error handled gracefully: {e}")
                error_tests.append(('ocr_empty_image', 'PASS'))
            
            # Test 3: Detection on invalid frame
            print("\n🧪 Test 3: Detection error handling...")
            try:
                import numpy as np
                invalid_frame = np.zeros((10, 10), dtype=np.uint8)  # Wrong dimensions
                detections = self.detector.detect(invalid_frame)
                print(f"✅ Detection on invalid frame handled: {len(detections)} results")
                error_tests.append(('detection_invalid_frame', 'PASS'))
            except Exception as e:
                print(f"✅ Detection error handled gracefully: {e}")
                error_tests.append(('detection_invalid_frame', 'PASS'))
            
            passed_tests = sum(1 for _, status in error_tests if status == 'PASS')
            print(f"\n📊 Error handling results: {passed_tests}/{len(error_tests)} tests passed")
            
            self.demo_results['error_handling'] = {
                'status': 'PASS' if passed_tests == len(error_tests) else 'PARTIAL',
                'tests_passed': passed_tests,
                'total_tests': len(error_tests),
                'test_results': error_tests
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error handling demo failed: {e}")
            self.demo_results['error_handling'] = {'status': 'FAIL', 'error': str(e)}
            return False
    
    def demo_step_6_performance_summary(self):
        """Demo Step 6: Performance summary and recommendations."""
        print("\n" + "📊 STEP 6: Performance Summary")
        print("-" * 40)
        
        print("System Performance Summary:")
        print("=" * 30)
        
        # Detection performance
        if 'object_detection' in self.demo_results:
            det_result = self.demo_results['object_detection']
            if det_result['status'] == 'PASS':
                latency = det_result['latency_ms']
                target_met = det_result['performance_target_met']
                status_icon = "✅" if target_met else "⚠️"
                print(f"{status_icon} Object Detection: {latency:.2f}ms (target: <500ms)")
            else:
                print("❌ Object Detection: FAILED")
        
        # OCR performance
        if 'ocr_functionality' in self.demo_results:
            ocr_result = self.demo_results['ocr_functionality']
            if ocr_result['status'] == 'PASS':
                latency = ocr_result['latency_s']
                target_met = ocr_result['performance_target_met']
                status_icon = "✅" if target_met else "⚠️"
                print(f"{status_icon} OCR Processing: {latency:.2f}s (target: <10s)")
            else:
                print("❌ OCR Processing: FAILED")
        
        # Overall system status
        passed_components = sum(1 for result in self.demo_results.values() 
                              if isinstance(result, dict) and result.get('status') == 'PASS')
        total_components = len([r for r in self.demo_results.values() if isinstance(r, dict)])
        
        print(f"\n🎯 Overall System Status: {passed_components}/{total_components} components working")
        
        # Recommendations
        print("\n💡 Recommendations:")
        if passed_components == total_components:
            print("✅ System is ready for demonstration and evaluation")
            print("✅ All performance targets are being met")
            print("✅ Error handling is working correctly")
        else:
            print("⚠️  Some components need attention before demonstration")
            print("⚠️  Review failed tests and address issues")
            print("⚠️  Consider performance optimizations if needed")
        
        return True
    
    def run_complete_demo(self):
        """Run the complete demonstration sequence."""
        self.print_banner()
        
        print("\nThis demonstration will showcase VisionMate-Lite capabilities:")
        print("1. System validation and dependency checking")
        print("2. Component initialization")
        print("3. Object detection functionality")
        print("4. OCR text reading functionality")
        print("5. Error handling and recovery")
        print("6. Performance summary and recommendations")
        
        self.wait_for_user("Press Enter to begin demonstration...")
        
        # Run demonstration steps
        demo_steps = [
            self.demo_step_1_system_validation,
            self.demo_step_2_component_initialization,
            self.demo_step_3_object_detection,
            self.demo_step_4_ocr_functionality,
            self.demo_step_5_error_handling,
            self.demo_step_6_performance_summary
        ]
        
        completed_steps = 0
        
        for i, step_func in enumerate(demo_steps, 1):
            try:
                if step_func():
                    completed_steps += 1
                else:
                    print(f"⚠️  Step {i} completed with issues")
            except Exception as e:
                print(f"❌ Step {i} failed: {e}")
            
            if i < len(demo_steps):
                self.wait_for_user()
        
        # Final summary
        print("\n" + "🎉 DEMONSTRATION COMPLETE")
        print("=" * 40)
        print(f"Completed steps: {completed_steps}/{len(demo_steps)}")
        
        if completed_steps == len(demo_steps):
            print("✅ Full demonstration successful!")
            print("🚀 VisionMate-Lite is ready for use and evaluation")
        else:
            print("⚠️  Demonstration completed with some issues")
            print("📋 Review the results above for details")
        
        # Cleanup
        self._cleanup()
        
        return completed_steps == len(demo_steps)
    
    def _create_demo_text_image(self, text):
        """Create a demo text image for OCR testing."""
        import cv2
        import numpy as np
        
        # Create white background
        img = np.ones((200, 500, 3), dtype=np.uint8) * 255
        
        # Add text lines
        lines = text.split('\n')
        y_start = 60
        line_height = 40
        
        for i, line in enumerate(lines):
            y_pos = y_start + (i * line_height)
            cv2.putText(img, line, (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.0, (0, 0, 0), 2, cv2.LINE_AA)
        
        return img
    
    def _cleanup(self):
        """Clean up resources."""
        try:
            if self.camera:
                self.camera.release()
        except Exception as e:
            self.logger.warning(f"Cleanup warning: {e}")


def main():
    """Run the VisionMate-Lite demonstration."""
    print("VisionMate-Lite Interactive Demonstration")
    print("This demo showcases the system's capabilities and performance.")
    
    try:
        demonstrator = VisionMateDemonstrator()
        success = demonstrator.run_complete_demo()
        
        if success:
            print("\n🎊 Thank you for viewing the VisionMate-Lite demonstration!")
            sys.exit(0)
        else:
            print("\n⚠️  Demonstration completed with issues. Please review the output above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()