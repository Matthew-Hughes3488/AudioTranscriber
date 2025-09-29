import os
import sys
import subprocess


def get_ffmpeg_path():
    """Get the path to the ffmpeg binary, using bundled version if available."""
    if getattr(sys, 'frozen', False):  # Running in a PyInstaller bundle
        bundled_ffmpeg = os.path.join(sys._MEIPASS, "ffmpeg")
        if os.path.exists(bundled_ffmpeg):
            return bundled_ffmpeg
    
    # Fall back to system ffmpeg
    return "ffmpeg"


def setup_ffmpeg_for_whisper():
    """Configure ffmpeg path for Whisper to use the bundled version."""
    ffmpeg_path = get_ffmpeg_path()
    
    # Set environment variable for ffmpeg-python to use our bundled version
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    
    # Also add the directory to PATH so subprocess calls can find it
    if getattr(sys, 'frozen', False):
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        current_path = os.environ.get("PATH", "")
        if ffmpeg_dir not in current_path:
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + current_path


# Call this early to set up ffmpeg for the entire application
setup_ffmpeg_for_whisper()


def transcribe_with_retry(file_path, max_retries=3, model=None):
    for attempt in range(1, max_retries + 1):
        try:
            transcribe_audio(file_path, model=model)
            print(f"Transcription succeeded for {file_path} on attempt {attempt}")
            return  # Ensure function exits after success
        except Exception as e:
            print(f"Attempt {attempt} failed for {file_path}: {e}")
            if attempt == max_retries:
                print(f"Giving up on {file_path} after {max_retries} attempts.")

def transcribe_audio(file_path, model=None):
    if model is None:
        raise ValueError("A valid Whisper model instance must be provided.")

    print()
    print("Starting transcription...")
    result = model.transcribe(file_path)
    print()
    print("Transcription completed.")
    
    audio_dir = os.path.dirname(file_path)
    
    transcriptions_dir = os.path.join(audio_dir, "transcriptions")
    os.makedirs(transcriptions_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(transcriptions_dir, f"{base_name}_transcription.txt")
    
    store_transcription(result, output_file)

def store_transcription(result, output_file="transcription.txt"):
    print()
    print(f"Storing transcription to {output_file}...")
    with open(output_file, "w") as f:
        for segment in result["segments"]:
            f.write(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}\n")
    print("Transcription stored successfully.")
    print()