#!/usr/bin/env python3
"""
System validation script for VisionMate-Lite.
Run this script to check if all dependencies and requirements are met.
"""

import sys
import os
import logging

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.error_handler import initialize_error_handling, get_system_validator, get_privacy_manager


def main():
    """Run comprehensive system validation."""
    print("VisionMate-Lite System Validation")
    print("=" * 40)
    
    # Set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    try:
        # Initialize error handling system
        print("Initializing error handling system...")
        if not initialize_error_handling():
            print("❌ System validation FAILED")
            return False
        
        print("✅ Error handling system initialized")
        
        # Get validation results
        validator = get_system_validator()
        privacy_manager = get_privacy_manager()
        
        # Print detailed validation report
        print("\n" + validator.get_validation_report())
        
        # Print privacy status
        print("\nPrivacy Settings:")
        print("-" * 20)
        privacy_status = privacy_manager.get_privacy_status()
        for key, value in privacy_status.items():
            print(f"  {key}: {value}")
        
        # Check if all critical validations passed
        all_passed = True
        for name, result in validator.validation_results.items():
            if result["status"] == "critical_failure":
                all_passed = False
                break
        
        print("\n" + "=" * 40)
        if all_passed:
            print("✅ System validation PASSED - VisionMate-Lite is ready to run")
            print("\nTo start the application, run:")
            print("  python main.py")
        else:
            print("❌ System validation FAILED - Please fix the issues above")
            print("\nCommon solutions:")
            print("  - Install missing dependencies: pip install -r requirements.txt")
            print("  - Install Tesseract OCR:")
            print("    Windows: https://github.com/UB-Mannheim/tesseract/wiki")
            print("    macOS: brew install tesseract")
            print("  - Check camera permissions and availability")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)