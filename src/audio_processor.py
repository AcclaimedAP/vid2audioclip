import os
import uuid
from pathlib import Path
from pydub import AudioSegment
from playsound import playsound
import time
from .utils.time_converter import TimeConverter

class AudioProcessor:
    def __init__(self, video_path: str):
        """
        Initialize the audio processor with a video file.
        
        Args:
            video_path (str): Path to the video file
        """
        self.audio = AudioSegment.from_file(video_path)
        self.start_time = 0
        self.end_time = self.audio.duration_seconds
        
        # Create temporary directory with unique name in current directory
        unique_id = str(uuid.uuid4())[:8]
        self.temp_dir = os.path.join(os.getcwd(), 'temp', f'audio_preview_{unique_id}')
        os.makedirs(self.temp_dir, exist_ok=True)

    def set_time_range(self, start: str | float, end: str | float):
        """
        Set the time range for audio processing.
        
        Args:
            start: Start time in format "MM:SS.ms" or "HH:MM:SS.ms", or seconds as float
            end: End time in format "MM:SS.ms" or "HH:MM:SS.ms", or seconds as float
            
        Raises:
            ValueError: If time range is invalid
        """
        try:
            # Convert numeric inputs to strings
            if isinstance(start, (int, float)):
                start = str(start)
            if isinstance(end, (int, float)):
                end = str(end)
            
            start_seconds = TimeConverter.time_to_seconds(start)
            end_seconds = TimeConverter.time_to_seconds(end)
            
            if start_seconds < 0 or end_seconds > self.audio.duration_seconds or start_seconds >= end_seconds:
                raise ValueError("Invalid time range")
                
            self.start_time = start_seconds
            self.end_time = end_seconds
            
        except ValueError as e:
            raise ValueError(f"Invalid time format: {str(e)}")

    def adjust_time_range(self, start_offset: str | float, end_offset: str | float):
        """
        Adjust the current time range by the given offsets.
        
        Args:
            start_offset: Offset to add to start time (e.g., "0:05" or "-0:05"), or seconds as float
            end_offset: Offset to add to end time (e.g., "0:05" or "-0:05"), or seconds as float
        """
        try:
            # Convert numeric inputs to strings
            if isinstance(start_offset, (int, float)):
                start_offset = str(start_offset)
            if isinstance(end_offset, (int, float)):
                end_offset = str(end_offset)
            
            start_offset_seconds = TimeConverter.time_to_seconds(start_offset, allow_negative=True)
            end_offset_seconds = TimeConverter.time_to_seconds(end_offset, allow_negative=True)
            
            new_start = self.start_time + start_offset_seconds
            new_end = self.end_time + end_offset_seconds
            
            # Convert back to time strings for set_time_range
            self.set_time_range(
                TimeConverter.seconds_to_time(new_start),
                TimeConverter.seconds_to_time(new_end)
            )
            
        except ValueError as e:
            raise ValueError(f"Invalid time format: {str(e)}")

    def play_preview(self):
        """Play the selected portion of the audio."""
        try:
            start_ms = int(self.start_time * 1000)
            end_ms = int(self.end_time * 1000)
            audio_slice = self.audio[start_ms:end_ms]
            
            # Ensure temp directory exists
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Create a new preview file with timestamp
            timestamp = int(time.time() * 1000)
            preview_path = os.path.join(self.temp_dir, f'preview_{timestamp}.wav')
            
            # Remove old preview files
            self._cleanup_old_previews()
            
            # Export and verify file was created
            audio_slice.export(preview_path, format='wav')
            if not os.path.exists(preview_path):
                raise ValueError("Failed to create preview file")
            
            # Play the audio
            playsound(preview_path)
            
        except Exception as e:
            raise ValueError(f"Failed to play preview: {str(e)}")

    def _cleanup_old_previews(self):
        """Clean up old preview files."""
        try:
            for file in os.listdir(self.temp_dir):
                if file.startswith('preview_') and file.endswith('.wav'):
                    file_path = os.path.join(self.temp_dir, file)
                    try:
                        os.remove(file_path)
                    except:
                        pass
        except:
            pass

    def adjust_volume(self, db_change: float):
        """
        Adjust the volume of the audio.
        
        Args:
            db_change (float): Decibel change (positive or negative)
        """
        self.audio = self.audio + db_change

    def get_audio_segment(self) -> AudioSegment:
        """
        Get the currently selected audio segment.
        
        Returns:
            AudioSegment: The selected portion of audio
        """
        start_ms = int(self.start_time * 1000)
        end_ms = int(self.end_time * 1000)
        return self.audio[start_ms:end_ms]

    def cleanup(self):
        """Remove the temporary directory and all its contents."""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except:
                pass

    def __del__(self):
        """Ensure cleanup is called when the object is destroyed."""
        self.cleanup() 