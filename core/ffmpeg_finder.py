import os
import shutil
import sys
from pathlib import Path


class FFmpegFinder:
    def __init__(self, config):
        self.config = config

    def find_ffmpeg(self):
        saved_path = self.config.get_ffmpeg_path()
        if saved_path:
            ffmpeg_exe = self._get_ffmpeg_exe(saved_path)
            if ffmpeg_exe:
                return ffmpeg_exe

        ffmpeg_in_path = shutil.which("ffmpeg")
        if ffmpeg_in_path:
            self.config.set_ffmpeg_path(os.path.dirname(ffmpeg_in_path))
            return ffmpeg_in_path

        common_paths = self._get_common_paths()
        for path in common_paths:
            ffmpeg_exe = self._get_ffmpeg_exe(path)
            if ffmpeg_exe:
                self.config.set_ffmpeg_path(path)
                return ffmpeg_exe

        return self._ask_user_for_ffmpeg()

    def _get_ffmpeg_exe(self, base_path):
        base = Path(base_path)

        if base.is_file() and base.name.startswith("ffmpeg"):
            return str(base.resolve())

        exe_path = base / "bin" / "ffmpeg.exe"
        if exe_path.exists():
            return str(exe_path.resolve())

        bin_path = base / "bin" / "ffmpeg"
        if bin_path.exists():
            return str(bin_path.resolve())

        direct_exe = base / "ffmpeg.exe"
        if direct_exe.exists():
            return str(direct_exe.resolve())

        direct_bin = base / "ffmpeg"
        if direct_bin.exists():
            return str(direct_bin.resolve())

        return None

    def _get_common_paths(self):
        paths = []

        if sys.platform == "win32":
            program_files = os.environ.get("PROGRAMFILES", "C:\\Program Files")
            program_files_x86 = os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)")
            local_appdata = os.environ.get("LOCALAPPDATA", "")

            paths.extend([
                Path(program_files) / "ffmpeg",
                Path(program_files) / "FFmpeg",
                Path(program_files_x86) / "ffmpeg",
                Path(program_files_x86) / "FFmpeg",
                Path(local_appdata) / "ffmpeg" if local_appdata else None,
                Path("C:\\ffmpeg"),
                Path("C:\\FFmpeg"),
                Path.home() / "ffmpeg",
            ])
        else:
            paths.extend([
                Path("/usr/local/bin"),
                Path("/usr/bin"),
                Path("/opt/ffmpeg"),
                Path("/opt/homebrew/bin"),
                Path.home() / ".local" / "bin",
                Path.home() / "ffmpeg",
            ])

        return [p for p in paths if p and p.exists()]

    def _ask_user_for_ffmpeg(self):
        print("-" * 60)
        print("FFmpeg was not found automatically on your system.")
        print("FFmpeg is required for merging video/audio and MP3 conversion.")
        print()
        print("Please enter the path to your FFmpeg installation.")
        print("Examples:")
        print('  Windows: C:\\ffmpeg  (where ffmpeg.exe is in C:\\ffmpeg\\bin)')
        print('  Windows: C:\\ffmpeg\\bin\\ffmpeg.exe')
        print('  Linux/Mac: /usr/bin/ffmpeg')
        print('  Linux/Mac: /opt/ffmpeg')
        print()

        while True:
            user_path = input("Enter FFmpeg path (or 'q' to quit): ").strip().strip('"').strip("'")

            if user_path.lower() == 'q':
                return None

            if not user_path:
                print("[ERROR] Path cannot be empty. Please try again.")
                continue

            ffmpeg_exe = self._get_ffmpeg_exe(user_path)
            if ffmpeg_exe:
                print(f"[INFO] FFmpeg found: {ffmpeg_exe}")
                base = Path(user_path)
                if base.is_file():
                    self.config.set_ffmpeg_path(str(base.parent))
                else:
                    self.config.set_ffmpeg_path(user_path)
                return ffmpeg_exe
            else:
                print(f"[ERROR] Could not find ffmpeg executable in: {user_path}")
                print("Please make sure the path is correct and try again.")
                print()
