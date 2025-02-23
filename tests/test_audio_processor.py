import pytest
from src.audio_processor import AudioProcessor
from pydub import AudioSegment
from unittest.mock import Mock, patch, MagicMock
from src.utils.time_converter import TimeConverter

class TestAudioProcessor:
    @pytest.fixture
    def processor(self):
        with patch('pydub.AudioSegment.from_file') as mock_from_file:
            # Create a mock audio segment that supports slicing and addition
            mock_audio = MagicMock(spec=AudioSegment)
            mock_audio.duration_seconds = 600  # 10 minutes duration
            mock_audio.dBFS = -20
            
            # Configure the mock to return itself for slicing
            mock_audio.__getitem__.return_value = mock_audio
            
            # Configure the mock to return itself for addition
            mock_audio.__add__.return_value = mock_audio
            mock_audio.__radd__.return_value = mock_audio
            
            mock_from_file.return_value = mock_audio
            processor = AudioProcessor("test_video.mp4")
            yield processor

    def test_init_loads_audio(self, processor):
        assert processor.audio is not None
        assert processor.start_time == 0
        assert processor.end_time == 600  # 10 minutes

    def test_set_time_range(self, processor):
        processor.set_time_range("2:00", "8:00")
        assert processor.start_time == 120  # 2 minutes
        assert processor.end_time == 480    # 8 minutes

    def test_adjust_time_range(self, processor):
        processor.set_time_range("2:00", "8:00")
        processor.adjust_time_range("1:00", "-1:00")  # Add 1 minute to start, subtract 1 minute from end
        assert processor.start_time == 180  # 3 minutes
        assert processor.end_time == 420    # 7 minutes

    def test_invalid_time_range_raises_error(self, processor):
        with pytest.raises(ValueError):
            processor.set_time_range("-1:00", "11:00")
        with pytest.raises(ValueError):
            processor.set_time_range("5:00", "2:00")
        with pytest.raises(ValueError):
            processor.set_time_range("invalid", "2:00")

    @patch('src.audio_processor.playsound')
    @patch.object(AudioSegment, 'export')
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs', return_value=None)
    def test_play_preview(self, mock_makedirs, mock_exists, mock_export, mock_playsound, processor):
        processor.set_time_range("0:02", "0:04")
        
        # Create a mock audio segment with its own export method
        mock_segment = MagicMock(spec=AudioSegment)
        mock_segment.export = Mock(return_value=None)  # Add export method directly to segment
        
        # Configure the audio slice to return our mock segment
        processor.audio.__getitem__.return_value = mock_segment
        
        processor.play_preview()
        
        # Verify that the segment's export method was called
        assert mock_segment.export.called
        assert mock_segment.export.call_args[1]['format'] == 'wav'  # Check format parameter
        mock_playsound.assert_called_once()

    def test_adjust_volume(self, processor):
        original_volume = -20
        processor.audio.dBFS = original_volume
        
        # Mock the volume adjustment behavior
        def adjust_volume(db_change):
            processor.audio.dBFS = original_volume + db_change
            return processor.audio
            
        processor.audio.__add__.side_effect = adjust_volume
        
        # Test
        processor.adjust_volume(10)
        assert processor.audio.dBFS == -10  # Original (-20) + adjustment (10) 