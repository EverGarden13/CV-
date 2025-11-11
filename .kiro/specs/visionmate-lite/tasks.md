# Implementation Plan

- [x] 1. Set up project structure and cross-platform dependencies

  - Create main project directory with src/, test_data/, evaluation/, and models/ folders
  - Set up requirements.txt with cross-platform packages: ultralytics, opencv-python, pytesseract, pyttsx3
  - Create basic config.py with platform detection (Windows/macOS) and appropriate TTS settings
  - Write simple main.py entry point that imports core modules
  - Add environment variable support for TEST_DATA_PATH as specified in project concept
  - Document Tesseract installation requirements for both Windows and macOS in README
  - _Requirements: 6.1, 6.4, 6.5, 9.5_

- [x] 2. Implement camera interface and basic frame capture




  - Create camera.py module with CameraInterface class
  - Implement initialize_camera() method using OpenCV VideoCapture with camera index 0
  - Add get_frame() method that returns numpy array of current webcam frame
  - Implement graceful error handling for camera not found or access denied scenarios
  - Add release() method for proper camera resource cleanup
  - _Requirements: 1.5, 6.3_



- [x] 3. Create object detection module with YOLOv8n






  - Create detection.py module with ObjectDetector class
  - Initialize YOLOv8n model using ultralytics package in constructor
  - Implement detect() method that takes frame and returns list of Detection objects
  - Filter detections to only include target classes: person (0), chair (56), car (2), door (custom mapping)


  - Apply confidence threshold of 0.5 to reduce false positives
  - _Requirements: 1.1, 1.2, 4.1, 4.4_

- [x] 4. Add proximity detection using bounding box analysis



  - Create Detection class with class_name, confidence, and bbox attributes
  - Implement get_area() method to calculate bounding box area
  - Add is_close() method that returns True if bbox area > 15% of frame area
  - Create get_largest_detection() function to find biggest detection when multiple objects present
  - _Requirements: 1.2, 1.3_

- [x] 5. Implement cross-platform audio management




  - Create audio.py module with AudioManager class
  - Initialize pyttsx3 engine with platform-specific TTS (Windows SAPI or macOS built-in)
  - Implement speak_alert() method for object detection announcements
  - Add speak_text() method for OCR text reading
  - Include is_busy() method to check if TTS is currently speaking
  - Create simple alert message mapping for each object class
  - _Requirements: 5.1, 5.2, 5.4_
-

- [x] 6. Create OCR engine with Tesseract integration




  - Create ocr.py module with OCREngine class
  - Implement extract_text() method using pytesseract on captured frames (offline OCR as specified)
  - Add basic image preprocessing (grayscale conversion, contrast enhancement) for better accuracy
  - Include text validation to filter out results shorter than 3 characters
  - Handle OCR processing errors gracefully with user feedback suggestions for better lighting
  - Ensure Tesseract works on both Windows and macOS platforms
  - _Requirements: 2.1, 2.2, 2.3, 2.5_

- [x] 7. Integrate keyboard input for OCR triggering





  - Add keyboard input handling using opencv waitKey or keyboard library
  - Implement spacebar trigger to capture current frame for OCR processing
  - Ensure OCR processing doesn't block the main detection loop
  - Add audio feedback when OCR processing starts ("Processing text")
  - _Requirements: 2.1, 2.4_

- [x] 8. Create main application loop with real-time processing


  - Implement main application loop that continuously processes webcam frames
  - Process every 3rd frame for object detection to maintain CPU performance
  - Integrate proximity checking and audio alerts for detected objects
  - Add 5-second cooldown to prevent repetitive alerts for same objects
  - Handle keyboard input for OCR triggering within the main loop
  - _Requirements: 1.4, 4.1, 4.5_

- [x] 1.5. Collect and organize necessary datasets


  - Create small curated test dataset (100-200 images) in your environment as specified in project concept
  - Collect images containing target objects: person, chair, door, car in various lighting conditions
  - Photograph printed signs, labels, and screens for OCR testing (following project concept guidelines)
  - Organize test data with clear folder structure: test_data/detection/ and test_data/ocr/
  - Document data collection protocol for ethics/privacy notes in final report
  - Optionally sample small subset from public datasets (COCO, ICDAR) for comparison as mentioned in concept
  - _Requirements: 7.2, 7.3, 10.3_

- [x] 9. Add error handling and graceful degradation
  - Implement try-catch blocks around camera initialization and frame capture
  - Add fallback behavior when models fail to load (clear error messages)
  - Handle TTS engine failures with system notification on both Windows and macOS
  - Create graceful shutdown procedure that releases all resources
  - Add startup validation to check all dependencies are available (Tesseract, camera access)
  - Implement privacy safeguards: no raw frame logging by default, clear user control as per project concept
  - _Requirements: 1.5, 2.5, 3.4, 10.1, 10.5_

