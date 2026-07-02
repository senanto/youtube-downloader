import os
import sys


class CLI:
    def __init__(self, downloader):
        self.downloader = downloader

    def run(self):
        while True:
            self._show_main_menu()
            choice = input("Select option: ").strip()

            if choice == '1':
                self._download_video_flow()
            elif choice == '2':
                self._download_audio_flow()
            elif choice == '3':
                self._change_output_dir()
            elif choice == '4':
                self._show_about()
            elif choice == '0':
                print("\nGoodbye!")
                break
            else:
                print("[ERROR] Invalid option. Please try again.\n")

    def _show_main_menu(self):
        print()
        print("-" * 60)
        print("  MAIN MENU")
        print("-" * 60)
        print("  [1] Download Video (MP4)")
        print("  [2] Download Audio (MP3)")
        print("  [3] Change Output Directory")
        print("  [4] About")
        print("  [0] Exit")
        print("-" * 60)

    def _get_url(self):
        url = input("Enter YouTube URL: ").strip()
        if not url:
            print("[ERROR] URL cannot be empty.")
            return None
        if not ('youtube.com' in url or 'youtu.be' in url):
            print("[WARNING] This doesn't look like a YouTube URL. Proceeding anyway...")
        return url

    def _show_video_quality_menu(self):
        print()
        print("  Select Video Quality:")
        print("  [1] 144p   (lowest, smallest file)")
        print("  [2] 360p")
        print("  [3] 480p")
        print("  [4] 720p   (HD)")
        print("  [5] 1080p  (Full HD)")
        print("  [6] 1440p  (2K)")
        print("  [7] 2160p  (4K)")
        print("  [8] Best Available (default)")

    def _show_audio_quality_menu(self):
        print()
        print("  Select Audio Quality:")
        print("  [1] 128 kbps (smaller file)")
        print("  [2] 192 kbps")
        print("  [3] 256 kbps")
        print("  [4] 320 kbps (highest quality)")
        print("  [5] Best Available (default)")

    def _ask_include_audio(self):
        print()
        print("  Do you want to import sounds?")
        print("  [Y] Yes (default)")
        print("  [N] No (video only, no audio)")
        choice = input("  Your choice [Y/n]: ").strip().lower()
        if choice == 'n':
            return False
        return True

    def _download_video_flow(self):
        url = self._get_url()
        if not url:
            return

        print("\n[INFO] Fetching video information...")
        info = self.downloader.get_video_info(url)
        if info:
            print(f"  Title:    {info['title']}")
            print(f"  Channel:  {info['uploader']}")
            duration = info['duration']
            if duration:
                mins, secs = divmod(duration, 60)
                print(f"  Duration: {mins}:{secs:02d}")
            print()

        include_audio = self._ask_include_audio()

        self._show_video_quality_menu()
        quality = input("Select quality [1-8, default=8]: ").strip() or '8'
        if quality not in self.downloader.VIDEO_QUALITIES:
            print("[INFO] Invalid choice, using Best Available.")
            quality = '8'

        print()
        success = self.downloader.download_video(url, quality, 'mp4', include_audio)
        if success:
            print(f"\n[SAVED] File saved to: {self.downloader.output_dir}")
        else:
            print("\n[FAILED] Download could not be completed.")

    def _download_audio_flow(self):
        url = self._get_url()
        if not url:
            return

        print("\n[INFO] Fetching video information...")
        info = self.downloader.get_video_info(url)
        if info:
            print(f"  Title:    {info['title']}")
            print(f"  Channel:  {info['uploader']}")
            duration = info['duration']
            if duration:
                mins, secs = divmod(duration, 60)
                print(f"  Duration: {mins}:{secs:02d}")
            print()

        self._show_audio_quality_menu()
        quality = input("Select quality [1-5, default=5]: ").strip() or '5'
        if quality not in self.downloader.AUDIO_QUALITIES:
            print("[INFO] Invalid choice, using Best Available.")
            quality = '5'

        print()
        success = self.downloader.download_audio(url, quality)
        if success:
            print(f"\n[SAVED] File saved to: {self.downloader.output_dir}")
        else:
            print("\n[FAILED] Download could not be completed.")

    def _change_output_dir(self):
        current = self.downloader.output_dir
        print(f"\nCurrent output directory: {current}")
        new_dir = input("Enter new output directory (or press Enter to keep current): ").strip()

        if new_dir:
            try:
                os.makedirs(new_dir, exist_ok=True)
                self.downloader.config.set_output_dir(new_dir)
                self.downloader.output_dir = new_dir
                print(f"[OK] Output directory changed to: {new_dir}")
            except OSError as e:
                print(f"[ERROR] Could not create directory: {e}")
        else:
            print("[INFO] Keeping current directory.")

    def _show_about(self):
        print()
        print("=" * 60)
        print("  YouTube Downloader")
        print("=" * 60)
        print("  A Python-based YouTube video and audio downloader.")
        print()
        print("  Features:")
        print("    - Download videos in MP4 format (144p to 4K)")
        print("    - Download audio in MP3 format (128k to 320k)")
        print("    - Optional audio inclusion for video downloads")
        print("    - Automatic FFmpeg detection")
        print("    - Progress tracking")
        print()
        print("  Requirements:")
        print("    - Python 3.8+")
        print("    - yt-dlp (pip install yt-dlp)")
        print("    - FFmpeg (for merging and conversion)")
        print("=" * 60)
