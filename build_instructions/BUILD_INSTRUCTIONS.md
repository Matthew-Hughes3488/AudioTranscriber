# Building Audio Transcriber .app for macOS

## Prerequisites
1. Install PyInstaller in your virtual environment:
   ```bash
   source venv_dissertation_transcriber/bin/activate
   pip install pyinstaller
   ```

## Building the .app

1. Activate your virtual environment:
   ```bash
   source venv_dissertation_transcriber/bin/activate
   ```

2. Build the .app using the spec file:
   ```bash
   pyinstaller AudioTranscriber.spec
   ```

3. The .app will be created in the `dist/` folder as `Audio Transcriber.app`

## Code Changes Made for .app Distribution

The following changes were made to ensure the app works correctly when distributed as a .app:

1. **Directory Detection**: The app now detects if it's running as a PyInstaller bundle and looks for audio files in the user's current working directory (where they double-clicked the .app)

2. **User Feedback**: Added clear messages showing where the app is looking for files and prompting the user before starting

3. **Error Handling**: Better error messages if no files are found

4. **Console Output**: The app keeps the console window open so users can see progress and results

## Usage for End Users

1. Put the `Audio Transcriber.app` in any folder
2. Put audio/video files in the same folder as the .app
3. Double-click `Audio Transcriber.app`
4. Follow the on-screen prompts
5. Transcription files will be saved in the same folder

## Notes

- The .app includes all dependencies (Whisper, PyTorch, etc.)
- The first run may be slower as it loads the AI model
- Users don't need Python or any technical setup
- The app will show a console window with progress information
- Transcription files are saved as `[filename]_transcription.txt` in the same folder as the audio files

## Troubleshooting

- If the .app doesn't run, users may need to right-click and select "Open" the first time (macOS security)
- The .app file will be quite large (several GB) due to the included AI models and PyTorch dependencies
- Consider using the "base" model instead of "tiny" for better accuracy, or "large" for best accuracy (but larger file size)
