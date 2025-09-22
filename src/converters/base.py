from pathlib import Path
from abc import ABC, abstractmethod
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

	def _run(self, command: list[str]) -> None:
		try:
			subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
		except subprocess.CalledProcessError as e:
			# Capture ffmpeg error output and raise with meaningful message
			error_msg = e.stderr.strip() if e.stderr else f"Command failed with exit code {e.returncode}"
			raise RuntimeError(f"FFmpeg conversion failed: {error_msg}") from e

	@abstractmethod
	def convert(self) -> None:
		pass