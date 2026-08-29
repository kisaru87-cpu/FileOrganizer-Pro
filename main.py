#!/usr/bin/env python3
"""
FileOrganizer-Pro - Main Entry Point
A cross-platform file organization and corruption detection tool

This script can be run directly or compiled to .exe using PyInstaller
"""

import sys
import os

# Ensure src directory is in path
if getattr(sys, 'frozen', False):
    # Running as compiled .exe
    base_dir = sys._MEIPASS
else:
    # Running as Python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

from ui.main_window import main

if __name__ == '__main__':
    main()
