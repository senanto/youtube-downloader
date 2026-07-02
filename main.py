#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config_manager import ConfigManager
from core.ffmpeg_finder import FFmpegFinder
from core.downloader import YouTubeDownloader
from ui.cli import CLI


def main():
    print("=" * 60)
    print("   YouTube Downloader - MP4 & MP3")
    print("=" * 60)
    print()

    config = ConfigManager()

    ffmpeg_finder = FFmpegFinder(config)
    ffmpeg_path = ffmpeg_finder.find_ffmpeg()

    if not ffmpeg_path:
        print("[ERROR] FFmpeg is required but could not be found.")
        print("Please install FFmpeg or provide the correct path.")
        sys.exit(1)

    print(f"[INFO] Using FFmpeg: {ffmpeg_path}")
    print()

    downloader = YouTubeDownloader(ffmpeg_path, config)

    cli = CLI(downloader)
    cli.run()


if __name__ == "__main__":
    main()
