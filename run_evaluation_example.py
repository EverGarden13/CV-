#!/usr/bin/env python3
"""
Example script demonstrating how to use the VisionMate-Lite evaluation module.

This script shows how to run individual evaluation components and the complete
evaluation suite for the COMP5523 project.

Usage:
    python3 run_evaluation_example.py

Note: This requires all dependencies to be installed (see requirements.txt)
"""

import os
import sys

def main():
    """
    Example usage of the VisionMate-Lite evaluation system.
    """
    print("VisionMate-Lite Evaluation Example")
    print("=" * 40)
    
    try:
        # Import the evaluation module
        from evaluation.evaluation import SimpleEvaluator
        
        # Initialize evaluator with test data path
        test_data_path = os.getenv('TEST_DATA_PATH', 'test_data/')
        evaluator = SimpleEvaluator(test_data_path=test_data_path)
        
        print(f"Initialized evaluator with test data path: {test_data_path}")
        print()
        
        # Example 1: Run individual metrics
        print("Example 1: Individual Metrics")
        print("-" * 30)
        
        # Measure detection latency
        print("Measuring detection latency...")
        detection_results = evaluator.measure_detection_latency(num_frames=50)
        print(f"Detection latency: {detection_results['average_ms']}ms average")
        print()
        
        # Measure OCR latency  
        print("Measuring OCR latency...")
        ocr_results = evaluator.measure_ocr_latency(num_samples=10)
        print(f"OCR latency: {ocr_results['average_s']}s average")
        print()
        
        # Calculate precision/recall
        print("Calculating precision/recall...")
        accuracy_results = evaluator.calculate_precision_recall()
        for class_name, metrics in accuracy_results.items():
            print(f"{class_name}: P={metrics['precision']:.3f}, R={metrics['recall']:.3f}, F1={metrics['f1_score']:.3f}")
        print()
        
        # Example 2: Generate manual testing scenarios
        print("Example 2: Manual Testing Scenarios")
        print("-" * 35)
        
        scenarios = evaluator.run_manual_testing_scenarios()
        print(f"Generated {len(scenarios)} testing scenarios")
        print("Scenarios saved to evaluation_results/manual_testing_scenarios.md")
        print()
        
        # Example 3: Complete evaluation suite
        print("Example 3: Complete Evaluation Suite")
        print("-" * 36)
        
        print("Running complete evaluation (this may take a few minutes)...")
        complete_results = evaluator.run_complete_evaluation()
        
        print("Complete evaluation finished!")
        print("Results saved to evaluation_results/ directory")
        print()
        
        # Example 4: Performance validation
        print("Example 4: Performance Target Validation")
        print("-" * 39)
        
        # Check if performance targets are met
        detection_target = 500  # ms
        ocr_target = 10  # seconds
        
        detection_pass = complete_results['detection_latency']['average_ms'] < detection_target
        ocr_pass = complete_results['ocr_latency']['average_s'] < ocr_target
        
        print(f"Detection latency target (<{detection_target}ms): {'✓ PASS' if detection_pass else '✗ FAIL'}")
        print(f"OCR processing target (<{ocr_target}s): {'✓ PASS' if ocr_pass else '✗ FAIL'}")
        print()
        
        # Summary
        print("Evaluation Summary")
        print("-" * 18)
        print("Files generated in evaluation_results/:")
        print("- complete_evaluation_results.json (detailed metrics)")
        print("- evaluation_summary.md (human-readable report)")
        print("- manual_testing_scenarios.md (testing procedures)")
        print("- manual_testing_scenarios.json (structured data)")
        print()
        print("These files are ready for inclusion in your COMP5523 project report!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("This likely means some dependencies are missing.")
        print("Please install the required packages:")
        print("  pip install -r requirements.txt")
        print()
        print("Required packages:")
        print("- ultralytics (for YOLO object detection)")
        print("- opencv-python (for image processing)")
        print("- pytesseract (for OCR)")
        print("- pyttsx3 (for text-to-speech)")
        
    except Exception as e:
        print(f"❌ Error running evaluation: {e}")
        print()
        print("This might be due to:")
        print("- Missing test data in test_data/ directory")
        print("- Camera access issues")
        print("- Missing system dependencies (e.g., Tesseract)")
        print()
        print("The evaluation module is designed to work with synthetic data")
        print("when real test data is not available.")

if __name__ == "__main__":
    main()