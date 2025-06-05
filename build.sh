#!/bin/bash
echo "Starting Chartastrophe build process..."
echo "Python version:"
python --version
echo "Pip version:"
pip --version
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "Build completed successfully!" 