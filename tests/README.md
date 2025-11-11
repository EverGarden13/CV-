# VisionMate-Lite Test Suite

This directory contains all test files for the VisionMate-Lite project.

## Test Organization

### Integration Tests
- `test_basic_integration.py` - Basic integration tests without external dependencies
- `test_system_integration.py` - Full system integration tests
- `test_integration_with_scene.py` - Scene classification integration tests

### Component Tests
- `test_scene_classification.py` - Scene classifier tests
- `test_keyboard_integration.py` - Keyboard handler tests
- `test_keyboard_simple.py` - Simple keyboard tests
- `test_ocr_integration_mock.py` - OCR integration tests with mocks
- `test_task7_complete.py` - Task 7 completion tests

### Bug Fix Tests
- `test_fixes.py` - Tests for applied bug fixes and improvements

## Running Tests

### Run All Basic Integration Tests
```bash
python -m pytest tests/test_basic_integration.py -v
```

### Run System Validation
```bash
python tests/validate_system.py
```

### Run Full Integration Tests
```bash
python tests/test_system_integration.py
```

### Run Bug Fix Tests
```bash
python -m pytest tests/test_fixes.py -v
```

### Run Interactive Demo
```bash
python demos/demo_system.py
```

### Run System Validation
```bash
python scripts/validate_system.py
```

## Test Coverage

The test suite covers:
- ✅ Module imports and initialization
- ✅ Component functionality
- ✅ Integration between components
- ✅ Error handling and recovery
- ✅ Performance benchmarks
- ✅ System validation

## Adding New Tests

When adding new tests:
1. Place test files in this `tests/` directory
2. Name test files with `test_` prefix
3. Use descriptive test function names
4. Include docstrings explaining test purpose
5. Update this README with new test descriptions
