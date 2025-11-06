# Troubleshooting Guide

## Error: "Request failed with status code 500"

### Issue
The video upload fails with a 500 error, typically because transcription dependencies are missing.

### Solution

The application has been updated to handle missing dependencies gracefully. Video processing (frame extraction and face detection) will work even without transcription features.

However, to enable full transcription and evaluation features, you need to:

#### 1. Install Python Dependencies

```bash
cd hr-video-analyzer
pip install openai-whisper ffmpeg-python torch
```

**Note**: Installing `torch` (PyTorch) can be large (~2GB). For Apple Silicon Macs, you may want to install the optimized version:

```bash
pip install torch torchvision torchaudio
```

#### 2. Install FFmpeg

FFmpeg is required to extract audio from video files.

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

#### 3. Verify Installation

```bash
# Check FFmpeg
ffmpeg -version

# Check Python packages
python3 -c "import whisper; import ffmpeg; print('All dependencies installed!')"
```

### Current Behavior

- **Without transcription dependencies**: Video processing works, but transcription and evaluation features are disabled. You'll see a helpful error message in the UI.
- **With transcription dependencies**: Full functionality including transcription and candidate evaluation.

### Testing

1. Upload a video without transcription dependencies installed
   - Should work for frame extraction and face detection
   - Will show error message about missing dependencies

2. Install dependencies and upload again
   - Should now transcribe audio and evaluate candidate

### Common Issues

#### "ModuleNotFoundError: No module named 'whisper'"
- Solution: `pip install openai-whisper`

#### "ffmpeg not found"
- Solution: Install FFmpeg using package manager (see above)

#### "CUDA out of memory" or slow processing
- Solution: Use a smaller Whisper model. Edit `video_processor.py` and change `model_size="base"` to `model_size="tiny"` (faster but less accurate)

#### Large download on first run
- Whisper models are downloaded on first use. The "base" model is ~150MB. This is normal.

### Getting Help

If issues persist:
1. Check server logs for detailed error messages
2. Verify all dependencies are installed: `pip list | grep -E "whisper|ffmpeg|torch"`
3. Ensure FFmpeg is in PATH: `which ffmpeg`
4. Check Python version: `python3 --version` (should be 3.8+)

