# Audio Transcriber App - User Guide

## What This App Does
This app automatically converts your audio and video files into text transcriptions using advanced AI technology. Simply put your audio files in the same folder as the app and double-click to start!

## Supported File Types
- **Audio Files:** MP3, WAV, M4A, FLAC, AAC, OGG, WMA
- **Video Files:** MP4, MKV, MOV, AVI, WebM, WMV, MPEG, MPG

## How to Use the App

### Step 1: Organize Your Files
1. Create a new folder on your computer (you can name it anything like "My Audio Files")
2. Copy the **"Audio Transcriber.app"** into this folder
3. Copy all the audio/video files you want transcribed into the **same folder**

Your folder should look like this:
```
My Audio Files/
├── Audio Transcriber.app        ← The transcription app
├── interview.mp3                ← Your audio file
├── meeting_recording.wav        ← Your audio file
├── lecture.mp4                  ← Your video file
└── phone_call.m4a              ← Your audio file
```

### Step 2: First-Time Setup (Mac Security)
The first time you use the app, Mac will block it for security reasons. Here's how to allow it:

1. **Right-click** on "Audio Transcriber.app"
2. Select **"Open"** from the menu
3. Mac will show a security warning - click **"Open"** to confirm
4. After this first time, you can just double-click normally

*Alternative: If the above doesn't work, go to System Preferences → Security & Privacy → General, look for the blocked app message, and click "Allow Anyway"*

### Step 3: Run the Transcription
1. Make sure all your audio/video files are in the same folder as the app
2. **Double-click** "Audio Transcriber.app"
3. A black Terminal window will open and show you what files it found
4. Press **Enter** to start the transcription process
5. Watch the progress - it will show you which file it's working on
6. When all files are finished, press **Enter** to close the app

### Step 4: Find Your Transcriptions
After the process completes, you'll find a new **"transcriptions"** folder in the same location:

```
My Audio Files/
├── Audio Transcriber.app
├── interview.mp3
├── meeting_recording.wav
├── lecture.mp4
├── phone_call.m4a
└── transcriptions/              ← New folder created automatically
    ├── interview_transcription.txt
    ├── meeting_recording_transcription.txt
    ├── lecture_transcription.txt
    └── phone_call_transcription.txt
```

## What the Transcription Files Look Like
Each transcription file contains text with timestamps, making it easy to find specific parts of your audio:

```
[0.00s - 3.45s] Hello and welcome to today's interview.
[3.45s - 8.12s] We're here to discuss the latest developments in technology.
[8.12s - 12.67s] Our guest today is an expert in artificial intelligence.
[12.67s - 18.23s] Thank you for joining us today.
```

## Troubleshooting

### "No audio/video files found" Message
- **Solution:** Make sure your audio files are in the exact same folder as the "Audio Transcriber.app"
- Check that your files have supported extensions (MP3, WAV, MP4, etc.)

### Mac Won't Let You Open the App
- **Solution:** Right-click the app and choose "Open" instead of double-clicking
- If that doesn't work, go to System Preferences → Security & Privacy and allow the app

### The App Closes Immediately
- **Solution:** Make sure you're putting audio files in the same folder as the app, not in a subfolder
- Try right-clicking and selecting "Open" instead of double-clicking

### Processing Takes a Long Time
- **This is normal!** Transcription is a complex process that takes time
- Longer audio files will take more time to process
- The app will show you progress as it works - don't close the window until it's finished

### The Text Isn't Perfect
- AI transcription is very good but not 100% perfect
- Background noise, accents, or poor audio quality can affect accuracy
- Technical terms or unusual words might be transcribed incorrectly
- You can edit the text files afterward if needed

## Tips for Best Results

### Audio Quality
- **Clear audio works best** - avoid background noise when possible
- **Close microphone** recordings work better than distant ones
- **Good volume levels** - not too quiet or too loud

### File Management
- **Use simple file names** - avoid special characters like @, #, %, etc.
- **Keep file sizes reasonable** - very large files (over 1 hour) will take a long time
- **Process similar files together** - put related recordings in the same folder

### Workflow Suggestions
1. **Create separate folders** for different projects or topics
2. **Backup your original audio files** before transcribing
3. **Review transcriptions** and edit them if needed for accuracy
4. **Use descriptive names** for your audio files to keep transcriptions organized

## Technical Notes
- The app works completely offline - no internet required after initial setup
- Your audio files are processed locally on your computer - nothing is sent to the internet
- The app includes advanced AI models that may make it run slower on older computers
- First-time use may be slower as the AI models load into memory

## Need Help?
If you're having trouble:

1. **Check the file placement** - audio files must be in the same folder as the app
2. **Try the security steps** if the app won't open
3. **Be patient** - transcription takes time, especially for long files
4. **Check file formats** - make sure your audio files are in supported formats
5. **Restart and try again** if something goes wrong

The Terminal window will show helpful error messages if something isn't working correctly.
