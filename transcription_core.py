"""
Core transcription logic that can be used by both CLI and GUI interfaces.
This module contains all the shared functionality for audio/video transcription.
"""

import os
import sys
from typing import List, Optional, Callable, Dict, Any


def setup_ffmpeg_path():
    """Set up ffmpeg path for PyInstaller bundle."""
    if getattr(sys, 'frozen', False):  # Running in a PyInstaller bundle
        bundled_ffmpeg = os.path.join(sys._MEIPASS, "ffmpeg")
        if os.path.exists(bundled_ffmpeg):
            # Set environment variable for ffmpeg-python
            os.environ["FFMPEG_BINARY"] = bundled_ffmpeg
            
            # Add to PATH for subprocess calls
            ffmpeg_dir = os.path.dirname(bundled_ffmpeg)
            current_path = os.environ.get("PATH", "")
            if ffmpeg_dir not in current_path:
                os.environ["PATH"] = ffmpeg_dir + os.pathsep + current_path


# Set up ffmpeg path early
setup_ffmpeg_path()


# Import whisper and audio_transcriber only when needed
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    from audio_transcriber import transcribe_with_retry
    TRANSCRIBER_AVAILABLE = True
except ImportError:
    TRANSCRIBER_AVAILABLE = False

# Supported audio and video file extensions
MEDIA_EXTS = {
    '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma',  # audio
    '.mp4', '.mkv', '.mov', '.avi', '.webm', '.wmv', '.mpeg', '.mpg'  # video
}

WHISPER_MODELS = {'tiny', 'base', 'small', 'medium'}

# Model descriptions for user-friendly display
MODEL_DESCRIPTIONS = {
    'tiny': 'Fastest but least accurate',
    'base': 'Balanced speed and accuracy (recommended)',
    'small': 'Slower but more accurate',
    'medium': 'Slowest but most accurate'
}


def is_media_file(filename: str) -> bool:
    """Check if a file is a supported audio/video file."""
    return any(filename.lower().endswith(ext) for ext in MEDIA_EXTS)


def find_media_files(search_dir: str) -> List[str]:
    """Find all media files in the specified directory."""
    try:
        files = [f for f in os.listdir(search_dir) 
                if os.path.isfile(os.path.join(search_dir, f)) and is_media_file(f)]
        return files
    except (OSError, PermissionError):
        return []


def get_search_directory() -> str:
    """Get the directory to search for media files."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.getcwd()


class TranscriptionSession:
    """Manages a transcription session with progress tracking."""
    
    def __init__(self, model_name: str = 'base', progress_callback: Optional[Callable] = None):
        self.model_name = model_name
        self.model = None
        self.progress_callback = progress_callback
        self.is_cancelled = False
        
    def load_model(self) -> bool:
        """Load the Whisper model. Returns True if successful."""
        if not WHISPER_AVAILABLE:
            if self.progress_callback:
                self.progress_callback("Error: Whisper not installed. Please install openai-whisper.")
            return False
            
        try:
            if self.progress_callback:
                self.progress_callback(f"Loading transcription model '{self.model_name}'...")
            
            self.model = whisper.load_model(self.model_name)
            
            if self.progress_callback:
                self.progress_callback("Transcription model loaded successfully.")
            
            return True
        except Exception as e:
            if self.progress_callback:
                self.progress_callback(f"Error loading model: {str(e)}")
            return False
    
    def transcribe_files(self, files: List[str], search_dir: str) -> Dict[str, Any]:
        """
        Transcribe multiple files with progress tracking.
        Returns a dictionary with results and statistics.
        """
        if not self.model:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        if not TRANSCRIBER_AVAILABLE:
            raise ValueError("Audio transcriber not available. Please check audio_transcriber.py.")
        
        results = {
            'total_files': len(files),
            'completed_files': 0,
            'failed_files': 0,
            'errors': []
        }
        
        for i, media_file in enumerate(files):
            if self.is_cancelled:
                break
                
            if self.progress_callback:
                self.progress_callback(f"Processing file {i+1} of {len(files)}: {media_file}")
            
            try:
                full_path = os.path.join(search_dir, media_file)
                transcribe_with_retry(full_path, model=self.model)
                results['completed_files'] += 1
                
                if self.progress_callback:
                    self.progress_callback(f"✓ Completed: {media_file}")
                    
            except Exception as e:
                results['failed_files'] += 1
                error_msg = f"Failed to transcribe {media_file}: {str(e)}"
                results['errors'].append(error_msg)
                
                if self.progress_callback:
                    self.progress_callback(f"✗ Failed: {media_file} - {str(e)}")
        
        return results
    
    def cancel(self):
        """Cancel the transcription session."""
        self.is_cancelled = True


def get_transcription_output_dir(search_dir: str) -> str:
    """Get the directory where transcriptions will be saved."""
    return os.path.join(search_dir, "transcriptions")


def validate_model_choice(model: str) -> bool:
    """Validate if the model choice is supported."""
    return model.lower() in WHISPER_MODELS


def get_model_info() -> Dict[str, str]:
    """Get model information for display."""
    return MODEL_DESCRIPTIONS.copy()