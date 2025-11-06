"""
Audio Transcription Module
Extracts audio from video and transcribes it using OpenAI Whisper
"""

import whisper
import os
import subprocess
import tempfile


class AudioTranscriber:
    """Transcribes audio from video files using Whisper."""
    
    def __init__(self, model_size="base"):
        """
        Initialize the transcriber.
        
        Args:
            model_size: Whisper model size - "tiny", "base", "small", "medium", "large"
                       Smaller models are faster but less accurate
        """
        self.model_size = model_size
        self.model = None
    
    def load_model(self):
        """Lazy load the Whisper model."""
        if self.model is None:
            print(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
        return self.model
    
    def extract_audio(self, video_path, audio_path=None):
        """
        Extract audio from video file using ffmpeg.
        
        Args:
            video_path: Path to input video file
            audio_path: Path to save audio file (optional, creates temp file if not provided)
            
        Returns:
            Path to extracted audio file
        """
        if audio_path is None:
            # Create temporary audio file
            temp_dir = os.path.dirname(video_path)
            audio_path = os.path.join(temp_dir, f"audio_{os.path.basename(video_path)}.wav")
        
        # Use ffmpeg to extract audio
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i", video_path,
                    "-vn",  # No video
                    "-acodec", "pcm_s16le",  # PCM 16-bit
                    "-ar", "16000",  # Sample rate 16kHz (Whisper's preferred)
                    "-ac", "1",  # Mono
                    "-y",  # Overwrite output file
                    audio_path
                ],
                check=True,
                capture_output=True,
                stderr=subprocess.DEVNULL
            )
            return audio_path
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to extract audio: {e}")
        except FileNotFoundError:
            raise Exception("ffmpeg not found. Please install ffmpeg: brew install ffmpeg")
    
    def transcribe(self, video_path, language=None):
        """
        Transcribe audio from a video file.
        
        Args:
            video_path: Path to video file
            language: Language code (e.g., "en") or None for auto-detection
            
        Returns:
            Dictionary with transcription results:
            {
                "text": full transcribed text,
                "segments": list of segments with timestamps,
                "language": detected language
            }
        """
        # Extract audio
        audio_path = self.extract_audio(video_path)
        
        try:
            # Load model and transcribe
            model = self.load_model()
            
            # Transcribe with language hint if provided
            transcribe_kwargs = {}
            if language:
                transcribe_kwargs["language"] = language
            
            result = model.transcribe(audio_path, **transcribe_kwargs)
            
            # Clean up temporary audio file
            if os.path.exists(audio_path) and "audio_" in audio_path:
                try:
                    os.remove(audio_path)
                except:
                    pass
            
            return {
                "text": result["text"].strip(),
                "segments": result.get("segments", []),
                "language": result.get("language", "unknown")
            }
        except Exception as e:
            # Clean up on error
            if os.path.exists(audio_path) and "audio_" in audio_path:
                try:
                    os.remove(audio_path)
                except:
                    pass
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_audio_file(self, audio_path, language=None):
        """
        Transcribe an audio file directly (without video extraction).
        
        Args:
            audio_path: Path to audio file
            language: Language code or None for auto-detection
            
        Returns:
            Dictionary with transcription results
        """
        model = self.load_model()
        
        transcribe_kwargs = {}
        if language:
            transcribe_kwargs["language"] = language
        
        result = model.transcribe(audio_path, **transcribe_kwargs)
        
        return {
            "text": result["text"].strip(),
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown")
        }

