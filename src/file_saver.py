import os
from pydub import AudioSegment

class FileSaver:
    SUPPORTED_FORMATS = {'mp3', 'wav', 'ogg', 'm4a'}

    def save_audio(self, audio_segment: AudioSegment, output_path: str):
        """
        Save an audio segment to a file.
        
        Args:
            audio_segment (AudioSegment): The audio to save
            output_path (str): Path where to save the audio file
            
        Raises:
            ValueError: If the file format is not supported or path is invalid
        """
        file_format = output_path.split('.')[-1].lower()
        if file_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except:
                raise ValueError("Invalid output directory path")

        try:
            audio_segment.export(output_path, format=file_format)
        except Exception as e:
            raise ValueError(f"Failed to save audio: {str(e)}") 