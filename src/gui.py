import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .youtube_downloader import YoutubeDownloader
from .audio_processor import AudioProcessor
from .file_saver import FileSaver

class AudioExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Extractor")
        self.downloader = YoutubeDownloader()
        self.file_saver = FileSaver()
        self.processor = None
        
        # Create GUI elements
        self._create_widgets()
        
    def _create_widgets(self):
        # URL input
        url_frame = ttk.LabelFrame(self.root, text="YouTube URL", padding="5")
        url_frame.pack(fill="x", padx=5, pady=5)
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side="left", padx=5, expand=True, fill="x")
        
        ttk.Button(url_frame, text="Download", command=self._download_video).pack(side="right", padx=5)
        
        # Time range frame
        time_frame = ttk.LabelFrame(self.root, text="Time Range", padding="5")
        time_frame.pack(fill="x", padx=5, pady=5)
        
        # Start time
        ttk.Label(time_frame, text="Start (e.g., 1:30):").grid(row=0, column=0, padx=5)
        self.start_time = ttk.Entry(time_frame, width=10)
        self.start_time.grid(row=0, column=1, padx=5)
        
        # End time
        ttk.Label(time_frame, text="End (e.g., 2:45):").grid(row=0, column=2, padx=5)
        self.end_time = ttk.Entry(time_frame, width=10)
        self.end_time.grid(row=0, column=3, padx=5)
        
        # Preview button
        ttk.Button(time_frame, text="Preview", command=self._preview_audio).grid(row=0, column=4, padx=5)
        
        # Volume adjustment
        volume_frame = ttk.LabelFrame(self.root, text="Volume", padding="5")
        volume_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(volume_frame, text="Adjustment (dB):").pack(side="left", padx=5)
        self.volume_adj = ttk.Entry(volume_frame, width=10)
        self.volume_adj.pack(side="left", padx=5)
        ttk.Button(volume_frame, text="Apply", command=self._adjust_volume).pack(side="right", padx=5)
        
        # Save button
        ttk.Button(self.root, text="Save Audio", command=self._save_audio).pack(pady=10)
        
    def _download_video(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
                
            video_path = self.downloader.download_video(url)
            self.processor = AudioProcessor(video_path)
            messagebox.showinfo("Success", "Video downloaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _preview_audio(self):
        if not self.processor:
            messagebox.showerror("Error", "Please download a video first")
            return
            
        try:
            start = self.start_time.get().strip()
            end = self.end_time.get().strip()
            self.processor.set_time_range(start, end)
            self.processor.play_preview()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _adjust_volume(self):
        if not self.processor:
            messagebox.showerror("Error", "Please download a video first")
            return
            
        try:
            db_change = float(self.volume_adj.get())
            self.processor.adjust_volume(db_change)
            messagebox.showinfo("Success", "Volume adjusted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _save_audio(self):
        if not self.processor:
            messagebox.showerror("Error", "Please download a video first")
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[
                    ("MP3 files", "*.mp3"),
                    ("WAV files", "*.wav"),
                    ("OGG files", "*.ogg"),
                    ("M4A files", "*.m4a")
                ]
            )
            if file_path:
                self.file_saver.save_audio(self.processor.get_audio_segment(), file_path)
                messagebox.showinfo("Success", "Audio saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def __del__(self):
        self.downloader.cleanup()

def main():
    root = tk.Tk()
    app = AudioExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 