from pathlib import Path
from abc import ABC, abstractmethod

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

	@abstractmethod
	def convert(self) -> None:
		pass