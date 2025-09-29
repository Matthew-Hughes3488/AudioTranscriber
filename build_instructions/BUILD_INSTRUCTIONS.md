# Building Audio Transcriber for Distribution

The Audio Transcriber now supports both GUI and CLI modes, making it even more user-friendly!

## New Dual-Mode Architecture

The app has been refactored into several components:
- `app.py` - Main entry point (supports `--gui`, `--cli`, `--help`)
- `gui_app.py` - Friendly GUI interface (default)
- `cli_app.py` - Command line interface  
- `transcription_core.py` - Shared transcription logic

## Prerequisites

1. Install PyInstaller and dependencies:
   ```bash
   source venv_dissertation_transcriber/bin/activate
   pip install -r requirements.txt
   ```

## Building Options

### Option 1: GUI Mode (Recommended for End Users)
Build with GUI as the default interface:

```bash
# Build GUI version
pyinstaller --onefile --windowed --name "Audio Transcriber GUI" app.py \
  --add-data "/Users/matthewhughes/development/AudioTranscriber/venv_audio/lib/python3.12/site-packages/whisper/assets:whisper/assets" \
  --add-binary "/opt/homebrew/bin/ffmpeg:." \
  --add-data "/Users/matthewhughes/.cache/whisper:whisper"
```

### Option 2: CLI Mode (For Power Users)
Build with CLI interface only:

```bash
# Build CLI version
pyinstaller --onefile --name "Audio Transcriber CLI" cli_app.py \
  --add-data "/Users/matthewhughes/development/AudioTranscriber/venv_audio/lib/python3.12/site-packages/whisper/assets:whisper/assets" \
  --add-binary "/opt/homebrew/bin/ffmpeg:." \
  --add-data "/Users/matthewhughes/.cache/whisper:whisper"
```

### Option 3: Universal Build (Both Modes)
Build with both GUI and CLI support:

```bash
# Build universal version
pyinstaller --onefile --name "Audio Transcriber" app.py \
  --add-data "/Users/matthewhughes/development/AudioTranscriber/venv_audio/lib/python3.12/site-packages/whisper/assets:whisper/assets" \
  --add-binary "/opt/homebrew/bin/ffmpeg:." \
  --add-data "/Users/matthewhughes/.cache/whisper:whisper"
```

## Updated Usage for End Users

### GUI Mode (Default)
1. Double-click `Audio Transcriber` (or `Audio Transcriber.exe` on Windows)
2. The friendly GUI interface will appear
3. Use the "Choose Files" or "Find Files in Folder" buttons
4. Select your transcription model
5. Click "Start Transcription"
6. Watch the progress and find results in the `transcriptions` folder

### CLI Mode
1. Run with `--cli` flag: `./Audio\ Transcriber --cli`
2. Or use the dedicated CLI build
3. Follow the original command-line interface

### Help
Run `./Audio\ Transcriber --help` to see all options

## Key Improvements

- **Dual Interface**: GUI for non-technical users, CLI for power users
- **Smart Fallback**: Automatically falls back to CLI if GUI unavailable  
- **Better UX**: Warm, friendly interface with clear progress tracking
- **File Management**: Easy file selection with drag-and-drop support
- **Error Handling**: Friendly error messages instead of technical errors
- **Progress Tracking**: Real-time updates during transcription

## Distribution Notes

- **GUI Version**: Perfect for non-technical end users
- **File Size**: Expect 2-5GB due to AI models and dependencies
- **Cross-Platform**: Works on Mac, Windows, Linux
- **Dependencies**: All included in the executable
- **First Run**: May be slower while downloading/caching models

## Troubleshooting

### "GUI won't start"
- Try CLI mode: `./Audio\ Transcriber --cli` 
- Check that tkinter is available on the target system

### "No display available"
- The app will automatically fall back to CLI mode on headless systems

### Performance Issues  
- GUI mode uses threading to prevent interface freezing
- CLI mode processes files sequentially for simpler debugging

---

*The GUI makes this tool perfect for non-technical users while maintaining all the power of the original CLI!*
