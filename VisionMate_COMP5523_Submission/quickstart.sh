#!/bin/bash
echo 'VisionMate-Lite Quick Start'
echo '============================'
echo ''
echo 'Installing dependencies...'
pip install -r requirements.txt
echo ''
echo 'Validating system...'
python scripts/validate_system.py
echo ''
echo 'Starting VisionMate-Lite...'
python main.py
