"""
Prepare VisionMate-Lite submission package for COMP5523
This script creates a clean submission directory with all necessary files
"""
import os
import shutil
from pathlib import Path

def create_submission_package():
    """Create submission package directory structure"""
    
    print("=" * 60)
    print("VisionMate-Lite Submission Package Creator")
    print("=" * 60)
    
    # Define submission directory
    submission_dir = Path("VisionMate_COMP5523_Submission")
    
    # Remove existing submission directory if it exists
    if submission_dir.exists():
        print(f"\n⚠️  Removing existing submission directory...")
        shutil.rmtree(submission_dir)
    
    # Create fresh submission directory
    print(f"\n✓ Creating submission directory: {submission_dir}")
    submission_dir.mkdir(exist_ok=True)
    
    # Define what to include
    files_to_copy = [
        "main.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "SETUP_INSTRUCTIONS.md",
        "SUBMISSION_README.md",
    ]
    
    directories_to_copy = [
        "src",
        "scripts",
        "docs",
        "evaluation",
        "demos",
    ]
    
    # Files/directories to exclude
    exclude_patterns = [
        "__pycache__",
        ".pyc",
        ".git",
        ".gitignore",
        ".vscode",
        ".kiro",
        "test_data",  # Exclude test data (too large)
        "models",     # Models will auto-download
        "tests",      # Exclude test scripts
    ]
    
    # Copy individual files
    print("\n📄 Copying core files...")
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy2(file, submission_dir / file)
            print(f"  ✓ {file}")
        else:
            print(f"  ⚠️  {file} not found, skipping")
    
    # Copy directories
    print("\n📁 Copying directories...")
    for directory in directories_to_copy:
        src_dir = Path(directory)
        if src_dir.exists():
            dest_dir = submission_dir / directory
            
            # Copy directory with exclusions
            shutil.copytree(
                src_dir,
                dest_dir,
                ignore=shutil.ignore_patterns(*exclude_patterns)
            )
            print(f"  ✓ {directory}/")
        else:
            print(f"  ⚠️  {directory}/ not found, skipping")
    
    # Create models directory with .gitkeep
    models_dir = submission_dir / "models"
    models_dir.mkdir(exist_ok=True)
    (models_dir / ".gitkeep").touch()
    (models_dir / "README.md").write_text(
        "# Models Directory\n\n"
        "YOLOv8n model will be automatically downloaded on first run.\n\n"
        "The model file (yolov8n.pt) will be downloaded from Ultralytics when you first run the application.\n"
    )
    print(f"  ✓ models/ (with auto-download instructions)")
    
    # Create a quick start script
    print("\n📝 Creating quick start script...")
    
    # Windows batch file
    quickstart_bat = submission_dir / "quickstart.bat"
    quickstart_bat.write_text(
        "@echo off\n"
        "echo VisionMate-Lite Quick Start\n"
        "echo ============================\n"
        "echo.\n"
        "echo Installing dependencies...\n"
        "pip install -r requirements.txt\n"
        "echo.\n"
        "echo Validating system...\n"
        "python scripts/validate_system.py\n"
        "echo.\n"
        "echo Starting VisionMate-Lite...\n"
        "python main.py\n"
    )
    print(f"  ✓ quickstart.bat (Windows)")
    
    # Unix shell script
    quickstart_sh = submission_dir / "quickstart.sh"
    quickstart_sh.write_text(
        "#!/bin/bash\n"
        "echo 'VisionMate-Lite Quick Start'\n"
        "echo '============================'\n"
        "echo ''\n"
        "echo 'Installing dependencies...'\n"
        "pip install -r requirements.txt\n"
        "echo ''\n"
        "echo 'Validating system...'\n"
        "python scripts/validate_system.py\n"
        "echo ''\n"
        "echo 'Starting VisionMate-Lite...'\n"
        "python main.py\n"
    )
    # Make executable
    quickstart_sh.chmod(0o755)
    print(f"  ✓ quickstart.sh (macOS/Linux)")
    
    # Create submission info file
    print("\n📋 Creating submission info...")
    submission_info = submission_dir / "SUBMISSION_INFO.txt"
    submission_info.write_text(
        "VisionMate-Lite - COMP5523 Project Submission\n"
        "=" * 60 + "\n\n"
        "Project: VisionMate-Lite - A Lightweight Assistive Vision System\n"
        "Course: COMP5523 Computer Vision and Image Processing\n"
        "Date: December 2, 2025\n"
        "Project Type: Solo Project\n\n"
        "=" * 60 + "\n"
        "QUICK START\n"
        "=" * 60 + "\n\n"
        "1. Read SETUP_INSTRUCTIONS.md for detailed setup\n"
        "2. Install dependencies: pip install -r requirements.txt\n"
        "3. Install Tesseract OCR (see SETUP_INSTRUCTIONS.md)\n"
        "4. Run validation: python scripts/validate_system.py\n"
        "5. Start application: python main.py\n\n"
        "OR use quick start scripts:\n"
        "  - Windows: quickstart.bat\n"
        "  - macOS/Linux: ./quickstart.sh\n\n"
        "=" * 60 + "\n"
        "SUBMISSION CONTENTS\n"
        "=" * 60 + "\n\n"
        "Core Files:\n"
        "  - main.py (application entry point)\n"
        "  - config.py (configuration)\n"
        "  - requirements.txt (dependencies)\n"
        "  - SETUP_INSTRUCTIONS.md (setup guide)\n"
        "  - SUBMISSION_README.md (submission overview)\n\n"
        "Source Code:\n"
        "  - src/ (all source modules)\n\n"
        "Documentation:\n"
        "  - docs/COMP5523_Project_Report_REFINED.md (8-page report)\n"
        "  - docs/VisionMate-Lite Project Presentation.pdf (slides)\n"
        "  - docs/USAGE_GUIDE.md (user guide)\n\n"
        "Evaluation:\n"
        "  - evaluation/evaluation_results.json (metrics)\n"
        "  - evaluation/ocr_evaluation_results.json (OCR results)\n"
        "  - docs/report_figures/ (generated figures)\n\n"
        "Scripts:\n"
        "  - scripts/validate_system.py (system check)\n"
        "  - scripts/simple_evaluation.py (evaluation)\n"
        "  - scripts/evaluate_ocr.py (OCR evaluation)\n"
        "  - scripts/generate_report_figures.py (figure generation)\n\n"
        "=" * 60 + "\n"
        "GRADING MATERIALS\n"
        "=" * 60 + "\n\n"
        "1. Project Report: docs/COMP5523_Project_Report_REFINED.md\n"
        "2. Presentation: docs/VisionMate-Lite Project Presentation.pdf\n"
        "3. Evaluation Results: evaluation/evaluation_results.json\n"
        "4. Source Code: src/ directory\n\n"
        "=" * 60 + "\n"
        "SYSTEM REQUIREMENTS\n"
        "=" * 60 + "\n\n"
        "- Python 3.8+\n"
        "- Webcam\n"
        "- Speakers/headphones\n"
        "- 4GB RAM minimum\n"
        "- Tesseract OCR\n"
        "- Internet (for initial setup only)\n\n"
        "=" * 60 + "\n"
        "EXPECTED PERFORMANCE\n"
        "=" * 60 + "\n\n"
        "- Detection Latency: ~428ms\n"
        "- OCR Processing: 5-8 seconds\n"
        "- System Startup: 15-20 seconds\n"
        "- Detection Accuracy: 82% precision, 75% recall\n"
        "- OCR Success Rate: 44% on standard dataset\n\n"
        "=" * 60 + "\n\n"
        "For detailed information, see SUBMISSION_README.md\n"
        "For setup help, see SETUP_INSTRUCTIONS.md\n\n"
        "Thank you for evaluating VisionMate-Lite!\n"
    )
    print(f"  ✓ SUBMISSION_INFO.txt")
    
    # Calculate directory size
    print("\n📊 Calculating package size...")
    total_size = sum(f.stat().st_size for f in submission_dir.rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)
    print(f"  Total size: {size_mb:.2f} MB")
    
    # Count files
    file_count = sum(1 for _ in submission_dir.rglob('*') if _.is_file())
    print(f"  Total files: {file_count}")
    
    # Create ZIP archive
    print("\n📦 Creating ZIP archive...")
    archive_name = "VisionMate_COMP5523_Submission"
    shutil.make_archive(archive_name, 'zip', submission_dir)
    archive_path = Path(f"{archive_name}.zip")
    archive_size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ {archive_path} ({archive_size_mb:.2f} MB)")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ SUBMISSION PACKAGE CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nDirectory: {submission_dir}/")
    print(f"Archive: {archive_path}")
    print(f"Size: {archive_size_mb:.2f} MB")
    print(f"Files: {file_count}")
    
    print("\n📋 Next Steps:")
    print("  1. Review contents in:", submission_dir)
    print("  2. Test the package on a fresh environment")
    print("  3. Submit:", archive_path)
    
    print("\n✓ Package is ready for submission!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        create_submission_package()
    except Exception as e:
        print(f"\n❌ Error creating submission package: {e}")
        import traceback
        traceback.print_exc()
