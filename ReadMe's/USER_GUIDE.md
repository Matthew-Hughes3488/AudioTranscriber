# 🎵 Audio Transcriber - Made with Love ❤️

**A warm, friendly tool to transcribe your interviews and research recordings**

*From Matthew to his amazing girlfriend - for all your academic research needs! 💝*

---

## What This Tool Does

This tool automatically transcribes your audio and video recordings into text files with timestamps, making it super easy to find specific parts of your interviews. Perfect for:

- 📝 Research interviews
- 🎓 Lecture recordings  
- 📞 Phone calls
- 🎤 Focus groups
- 📺 Video recordings

---

## How to Use (Super Simple!)

### Option 1: Easy GUI Mode (Recommended) 🖱️

Just **double-click** the app and use the friendly interface:

1. **Open the app** - Double-click `Audio Transcriber.app` (Mac) or run `python app.py`
2. **Choose your files** - Click "Choose Files" or "Find Files in Folder" 
3. **Pick a model** - Choose how fast vs. accurate you want (Base is usually perfect!)
4. **Start transcribing** - Click "Start Transcription" and wait
5. **Find your transcripts** - They'll be in a "transcriptions" folder

### Option 2: Command Line Mode 💻

For tech-savvy users or batch processing:

```bash
# Launch CLI mode
python app.py --cli

# Or use the original way
python cli_app.py
```

---

## Quick Start Guide

### Step 1: Put Everything Together
Create a folder and put these items in it:
- ✅ The transcriber app
- ✅ Your audio/video files to transcribe

### Step 2: Run the App
- **Mac**: Double-click `Audio Transcriber.app`
- **Windows/Linux**: Open terminal and run `python app.py`

### Step 3: Choose Your Settings
- **Model**: Start with "Base" (good balance of speed and accuracy)
- **Files**: Select the recordings you want transcribed

### Step 4: Let It Work
- Click "Start Transcription"
- Go grab a coffee ☕ - this can take a while for long recordings
- Watch the progress updates

### Step 5: Find Your Results
Your transcripts will be saved as `.txt` files in a new `transcriptions` folder, with timestamps like:

```
[0.00s - 3.45s] Hello and welcome to today's interview.
[3.45s - 8.12s] We're here to discuss your research on educational psychology.
[8.12s - 12.67s] Could you tell us about your methodology?
```

---

## Model Guide - Which One to Choose?

| Model | Speed | Accuracy | Best For |
|-------|--------|----------|----------|
| **Tiny** | ⚡⚡⚡⚡ | ⭐⭐ | Quick drafts, rough transcripts |
| **Base** | ⚡⚡⚡ | ⭐⭐⭐ | **Most people (RECOMMENDED)** |
| **Small** | ⚡⚡ | ⭐⭐⭐⭐ | Higher quality needed |

💡 **Start with "Base"** - it's the sweet spot for most academic work!

---

## Supported File Types

### Audio Files 🎵
- MP3, WAV, M4A, FLAC, AAC, OGG, WMA

### Video Files 📹  
- MP4, MKV, MOV, AVI, WEBM, WMV, MPEG, MPG

---

## Tips for Best Results

### 🎤 Recording Quality
- **Clear audio is key** - avoid background noise when possible
- **Good microphone placement** - closer is better
- **Reasonable volume** - not too quiet or too loud

### 📁 File Management
- **Use simple filenames** - avoid special characters (@, #, %, etc.)
- **Keep files reasonable size** - very long recordings take much longer
- **Organize by project** - create separate folders for different research projects

### 🔄 Workflow Tips
1. **Back up originals** before transcribing
2. **Review transcripts** - AI is good but not perfect!
3. **Use timestamps** to quickly find specific parts in your original recordings
4. **Edit transcripts** as needed for your final work

---

## Troubleshooting

### "No files found"
- Make sure audio/video files are in the same folder as the app
- Check that your files have the right extensions (.mp3, .wav, etc.)

### "App won't start" (Mac)
- Right-click the app and select "Open" (security permission needed first time)

### "Transcription failed"
- Try a smaller file first to test
- Check that your audio isn't corrupted
- Make sure you have enough disk space

### "Taking too long"
- Long recordings take time! 1 hour of audio ≈ 10-30 minutes to transcribe
- Try the "Tiny" model for faster (but less accurate) results
- Close other programs to free up computer resources

---

## Getting Help

If something isn't working:

1. **Check the error messages** - they usually explain what's wrong
2. **Try with a short test file** first
3. **Contact Matt** - he made this with love and wants it to work for you! 💕

---

## Technical Details

### Installation Requirements
- Python 3.8 or newer
- FFmpeg (for video files)
- About 2-5 GB of disk space (for AI models)

### Advanced Usage
```bash
# Show help
python app.py --help

# Force GUI mode
python app.py --gui

# Force CLI mode  
python app.py --cli
```

---

## What Makes This Special

This tool was made specifically for academic research with love and care:

- 💝 **Personal touch** - Made by Matthew for his girlfriend's dissertation research
- 🎓 **Academic-focused** - Perfect for interviews, focus groups, and research recordings  
- 🤗 **Non-technical friendly** - No command line knowledge needed
- ⏰ **Timestamps included** - Easy to find specific quotes in your original recordings
- 🔄 **Batch processing** - Transcribe multiple files at once
- 📁 **Organized output** - Creates neat folders for your transcripts

---

*Made with ❤️ for academic excellence and research success!*

**Happy transcribing! 🎉**