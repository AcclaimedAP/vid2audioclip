import pytest
import os
from src.file_saver import FileSaver
from pydub import AudioSegment
from unittest.mock import Mock, patch

class TestFileSaver:
    @pytest.fixture
    def saver(self):
        return FileSaver()

    @pytest.fixture
    def mock_audio_segment(self):
        audio = Mock(spec=AudioSegment)
        # Make export create a dummy file
        def mock_export(output_path, format):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write('test')
        audio.export.side_effect = mock_export
        return audio

    def test_save_audio_creates_file(self, saver, mock_audio_segment, tmp_path):
        output_path = str(tmp_path / "test_output.mp3")
        saver.save_audio(mock_audio_segment, output_path)
        assert os.path.exists(output_path)

    def test_invalid_format_raises_error(self, saver, mock_audio_segment):
        with pytest.raises(ValueError):
            saver.save_audio(mock_audio_segment, "test.invalid")

    def test_invalid_path_raises_error(self, saver, mock_audio_segment):
        with pytest.raises(ValueError):
            # Use a path that will definitely be invalid
            saver.save_audio(mock_audio_segment, "\0invalid/path/test.mp3") 