#!/usr/bin/env python3
"""
Simple launcher for Audio Transcriber
Makes it super easy to start the GUI with just a double-click
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import main
    main()
except Exception as e:
    print(f"Error starting Audio Transcriber: {e}")
    print("Please contact Matt if you need help!")
    input("Press Enter to exit...")