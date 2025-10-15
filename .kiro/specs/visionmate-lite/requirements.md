# Requirements Document

## Introduction

VisionMate-Lite is a solo-feasible, lightweight assistive vision system designed for the COMP5523 course project. The system helps visually impaired users navigate and interact with their environment using a standard laptop webcam and microphone. It provides real-time object detection alerts, on-demand OCR text reading, and optional scene labeling through audio feedback. The system operates entirely offline using CPU-friendly models, with a focus on practicality, reliability, and low-latency feedback suitable for a solo developer timeline ending December 2, 2025.

## Requirements

### Requirement 1

**User Story:** As a visually impaired user, I want to receive audio alerts about nearby objects and obstacles, so that I can navigate safely through my environment.

#### Acceptance Criteria

1. WHEN the system detects a person within proximity using bounding box size heuristics THEN the system SHALL provide an audio alert stating "Person ahead"
2. WHEN the system detects common navigation obstacles from a limited set (person, chair, door, car) THEN the system SHALL announce the object type with simple proximity indication
3. WHEN multiple objects are detected simultaneously THEN the system SHALL prioritize alerts based on bounding box size as a proximity indicator
4. WHEN the same object remains in view THEN the system SHALL avoid repetitive alerts within a 5-second window to prevent audio spam
5. IF the webcam feed is unavailable or initialization fails THEN the system SHALL provide an audio notification of the camera status

### Requirement 2

**User Story:** As a visually impaired user, I want to trigger text reading on demand, so that I can access written information in my environment.

#### Acceptance Criteria

1. WHEN the user presses a designated keyboard key THEN the system SHALL capture the current webcam frame for OCR processing
2. WHEN text is detected in the captured frame using Tesseract OCR THEN the system SHALL read the extracted text aloud using platform-appropriate text-to-speech (Windows SAPI or macOS built-in)
3. WHEN no readable text is detected in the frame THEN the system SHALL announce "No text found"
4. WHEN OCR processing exceeds 3 seconds THEN the system SHALL provide a "Processing text" audio notification
5. IF the text extraction produces garbled results due to poor image quality THEN the system SHALL suggest "Try better lighting or closer positioning"

### Requirement 3

**User Story:** As a visually impaired user, I want the system to work offline without internet connectivity, so that my privacy is protected and the system remains reliable.

#### Acceptance Criteria

1. WHEN the system starts THEN it SHALL initialize all models and components without requiring internet access
2. WHEN processing video frames THEN the system SHALL perform all detection and OCR operations locally on the device
3. WHEN audio feedback is generated THEN the system SHALL use offline text-to-speech capabilities
4. IF internet connectivity is lost THEN the system SHALL continue operating without degradation
5. WHEN the system processes images THEN it SHALL NOT transmit any visual data to external servers

### Requirement 4

**User Story:** As a visually impaired user, I want the system to respond quickly to my environment, so that I can receive timely assistance for navigation and interaction.

#### Acceptance Criteria

1. WHEN object detection is running on CPU THEN the system SHALL process frames with an average latency under 300ms using lightweight models (MobileNet-SSD or YOLO nano)
2. WHEN OCR is triggered THEN the system SHALL complete text extraction and begin audio output within 5 seconds on standard laptop hardware
3. WHEN the system starts up THEN it SHALL load models and be ready to provide assistance within 15 seconds
4. WHEN running on CPU-only hardware without GPU acceleration THEN the system SHALL maintain usable performance for real-time object detection
5. IF processing latency becomes unacceptable THEN the system SHALL reduce frame processing rate or image resolution to maintain responsiveness

### Requirement 5

**User Story:** As a visually impaired user, I want clear and concise audio feedback, so that I can quickly understand and act on the information provided.

#### Acceptance Criteria

