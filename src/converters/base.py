from pathlib import Path
from abc import ABC, abstractmethod

# FFmpeg configuration
FFMPEG_LOG_LEVEL = "error"

# Metadata configuration
ID3_VERSION = 3
ID3_ENCODING = 3

class BaseConverter(ABC):
	@abstractmethod
	def convert(self, audio: Path, output_root: Path) -> None:
		pass