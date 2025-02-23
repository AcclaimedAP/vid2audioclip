import argparse
import sys
from typing import Optional
from .youtube_downloader import YoutubeDownloader
from .audio_processor import AudioProcessor
from .file_saver import FileSaver

class AudioExtractorCLI:
    def __init__(self):
        self.downloader = YoutubeDownloader()
        self.file_saver = FileSaver()
        
    def run(self):
        try:
            # Get YouTube URL
            url = self._get_input("Enter YouTube URL: ")
            print("Downloading video...")
            video_path = self.downloader.download_video(url)
            
            # Process audio
            print("Processing audio...")
            processor = AudioProcessor(video_path)
            start = None
            end = None
            while True:
                if start is None:
                    # Get time range (now using time format)
                    start = self._get_input("Enter start time (e.g., 1:30 or 1:30.5): ")
                    end = self._get_input("Enter end time (e.g., 2:45 or 2:45.5): ")

                    try:
                        processor.set_time_range(start, end)
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                
                # Preview
                print("\nPlaying preview...")
                processor.play_preview()
                
                # Ask if they want to adjust
                if self._get_input("\nDo you want to adjust the time range? (y/n): ").lower() != 'y':
                    break
                # Get adjustments (now using time format)
                start_adj = self._get_input("Enter start time adjustment (e.g., 0:05 or -0:05): ")
                end_adj = self._get_input("Enter end time adjustment (e.g., 0:05 or -0:05): ")
                
                try:
                    processor.adjust_time_range(start_adj, end_adj)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            
            # Volume adjustment
            if self._get_input("\nDo you want to adjust volume? (y/n): ").lower() == 'y':
                db_change = float(self._get_input("Enter volume adjustment in dB (positive or negative): "))
                processor.adjust_volume(db_change)
            
            # Save file
            output_path = self._get_input("\nEnter output file path (e.g., output.mp3): ")
            print("Saving audio...")
            self.file_saver.save_audio(processor.get_audio_segment(), output_path)
            print(f"\nAudio saved to: {output_path}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.downloader.cleanup()
    
    def _get_input(self, prompt: str) -> str:
        """Helper method to get input from user."""
        return input(prompt).strip()

def main():
    cli = AudioExtractorCLI()
    cli.run()

if __name__ == "__main__":
    main() 