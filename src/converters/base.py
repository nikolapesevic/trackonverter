from pathlib import Path
from abc import ABC, abstractmethod
import file
import subprocess

class BaseConverter(ABC):
	def __init__(self):
		# Default settings (override in subclasses as needed)
		self._ffmpeg_log_level = "error"
		self._id3_version = 3
		self._id3_encoding = 3

		self.extension = ""
		self.sample_rate = 44100
		self.sample_format = ""
		self.codec = ""
		self.bitrate = ""

		# Needs to be specified for certain subclass converters
		self.mp3_paths = None

	def _get_mp3_path(self, input: str) -> str:
		if self.mp3_paths:
			mp3_path = self.mp3_paths.get(input)
			if mp3_path:
				return mp3_path
			else:
				raise RuntimeError("Missing MP3 file for converter that requires it.")
		else:
			raise RuntimeError("Missing MP3 path for converter that requires it.")

	def _run(self, command: list[str]) -> None:
		try:
			subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
		except subprocess.CalledProcessError as e:
			# Capture ffmpeg erroar output and raise with meaningful message
			error_msg = e.stderr.strip() if e.stderr else f"Command failed with exit code {e.returncode}"
			raise RuntimeError(f"FFmpeg conversion failed: {error_msg}") from e

	@abstractmethod
	def convert(self) -> None:
		pass