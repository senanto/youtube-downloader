import os
import sys
import yt_dlp
from pathlib import Path


class YouTubeDownloader:
    VIDEO_QUALITIES = {
        '1': ('144p', 'worst[height<=144]'),
        '2': ('360p', 'best[height<=360]'),
        '3': ('480p', 'best[height<=480]'),
        '4': ('720p', 'best[height<=720]'),
        '5': ('1080p', 'best[height<=1080]'),
        '6': ('1440p (2K)', 'best[height<=1440]'),
        '7': ('2160p (4K)', 'best[height<=2160]'),
        '8': ('Best Available', 'bestvideo+bestaudio/best'),
    }

    AUDIO_QUALITIES = {
        '1': ('128 kbps', '192'),
        '2': ('192 kbps', '192'),
        '3': ('256 kbps', '256'),
        '4': ('320 kbps', '320'),
        '5': ('Best Available', '0'),
    }

    def __init__(self, ffmpeg_path, config):
        self.ffmpeg_path = ffmpeg_path
        self.config = config
        self.output_dir = config.get_output_dir()

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\r  Progress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n  [OK] Download complete: {Path(d['filename']).name}")

    def download_video(self, url, quality_choice='8', output_format='mp4', include_audio=True):
        quality_name, format_spec = self.VIDEO_QUALITIES.get(quality_choice, self.VIDEO_QUALITIES['8'])

        outtmpl = os.path.join(self.output_dir, '%(title)s [%(id)s].%(ext)s')

        if include_audio:
            ydl_opts = {
                'format': format_spec,
                'outtmpl': outtmpl,
                'merge_output_format': output_format,
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': False,
                'retries': 3,
                'fragment_retries': 3,
                'continuedl': True,
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]/bestvideo',
                'outtmpl': outtmpl,
                'merge_output_format': output_format,
                'ffmpeg_location': self.ffmpeg_path,
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': False,
                'retries': 3,
                'fragment_retries': 3,
                'continuedl': True,
            }

        if output_format == 'mp4':
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

        print(f"[INFO] Downloading video: {quality_name}")
        if include_audio:
            print("[INFO] Audio: INCLUDED")
        else:
            print("[INFO] Audio: MUTED (video only)")
        print(f"[INFO] Output format: {output_format.upper()}")
        print(f"[INFO] Output directory: {self.output_dir}")
        print()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n[SUCCESS] Downloaded: {title}")
                return True
        except yt_dlp.utils.DownloadError as e:
            print(f"\n[ERROR] Download failed: {e}")
            return False
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            return False

    def download_audio(self, url, quality_choice='5'):
        quality_name, bitrate = self.AUDIO_QUALITIES.get(quality_choice, self.AUDIO_QUALITIES['5'])

        outtmpl = os.path.join(self.output_dir, '%(title)s [%(id)s].%(ext)s')

        if bitrate == '0':
            preferredcodec = 'mp3'
            preferredquality = '0'
        else:
            preferredcodec = 'mp3'
            preferredquality = bitrate

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'ffmpeg_location': self.ffmpeg_path,
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': False,
            'retries': 3,
            'fragment_retries': 3,
            'continuedl': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': preferredcodec,
                'preferredquality': preferredquality,
            }],
        }

        print(f"[INFO] Downloading audio: {quality_name}")
        print("[INFO] Output format: MP3")
        print(f"[INFO] Output directory: {self.output_dir}")
        print()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n[SUCCESS] Downloaded MP3: {title}")
                return True
        except yt_dlp.utils.DownloadError as e:
            print(f"\n[ERROR] Download failed: {e}")
            return False
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
            return False

    def get_video_info(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else 'No description',
                }
        except Exception as e:
            print(f"[ERROR] Could not fetch video info: {e}")
            return None