1. WHEN providing object alerts THEN the system SHALL use clear, standardized phrases (e.g., "Person ahead", "Chair on left")
2. WHEN reading text via OCR THEN the system SHALL speak at an adjustable rate with clear pronunciation
3. WHEN multiple alerts are queued THEN the system SHALL prioritize safety-related notifications first
4. WHEN background noise might interfere THEN the system SHALL provide audio at sufficient volume levels
5. IF the user interrupts during text reading THEN the system SHALL stop speaking and be ready for new input

### Requirement 6

**User Story:** As a developer/user setting up the system, I want easy configuration and setup, so that I can customize the system for my specific needs and testing environment.

#### Acceptance Criteria

1. WHEN the system is first run THEN it SHALL create a default configuration file for customizing detection classes, audio settings, and data paths
2. WHEN configuring the system THEN users SHALL be able to adjust audio volume, speech rate, alert frequency, and model parameters via a config file
3. WHEN the system starts THEN it SHALL automatically detect and use the default webcam (index 0) without manual configuration
4. WHEN using custom test datasets for evaluation THEN the system SHALL load data paths from environment variables or config files (never hardcoded paths)
5. IF configuration files are missing or corrupted THEN the system SHALL create default configurations with reasonable values and continue operating

### Requirement 7

**User Story:** As a developer conducting course project evaluation, I want to measure the system's performance, so that I can document effectiveness for the COMP5523 project report.

#### Acceptance Criteria

1. WHEN running performance tests THEN the system SHALL log latency metrics (average and 95th percentile) for detection and OCR operations
2. WHEN evaluating detection accuracy THEN the system SHALL support testing against a small curated dataset (100-200 images) with precision/recall metrics for chosen object classes
3. WHEN testing OCR functionality THEN the system SHALL measure word accuracy (exact match rate) on a test set of photographed signs and text
4. WHEN conducting task-based evaluation THEN the system SHALL support 3-5 predefined scenarios (e.g., "warn about person approaching", "read door sign") for measuring success rates
5. IF evaluation data is collected THEN the system SHALL export metrics to files suitable for inclusion in the 8-page project report

### Requirement 8

**User Story:** As a visually impaired user, I want optional scene context information, so that I can better understand my overall environment.

#### Acceptance Criteria

1. WHEN scene classification is enabled THEN the system SHALL provide periodic environment labels (e.g., "office", "street", "corridor")
2. WHEN scene information is provided THEN it SHALL be delivered at a low frequency to avoid information overload
3. WHEN the scene changes significantly THEN the system SHALL announce the new environment type
4. IF scene classification is disabled THEN the system SHALL focus solely on object detection and OCR functionality
5. WHEN scene classification fails THEN the system SHALL continue operating other features without interruption
### Requ
irement 9

**User Story:** As a course project developer, I want to meet COMP5523 project constraints and timeline, so that I can successfully complete the solo project by December 2, 2025.

#### Acceptance Criteria

1. WHEN developing the system THEN it SHALL be implementable by a single developer within the 5-week timeline (November to December 2025)
2. WHEN using external libraries THEN the system SHALL prefer permissive licenses and document all dependencies for the project report
3. WHEN creating the system THEN it SHALL demonstrate appropriateness, soundness, and excitement criteria suitable for the course rubric
4. WHEN the system is complete THEN it SHALL be capable of live demonstration even without formal presentation
5. IF the system uses any credentials or API keys THEN they SHALL be loaded from environment variables and never committed to version control

### Requirement 10

**User Story:** As a privacy-conscious user, I want my visual data to remain secure and private, so that I can use the system without concerns about data exposure.

#### Acceptance Criteria

1. WHEN the system processes webcam frames THEN it SHALL never save raw frames to disk by default
2. WHEN debugging mode is enabled via configuration THEN the system MAY optionally save frames but SHALL clearly indicate this to the user
3. WHEN sharing system outputs for evaluation THEN any saved data SHALL be scrubbed of personally identifiable information
4. WHEN the system operates THEN it SHALL never transmit any visual data over network connections
5. IF frame logging is enabled for debugging THEN the system SHALL provide clear controls to disable logging and delete stored frames