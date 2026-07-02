import os
import json
from pathlib import Path


class ConfigManager:
    CONFIG_FILE = "config.json"
    DEFAULT_OUTPUT_DIR = "downloads"

    def __init__(self):
        self.config_path = Path(self.CONFIG_FILE)
        self.config = self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "output_dir": self.DEFAULT_OUTPUT_DIR,
            "ffmpeg_path": None,
            "default_format": "mp4",
            "default_quality": "best"
        }

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"[WARNING] Could not save config: {e}")

    def get_output_dir(self):
        output_dir = self.config.get("output_dir", self.DEFAULT_OUTPUT_DIR)
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return str(path.resolve())

    def set_output_dir(self, output_dir):
        self.config["output_dir"] = output_dir
        self.save_config()

    def get_ffmpeg_path(self):
        path = self.config.get("ffmpeg_path")
        if path and Path(path).exists():
            return path
        return None

    def set_ffmpeg_path(self, path):
        self.config["ffmpeg_path"] = path
        self.save_config()

    def get_default_format(self):
        return self.config.get("default_format", "mp4")

    def get_default_quality(self):
        return self.config.get("default_quality", "best")
