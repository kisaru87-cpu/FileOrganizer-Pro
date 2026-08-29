#!/usr/bin/env python3
"""
FileOrganizer-Pro - Main Entry Point
A cross-platform file organization and corruption detection tool
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import main

if __name__ == '__main__':
    main()
