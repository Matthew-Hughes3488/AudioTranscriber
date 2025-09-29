"""
CLI interface for audio/video transcription using OpenAI Whisper.
This is the command-line version that maintains the original functionality.
"""

import os
import sys
import time
from transcription_core import (
    TranscriptionSession, find_media_files, get_search_directory,
    WHISPER_MODELS, get_model_info, validate_model_choice
)

# Force unbuffered output for stdout and stderr
os.environ["PYTHONUNBUFFERED"] = "1"
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), "w", buffering=1)


def slow_type(text, delay=0.01):
    """Type text slowly for effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 


def display_banner():
    """Display the welcome banner."""
    print()
    print("=" * 80)
    print("{:^80}".format("██   ██ ███████ ██      ██       ██████       █████  ███    ███ ██    ██"))
    print("{:^80}".format("██   ██ ██      ██      ██      ██    ██     ██   ██ ████  ████  ██  ██ "))
    print("{:^80}".format("███████ █████   ██      ██      ██    ██     ███████ ██ ████ ██   ████  "))
    print("{:^80}".format("██   ██ ██      ██      ██      ██    ██     ██   ██ ██  ██  ██    ██   "))
    print("{:^80}".format("██   ██ ███████ ███████ ███████  ██████      ██   ██ ██      ██    ██   "))
    print()
    print("{:^80}".format("🎵 AUDIO TRANSCRIPTION TOOL 🎵"))
    print("{:^80}".format("Made with love for you to transcribe your interviews easily!"))
    print("{:^80}".format("From Matt ❤️"))
    print("=" * 80)
    print()


def get_model_choice():
    """Get user's model choice via command line."""
    model_info = get_model_info()
    
    print("Model Information:")
    for model, description in model_info.items():
        print(f"  {model}: {description}")
    print()
    
    while True:
        model_choice = input(f"Choose Transcription Model {WHISPER_MODELS} (default: base): ").strip().lower()
        if model_choice == '':
            model_choice = 'base'
        if validate_model_choice(model_choice):
            return model_choice
        else:
            print(f"Invalid choice. Please choose from {WHISPER_MODELS}.")


def display_found_files(files, search_dir):
    """Display found media files to the user."""
    if not files:
        print(f"No audio/video files found in: {os.path.abspath(search_dir)}")
        print("Please place your audio/video files in the same folder as this app.")
        return False
    
    print(f"Found {len(files)} media file(s) in: {os.path.abspath(search_dir)}")
    for f in files:
        print(f"  {f}")
    return True


def cli_progress_callback(message):
    """Progress callback for CLI output."""
    print(message)


def main():
    """Main CLI application entry point."""
    try:
        # Get search directory
        search_dir = get_search_directory()
        
        # Display banner
        display_banner()
        
        # Get model choice
        model_choice = get_model_choice()
        print()
        
        # Find media files
        files = find_media_files(search_dir)
        if not display_found_files(files, search_dir):
            input("Press Enter to exit...")
            return
        
        # Confirm start
        print()
        print("Press Enter to start the transcriptions, or Ctrl+C to cancel...")
        input()
        
        # Create transcription session
        session = TranscriptionSession(model_choice, cli_progress_callback)
        
        # Load model
        if not session.load_model():
            print("Failed to load model. Exiting...")
            input("Press Enter to exit...")
            return
        
        # Start transcription
        print()
        results = session.transcribe_files(files, search_dir)
        
        # Display results
        print()
        print("="*80)
        print("Transcription Results:")
        print(f"  Total files: {results['total_files']}")
        print(f"  Completed: {results['completed_files']}")
        print(f"  Failed: {results['failed_files']}")
        
        if results['errors']:
            print("\nErrors encountered:")
            for error in results['errors']:
                print(f"  {error}")
        
        if results['completed_files'] > 0:
            print(f"\nTranscription files saved in: {os.path.join(search_dir, 'transcriptions')}")
        
        print("="*80)
        print()
        input("Press Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\nTranscription cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        print("Contact your Matt if you need help.")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    # Fix for PyInstaller multiprocessing issues
    import multiprocessing
    multiprocessing.freeze_support()
    
    # Only run main if this is the actual script execution, not a subprocess
    if not hasattr(sys, '_called_from_test'):
        main()