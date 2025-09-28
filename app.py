import whisper
import os
import sys
from audio_transcriber import transcribe_with_retry

# Supported audio and video file extensions
MEDIA_EXTS = {
    '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma', # audio
    '.mp4', '.mkv', '.mov', '.avi', '.webm', '.wmv', '.mpeg', '.mpg' # video
}

WHISPER_MODELS = { 'tiny', 'base', 'small', 'medium'}

def is_media_file(filename):
    return any(filename.lower().endswith(ext) for ext in MEDIA_EXTS)

def main():
    # When running as a .app, look in the user's current working directory
    # (where they double-clicked the .app from)
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        search_dir = os.getcwd()  # User's current directory
    else:
        # Running as a script
        search_dir = '.'

    while True:
        # Print model info for non-technical users
        print()
        print("Model Information:")
        print("  tiny: Fastest but least accurate")
        print("  base: Balanced speed and accuracy")
        print("  small: Slower but more accurate")
        print("  medium: Slowest but most accurate")
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
    print("Press Enter to start transcription, or Ctrl+C to cancel...")
    input()

    for media_file in files:
        print()
        print(f"Processing: {media_file}")
        full_path = os.path.join(search_dir, media_file)
        transcribe_with_retry(full_path, model=model_choice)

    print()
    print("="*50)
    print("All transcriptions completed!")
    print("Check for the *_transcription.txt files in the same folder.")
    print("="*50)
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()