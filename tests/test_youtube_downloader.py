import pytest
import os
from src.youtube_downloader import YoutubeDownloader
from unittest.mock import Mock, patch

class TestYoutubeDownloader:
    @pytest.fixture
    def downloader(self):
        return YoutubeDownloader()

    def test_init_creates_temp_directory(self, downloader):
        assert os.path.exists(downloader.temp_dir)
        assert downloader.temp_dir.endswith('youtube_temp')

    @patch('src.youtube_downloader.YouTube')
    def test_download_video_success(self, mock_youtube, downloader):
        # Mock setup
        mock_stream = Mock()
        mock_stream.download.return_value = os.path.join(downloader.temp_dir, "video.mp4")
        mock_yt = Mock()
        mock_yt.streams.filter.return_value.first.return_value = mock_stream
        mock_youtube.return_value = mock_yt

        # Test
        result = downloader.download_video("https://youtube.com/watch?v=dQw4w9WgXcQ")
        assert result.endswith('.mp4')
        assert os.path.dirname(result) == downloader.temp_dir

    def test_cleanup_removes_temp_directory(self, downloader):
        # Create a dummy file in temp directory
        test_file = os.path.join(downloader.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")

        downloader.cleanup()
        assert not os.path.exists(downloader.temp_dir)

    def test_invalid_url_raises_error(self, downloader):
        with pytest.raises(ValueError):
            downloader.download_video("invalid_url") 