#!/usr/bin/env python3
"""
Build script for creating FileOrganizer-Pro .exe executable
Requirements: PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """Build FileOrganizer-Pro .exe using PyInstaller"""
    
    print("="*60)
    print("FileOrganizer-Pro Executable Builder")
    print("="*60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"\n✓ PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("\n✗ PyInstaller not found!")
        print("Install it with: pip install PyInstaller")
        return False
    
    # Check if spec file exists
    spec_file = Path('FileOrganizer-Pro.spec')
    if not spec_file.exists():
        print(f"\n✗ Spec file not found: {spec_file}")
        return False
    
    print(f"\n✓ Found spec file: {spec_file}")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for directory in ['build', 'dist', '__pycache__']:
        if os.path.exists(directory):
            print(f"  Removing {directory}/")
            shutil.rmtree(directory)
    
    # Run PyInstaller
    print("\nBuilding executable...")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', str(spec_file), '--windowed'],
            check=True
        )
        print("-" * 60)
        print("\n✓ Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print(f"\n✗ Build failed with error: {e}")
        return False
    
    # Verify output
    exe_path = Path('dist/FileOrganizer-Pro/FileOrganizer-Pro.exe')
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024*1024)  # Size in MB
        print(f"\n📦 Executable created: {exe_path}")
        print(f"   Size: {exe_size:.2f} MB")
        print(f"\n✓ You can now run: {exe_path}")
        return True
    else:
        print(f"\n✗ Executable not found at expected location: {exe_path}")
        return False

def create_installer():
    """Create NSIS installer (optional)"""
    print("\n" + "="*60)
    print("Creating Windows Installer...")
    print("="*60)
    
    print("\nNote: To create an installer, install NSIS:")
    print("  Download from: https://nsis.sourceforge.io/")
    print("  Then run: makensis installer.nsi")

if __name__ == '__main__':
    success = build_exe()
    
    if success:
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print("\nNext steps:")
        print("1. Test the executable: dist/FileOrganizer-Pro/FileOrganizer-Pro.exe")
        print("2. Distribute the entire 'dist/FileOrganizer-Pro' folder")
        print("3. Users can run FileOrganizer-Pro.exe without installing Python")
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("BUILD FAILED!")
        print("="*60)
        sys.exit(1)