- [x] 10. Create simple evaluation and metrics collection
  - Create evaluation.py module with SimpleEvaluator class following project concept evaluation plan
  - Implement measure_detection_latency() to time object detection operations (average and 95th percentile)
  - Add measure_ocr_latency() to time OCR processing from trigger to speech
  - Create basic logging for performance metrics (average latency, detection counts)
  - Add manual testing scenarios documentation for the 3-5 simple tasks defined in project concept
  - Implement precision/recall calculation on curated test set for chosen object classes
  - _Requirements: 7.1, 7.2, 7.4, 7.5_

- [x] 11. Optional scene classification (if time permits)
  - Research lightweight scene classification models suitable for CPU
  - Implement basic scene labeling with low update frequency
  - Add scene change detection to avoid repetitive announcements
  - Integrate scene announcements into audio management system
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 12. Final integration and system testing
  - Test complete system with all components integrated on both Windows and macOS if possible
  - Verify performance targets: <500ms detection latency, <10s OCR processing as per design document
  - Conduct manual testing scenarios following project concept: person detection, object detection, OCR reading
  - Test the 3-5 simple tasks defined in project concept (e.g., "Warn about person approaching", "Read door sign")
  - Document any performance issues and create optimization recommendations for 8-page report
  - Prepare system for potential demonstration capability as specified in project concept
  - Create usage instructions and document system limitations for solo project scope
  - _Requirements: 4.1, 4.2, 4.3, 7.4, 9.4_

- [x] 13. Create COMP5523 project report (8-page A4 document)





  - Write comprehensive project report following COMP5523 specification requirements
  - Document task settings, background, and system development process
  - Include methodology section covering computer vision approaches and algorithms used
  - Present evaluation results with performance metrics, accuracy measurements, and testing outcomes
  - Add challenges faced and solutions implemented during development
  - Include system functionality overview with clear explanations of features
  - Document group member roles and contributions (adapt for solo project context)
  - Format report: 12pt Times New Roman, 1.0 line spacing, single column, 1-inch margins
  - Add figures and tables to enhance readability and understanding
  - Include APA-formatted references section (unlimited pages)
  - _Requirements: 7.1, 7.4, 7.5, 9.3, 9.4_

- [ ] 14. Create presentation slides and demonstration video
  - Create 15-minute presentation slides covering system overview and capabilities
  - Record comprehensive demonstration video showcasing VisionMate-Lite functionality
  - Include slides on task settings, challenges, and methodologies used
  - Present system features: object detection, OCR text reading, audio feedback
  - Record real-time object detection with proximity alerts in action
  - Demonstrate OCR functionality with text reading capabilities
  - Present evaluation results and performance metrics
  - Create clear narration explaining each feature and its benefits
  - Ensure video quality is high enough to show system interface and responses
  - Edit video to maintain 15-minute presentation timing with smooth transitions
  - Export final presentation slides as PDF and video in standard format (MP4)
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 4.1, 7.4, 9.4_

- [ ] 15. Create COMP5523 submission package for grader functionality
  - Create submission directory structure following COMP5523 requirements
  - Include ALL essential project files: complete source code (src/), main.py, config.py, requirements.txt
  - Package project documentation: comprehensive README.md with setup guide, final project report (8-page PDF)
  - Add presentation materials: slides (PDF) and demonstration video (MP4)
  - Create detailed SETUP_INSTRUCTIONS.md with step-by-step installation guide for graders
  - Include automatic dependency installation script (setup.py or install.bat/install.sh)
  - Document model download process with clear commands: "pip install ultralytics" and first-run auto-download
  - Add system requirements check script to verify camera access and Tesseract installation
  - Include troubleshooting guide for common issues (camera permissions, Tesseract path, TTS engine)
  - Create quick-start demo script that validates all functionality without requiring manual setup
  - Exclude unnecessary files: __pycache__ directories, .git folder, IDE configurations (.vscode, .kiro)
  - Exclude test scripts and test data folders from submission package
  - Exclude large model files but ensure automatic download on first run
  - Generate comprehensive submission_README.md with usage instructions and feature overview
  - Test complete package on fresh environment to ensure graders can run application immediately
  - Verify all core features work: object detection, OCR text reading, audio feedback, keyboard controls
  - Compress final package as ZIP file with clear naming: VisionMate_COMP5523_Submission.zip
  - Include version compatibility notes for Python 3.8+ and cross-platform support (Windows/macOS/Linux)
  - _Requirements: 9.3, 9.4, 10.4_