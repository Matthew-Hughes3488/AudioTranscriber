import whisper
import os
import sys
import multiprocessing
from audio_transcriber import transcribe_with_retry
import time


# Force unbuffered output for stdout and stderr
os.environ["PYTHONUNBUFFERED"] = "1"
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), "w", buffering=1)

# Supported audio and video file extensions
MEDIA_EXTS = {
    '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma', # audio
    '.mp4', '.mkv', '.mov', '.avi', '.webm', '.wmv', '.mpeg', '.mpg' # video
}

WHISPER_MODELS = { 'tiny', 'base', 'small', 'medium'}

def slow_type(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() 

def is_media_file(filename):
    return any(filename.lower().endswith(ext) for ext in MEDIA_EXTS)

def main():
    try:
        # When running as a .app, look in the user's current working directory
        # (where they double-clicked the .app from)
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller bundle
            search_dir = os.path.dirname(sys.executable)  # Directory of the .app file
        else:
            # Running as a script
            search_dir = os.getcwd()  # Current working directory

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
        print("{:^80}".format("From Matthew ❤️"))
        print("=" * 80)
        print()

        while True:
            # Print model info for non-technical users
            print()
            slow_type("Model Information:")
            slow_type("  tiny: Fastest but least accurate")
            slow_type("  base: Balanced speed and accuracy")
            slow_type("  small: Slower but more accurate")
            slow_type("  medium: Slowest but most accurate")
            print()
            model_choice = input(f"Choose Whisper model {WHISPER_MODELS} (default: base): ").strip().lower()
            if model_choice == '':
                model_choice = 'base'
            if model_choice in WHISPER_MODELS:
                break
            else:
                print(f"Invalid choice. Please choose from {WHISPER_MODELS}.")

        print()
        files = [f for f in os.listdir(search_dir) if os.path.isfile(os.path.join(search_dir, f)) and is_media_file(f)]
        if not files:
            print(f"No audio/video files found in: {os.path.abspath(search_dir)}")
            print("Please place your audio/video files in the same folder as this app.")
            input("Press Enter to exit...")
            return

        print(f"Found {len(files)} media file(s) in: {os.path.abspath(search_dir)}")
        for f in files:
            print(f"  {f}")

        print()
        print("Press Enter to start the transcriptions, or Ctrl+C to cancel...")
        input()

        print(f"Loading transcription model '{model_choice}'...")
        model = whisper.load_model(model_choice)
        print("Transcription model loaded successfully.")
        for media_file in files:
            print()
            print(f"Processing: {media_file}")
            full_path = os.path.join(search_dir, media_file)
            transcribe_with_retry(full_path, model=model)

        print()
        print("="*50)
        print("All transcriptions completed!")
        print("Check for the *_transcription.txt files in the same folder.")
        print("="*50)
        print()
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    # Fix for PyInstaller multiprocessing issues
    import multiprocessing
    multiprocessing.freeze_support()
    
    # Only run main if this is the actual script execution, not a subprocess
    if not hasattr(sys, '_called_from_test'):
        main()