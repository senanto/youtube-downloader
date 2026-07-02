# YouTube Downloader

A modular Python YouTube downloader supporting MP4 (video) and MP3 (audio) output formats using `yt-dlp` and `FFmpeg`.

## Features

- **Video Downloads**: MP4 format with quality selection (144p to 4K)
- **Audio Downloads**: MP3 format with bitrate selection (128k to 320k)
- **Audio Toggle**: Choose whether to include or mute audio in video downloads
- **Auto FFmpeg Detection**: Automatically finds FFmpeg or prompts for path
- **Progress Tracking**: Real-time download progress display
- **Modular Architecture**: Clean separation of concerns across multiple files

## Requirements

- Python 3.8 or higher
- `yt-dlp` Python package
- FFmpeg binary (NOT the Python `ffmpeg` package)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and extract to `C:\ffmpeg` or add to PATH
   - **Linux**: `sudo apt install ffmpeg`
   - **Mac**: `brew install ffmpeg`

## Usage

Run the main script:
```bash
python main.py
```

The program will:
1. Search for FFmpeg automatically (common paths + PATH)
2. If not found, ask you to enter the path to your FFmpeg `bin` folder
3. Show the main menu for video/audio downloads

## Project Structure

```
youtube_downloader/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── config.json             # Saved settings (auto-generated)
├── downloads/              # Default output folder
├── core/
│   ├── __init__.py
│   ├── config_manager.py   # Settings management
│   ├── ffmpeg_finder.py    # FFmpeg auto-detection
│   └── downloader.py       # Download logic (yt-dlp)
└── ui/
    ├── __init__.py
    └── cli.py              # Command-line interface
```

## FFmpeg Path Examples

When prompted, enter one of these:

- **Windows** (if ffmpeg.exe is in `C:\ffmpeg\bin`):
  ```
  C:\ffmpeg
  ```
  or directly:
  ```
  C:\ffmpeg\bin\ffmpeg.exe
  ```

- **Linux/Mac**:
  ```
  /usr/bin/ffmpeg
  ```
  or:
  ```
  /opt/ffmpeg
  ```

## License

MIT License - For educational and personal use only.
