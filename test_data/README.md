# Test Data Organization

This directory contains test datasets for evaluating VisionMate-Lite performance.

## Directory Structure

```
test_data/
├── detection/           # Object detection test images
│   ├── person/         # Images containing people
│   ├── chair/          # Images containing chairs
│   ├── car/            # Images containing cars
│   ├── door/           # Images containing doors
│   └── mixed/          # Images with multiple objects
└── ocr/                # OCR test images
    ├── signs/          # Street signs, building signs
    ├── labels/         # Product labels, name tags
    ├── screens/        # Computer screens, phone displays
    └── documents/      # Printed documents, books
```

## Data Collection Protocol

### Ethics and Privacy Guidelines

1. **Consent**: Only photograph people who have given explicit consent
2. **Public Spaces**: Focus on public areas where photography is permitted
3. **No Personal Information**: Avoid capturing personal documents, private information
4. **Anonymization**: Blur faces in images if not essential for testing
5. **Local Use Only**: All images are for local testing only, never shared publicly

### Detection Dataset (Target: 100-200 images)

#### Person Detection (25-50 images)
- Various distances: close (large bounding box), medium, far
- Different lighting: indoor, outdoor, bright, dim
- Different poses: standing, sitting, walking
- Multiple people in frame for testing prioritization

#### Chair Detection (25-50 images)
- Office chairs, dining chairs, armchairs
- Different angles and orientations
- Various lighting conditions
- Chairs as obstacles in pathways

#### Car Detection (25-50 images)
- Parked cars from pedestrian perspective
- Different car types: sedan, SUV, truck
- Various distances and angles
- Cars as navigation obstacles

#### Door Detection (25-50 images)
- Building entrances, room doors
- Open and closed doors
- Different door types: glass, wood, metal
- Various lighting conditions

#### Mixed Scenes (25-50 images)
- Multiple object types in single frame
- Test prioritization algorithms
- Real-world navigation scenarios

### OCR Dataset (Target: 50-100 images)

#### Signs (15-25 images)
- Street signs, building directories
- Various fonts and sizes
- Different lighting conditions
- Both high and low contrast

#### Labels (15-25 images)
- Product labels, name tags
- Small text testing
- Various backgrounds
- Different text orientations

#### Screens (15-25 images)
- Computer monitors, phone screens
- Digital displays, LED signs
- Test backlit text recognition
- Various screen brightness levels

#### Documents (15-25 images)
- Printed pages, books
- Handwritten text (if applicable)
- Various paper types and conditions
- Different text sizes and fonts

## Image Requirements

### Technical Specifications
- **Format**: JPG or PNG
- **Resolution**: Minimum 640x480, recommended 1280x720
- **Quality**: Good focus, minimal motion blur
- **Lighting**: Variety of conditions to test robustness

### Naming Convention
```
{category}_{condition}_{number}.jpg

Examples:
person_indoor_bright_001.jpg
chair_outdoor_dim_002.jpg
car_parking_lot_003.jpg
door_office_building_004.jpg
sign_street_sunny_001.jpg
label_product_close_002.jpg
```

### Metadata Documentation
For each image, document:
- Location type (indoor/outdoor)
- Lighting condition (bright/dim/mixed)
- Distance to main object (close/medium/far)
- Any special conditions or challenges

## Data Collection Checklist

### Detection Images
- [ ] Person images: various distances and lighting
- [ ] Chair images: different types and orientations  
- [ ] Car images: different vehicles and angles
- [ ] Door images: various door types and states
- [ ] Mixed scenes: multiple objects for prioritization testing

### OCR Images
- [ ] Sign images: various fonts and lighting
- [ ] Label images: small text and different backgrounds
- [ ] Screen images: digital displays and monitors
- [ ] Document images: printed text in various conditions

### Documentation
- [ ] Image metadata recorded
- [ ] Ethics compliance verified
- [ ] Privacy considerations addressed
- [ ] Data collection protocol followed

## Optional: Public Dataset Samples

If needed for comparison, small samples from public datasets:

### COCO Dataset
- Download 10-20 images containing target classes
- Use for baseline comparison only
- Cite properly in final report

### ICDAR Dataset  
- Download 10-20 text images for OCR comparison
- Use for benchmarking OCR accuracy
- Cite properly in final report

## Usage in Evaluation

This test data will be used for:
1. **Performance measurement**: Timing detection and OCR operations
2. **Accuracy evaluation**: Manual verification of detection results
3. **Robustness testing**: Various lighting and distance conditions
4. **System validation**: End-to-end functionality testing

## Privacy and Cleanup

- All personal images can be deleted after project completion
- No images will be included in final project submission
- Only aggregate metrics and anonymized examples in report
- Clear documentation of data handling in ethics section