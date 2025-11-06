# Interview Analysis Feature

## Overview

The HR Interview Analytics Platform now includes comprehensive interview analysis capabilities that automatically transcribe video interviews and evaluate candidates based on multiple parameters.

## Features

### 1. Video Transcription
- Automatically extracts audio from uploaded interview videos
- Transcribes speech to text using OpenAI Whisper (base model)
- Supports multiple languages with auto-detection
- Provides word-level timestamps

### 2. Candidate Evaluation

The system evaluates candidates on **5 key parameters**:

1. **Communication Clarity** (0-100%)
   - Sentence structure and length
   - Vocabulary diversity
   - Text organization and clarity

2. **Confidence & Assertiveness** (0-100%)
   - Sentiment positivity
   - Use of confidence keywords
   - Language assertiveness

3. **Enthusiasm & Positivity** (0-100%)
   - Positive sentiment analysis
   - Enthusiasm keywords
   - Overall energy in language

4. **Professionalism** (0-100%)
   - Professional keywords usage
   - Language formality
   - Balanced sentiment (not overly emotional)

5. **Engagement & Energy** (0-100%)
   - Text length and detail
   - Sentiment strength
   - Language variety

### 3. Overall Score

The system calculates an overall score (0-100%) based on the average of all 5 parameters, providing a quick assessment of candidate performance.

## How It Works

1. **Upload Video**: Upload an interview video file
2. **Frame Extraction**: System extracts frames for face detection
3. **Audio Transcription**: Audio is extracted and transcribed using Whisper
4. **Sentiment Analysis**: Transcribed text is analyzed using TextBlob and VADER
5. **Candidate Evaluation**: Scores are calculated for each parameter
6. **Results Display**: Comprehensive results are shown including:
   - Full transcription
   - Individual parameter scores
   - Overall score
   - Sentiment analysis
   - Summary and recommendations

## Technical Details

### Dependencies

- **OpenAI Whisper**: For speech-to-text transcription
- **TextBlob**: For sentiment analysis (polarity and subjectivity)
- **VADER**: For sentiment analysis (compound scores and emotion breakdown)
- **FFmpeg**: For audio extraction from video files

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg (required for audio extraction):
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

3. First run will download Whisper model (base model, ~150MB)

### API Endpoints

- `POST /upload/` - Upload video and get analysis results
  - Parameters:
    - `file`: Video file (multipart/form-data)
    - `step`: Frame extraction step (default: 30)
    - `transcribe`: Enable transcription (default: true)

### Response Format

```json
{
  "frame_analysis": {...},
  "transcription": {
    "text": "Full transcribed text...",
    "language": "en",
    "segments": [...]
  },
  "evaluation": {
    "scores": {
      "communication_clarity": 0.75,
      "confidence": 0.82,
      "enthusiasm": 0.68,
      "professionalism": 0.79,
      "engagement": 0.71
    },
    "overall_score": 0.75,
    "overall_sentiment": {
      "label": "positive",
      "confidence": 0.65
    }
  }
}
```

## Usage Tips

1. **Video Quality**: Better audio quality = better transcription accuracy
2. **Language**: System auto-detects language, but works best with English
3. **Processing Time**: Transcription takes time based on video length (approximately 1-2x video duration)
4. **Model Size**: Currently using "base" model for balance between speed and accuracy. Can be changed in `audio_transcriber.py`

## Troubleshooting

### FFmpeg Not Found
- Install FFmpeg using package manager
- Ensure it's in your system PATH

### Transcription Fails
- Check video has audio track
- Verify video format is supported
- Check system has enough memory (Whisper requires ~2GB RAM)

### Low Scores
- Scores are relative and based on language patterns
- Consider context: technical interviews may score differently than behavioral interviews
- Review individual parameters for specific insights

## Future Enhancements

- Support for multiple speakers (speaker diarization)
- Custom evaluation criteria
- Comparison between multiple candidates
- Export evaluation reports
- Integration with ATS systems

