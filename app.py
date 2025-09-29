"""
Audio Transcriber - Unified Entry Point
Supports both GUI and CLI modes for audio/video transcription using OpenAI Whisper.

Usage:
  python app.py           # Launch GUI mode (default)
  python app.py --gui     # Launch GUI mode explicitly  
  python app.py --cli     # Launch CLI mode
  python app.py --help    # Show help
"""

import sys
import os
import argparse


def show_help():
    """Display help information."""
    help_text = """
🎵 Audio Transcriber - Made with ❤️ by Matt 🎵

This tool transcribes audio and video files using OpenAI Whisper.

USAGE:
  python app.py           Launch GUI mode (default)
  python app.py --gui     Launch GUI mode explicitly
  python app.py --cli     Launch CLI mode (command line)
  python app.py --help    Show this help message

GUI MODE (Default):
  - Friendly interface perfect for non-technical users
  - File picker for selecting audio/video files
  - Model selection with clear descriptions
  - Progress tracking and status updates
  - No command line knowledge required

CLI MODE:
  - Command line interface (original functionality)
  - Automatically finds media files in current directory
  - Interactive model selection
  - Batch processing of all found files

SUPPORTED FORMATS:
  Audio: MP3, WAV, M4A, FLAC, AAC, OGG, WMA
  Video: MP4, MKV, MOV, AVI, WEBM, WMV, MPEG, MPG

OUTPUT:
  - Timestamped transcription files
  - Saved in 'transcriptions' folder
  - Format: [00.00s - 05.23s] Transcribed text here...

Made with love for academic research and interviews! ❤️
"""
    print(help_text)


def main():
    """Main entry point - determines whether to launch GUI or CLI."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Audio Transcriber - GUI and CLI modes available",
        add_help=False  # We'll handle help ourselves
    )
    parser.add_argument('--gui', action='store_true', help='Launch GUI mode (default)')
    parser.add_argument('--cli', action='store_true', help='Launch CLI mode')
    parser.add_argument('--help', action='store_true', help='Show help information')
    
    args, unknown = parser.parse_known_args()
    
    # Handle help
    if args.help:
        show_help()
        return
    
    # Determine mode
    if args.cli:
        launch_mode = 'cli'
    else:
        # Default to GUI, but check if we can import tkinter
        try:
            import tkinter
            launch_mode = 'gui'
        except ImportError:
            print("GUI mode not available (tkinter not installed). Falling back to CLI mode.")
            launch_mode = 'cli'
    
    print(f"🎵 Audio Transcriber - Starting in {'GUI' if launch_mode == 'gui' else 'CLI'} mode...")
    print()
    
    # Launch appropriate mode
    if launch_mode == 'gui':
        try:
            from gui_app import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error importing GUI components: {e}")
            print("Falling back to CLI mode...")
            from cli_app import main as cli_main
            cli_main()
        except Exception as e:
            print(f"Error in GUI mode: {e}")
            print("Falling back to CLI mode...")
            from cli_app import main as cli_main
            cli_main()
    else:
        from cli_app import main as cli_main
        cli_main()

if __name__ == "__main__":
    # Fix for PyInstaller multiprocessing issues
    import multiprocessing
    multiprocessing.freeze_support()
    
    # Only run main if this is the actual script execution, not a subprocess
    if not hasattr(sys, '_called_from_test'):
        main()