import os
import shutil
import tempfile
from pytubefix import YouTube
from urllib.parse import urlparse, parse_qs

class YoutubeDownloader:
    def __init__(self):
        """Initialize the downloader with a temporary directory."""
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'youtube_temp')
        os.makedirs(self.temp_dir, exist_ok=True)

    def download_video(self, url: str) -> str:
        """
        Download a video from YouTube and save it to the temporary directory.
        
        Args:
            url (str): The YouTube video URL
            
        Returns:
            str: Path to the downloaded video file
            
        Raises:
            ValueError: If the URL is invalid
        """
        if not self._is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL")

        try:
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension='mp4').first()
            return video.download(output_path=self.temp_dir)
        except Exception as e:
            raise ValueError(f"Failed to download video: {str(e)}")

    def cleanup(self):
        """Remove the temporary directory and all its contents."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _is_valid_youtube_url(self, url: str) -> bool:
        """Validate if the given URL is a valid YouTube URL."""
        try:
            parsed_url = urlparse(url)
            return all([
                parsed_url.netloc in ['youtube.com', 'www.youtube.com', 'youtu.be'],
                parsed_url.scheme in ['http', 'https']
            ])
        except:
            return False

    def __del__(self):
        """Ensure cleanup is called when the object is destroyed."""
        self.cleanup() 