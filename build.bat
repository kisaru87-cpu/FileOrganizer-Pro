#!/bin/bash
# Build script for creating FileOrganizer-Pro .exe on Windows
# This script requires PyInstaller to be installed

echo "============================="
echo "FileOrganizer-Pro Build Script"
echo "============================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version

echo ""
echo "Installing/Updating PyInstaller..."
pip install --upgrade PyInstaller

echo ""
echo "Building executable..."
python build.py

echo ""
echo "Build process complete!"
