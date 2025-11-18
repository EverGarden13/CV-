#!/usr/bin/env python3
"""
Demo script for VisionMate-Lite Scene Classification Integration

This script demonstrates the scene classification feature integrated with
the main application components, without requiring OCR dependencies.
"""

import sys
import os
import time
import cv2
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration and components
import config
from src.camera import CameraInterface
from src.detection import ObjectDetector
from src.audio import AudioManager
from src.scene_integration import SceneIntegration


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def demo_scene_integration():
    """
    Demo the scene classification integration with real camera.
    """
    print("VisionMate-Lite Scene Classification Demo")
    print("=" * 50)
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        
        camera = CameraInterface()
        if not camera.initialize_camera(config.CAMERA_INDEX):
            print("❌ Failed to initialize camera")
            return False
        
        audio_manager = AudioManager(speech_rate=config.SPEECH_RATE)
        object_detector = ObjectDetector(confidence_threshold=config.CONFIDENCE_THRESHOLD)
        
        # Initialize scene integration
        scene_integration = SceneIntegration(
            audio_manager,
            update_interval=config.SCENE_UPDATE_INTERVAL,
            confidence_threshold=config.SCENE_CONFIDENCE_THRESHOLD,
            enabled=config.ENABLE_SCENE_CLASSIFICATION
        )
        
        print(f"✅ Camera: Initialized")
        print(f"✅ Audio: Initialized")
        print(f"✅ Object Detection: Initialized")
        print(f"✅ Scene Classification: {'Enabled' if scene_integration.is_enabled() else 'Disabled'}")
        
        if not scene_integration.is_enabled():
            print("⚠️  Scene classification is disabled - demo will show other features only")
        
        print("\nDemo Controls:")
        print("- Press 'q' to quit")
        print("- Press 's' to force scene classification")
        print("- Press 'a' to test audio announcement")
        print("- Scene classification happens automatically every 15 seconds")
        
        # Main demo loop
        frame_count = 0
        last_alert_time = {}
        
        cv2.namedWindow('VisionMate Scene Demo', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('VisionMate Scene Demo', 800, 600)
        
        logger.info("Starting demo loop...")
        
        while True:
            # Capture frame
            frame = camera.get_frame()
            if frame is None:
                logger.warning("Failed to capture frame")
                time.sleep(0.1)
                continue
            
            frame_count += 1
            
            # Process object detection (every 3rd frame)
            detections = []
            if frame_count % config.FRAME_SKIP == 0:
                try:
                    detections = object_detector.detect(frame)
                    
                    # Process proximity alerts
                    current_time = time.time()
                    for detection in detections:
                        if detection.is_close(frame.shape[1], frame.shape[0]):
                            last_alert = last_alert_time.get(detection.class_name, 0)
                            if current_time - last_alert > config.ALERT_COOLDOWN_SECONDS:
                                if not audio_manager.is_busy():
                                    audio_manager.speak_alert(detection.class_name)
                                    last_alert_time[detection.class_name] = current_time
                                    logger.info(f"Alert: {detection.class_name} detected nearby")
                except Exception as e:
                    logger.error(f"Object detection error: {e}")
            
            # Process scene classification
            announced_scene = None
            if scene_integration.is_enabled() and frame_count % (config.FRAME_SKIP * 5) == 0:
                try:
                    announced_scene = scene_integration.process_frame(frame)
                    if announced_scene:
                        logger.info(f"Scene announced: {announced_scene}")
                except Exception as e:
                    logger.error(f"Scene classification error: {e}")
            
            # Create display frame
            display_frame = frame.copy()
            
            # Add status information
            y_offset = 30
            cv2.putText(display_frame, "VisionMate-Lite Scene Demo", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            y_offset += 40
            
            cv2.putText(display_frame, f"Frame: {frame_count}", (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y_offset += 30
            
            # Show detected objects
            if detections:
                cv2.putText(display_frame, f"Objects: {len(detections)}", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
                y_offset += 25
                
                for detection in detections:
                    obj_text = f"  {detection.class_name} ({detection.confidence:.2f})"
                    cv2.putText(display_frame, obj_text, (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    y_offset += 20
            
            # Show current scene
            if scene_integration.is_enabled():
                current_scene = scene_integration.get_current_scene()
                if current_scene:
                    cv2.putText(display_frame, f"Scene: {current_scene}", (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                    y_offset += 30
                
                if announced_scene:
                    cv2.putText(display_frame, "SCENE ANNOUNCED!", (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    y_offset += 30
            
            # Show audio status
            if audio_manager.is_busy():
                cv2.putText(display_frame, "SPEAKING...", (10, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Draw bounding boxes for detections
            for detection in detections:
                x1, y1, x2, y2 = detection.bbox
                color = (0, 255, 0) if detection.is_close(frame.shape[1], frame.shape[0]) else (255, 0, 0)
                cv2.rectangle(display_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                
                label = f"{detection.class_name} {detection.confidence:.2f}"
                cv2.putText(display_frame, label, (int(x1), int(y1-10)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Show controls
            controls_y = display_frame.shape[0] - 60
            cv2.putText(display_frame, "Controls: Q=quit, S=force scene, A=test audio", 
                       (10, controls_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Display frame
            cv2.imshow('VisionMate Scene Demo', display_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("Quit requested")
                break
            elif key == ord('s') and scene_integration.is_enabled():
                logger.info("Forcing scene classification...")
                forced_scene = scene_integration.force_scene_update(frame)
                if forced_scene:
                    logger.info(f"Forced scene: {forced_scene}")
                    if not audio_manager.is_busy():
                        audio_manager.speak_scene(forced_scene)
                else:
                    logger.info("Scene classification failed")
            elif key == ord('a'):
                logger.info("Testing audio announcement...")
                if not audio_manager.is_busy():
                    if scene_integration.is_enabled() and scene_integration.get_current_scene():
                        audio_manager.speak_scene(scene_integration.get_current_scene())
                    else:
                        audio_manager.speak_text("Audio system is working correctly")
            
            # Small delay
            time.sleep(0.01)
        
        # Cleanup
        camera.release()
        cv2.destroyAllWindows()
        audio_manager.cleanup()
        
        logger.info("Demo completed successfully")
        return True
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        return True
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        return False


def main():
    """Main entry point for the demo."""
    print("Starting VisionMate-Lite Scene Classification Demo...")
    
    success = demo_scene_integration()
    
    if success:
        print("\n✅ Demo completed successfully!")
        print("Scene classification integration is working properly.")
        return 0
    else:
        print("\n❌ Demo failed!")
        print("Check the output above for error details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())