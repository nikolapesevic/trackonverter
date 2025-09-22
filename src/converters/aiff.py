from .base import BaseConverter
import ffmpeg

class AIFFConverter(BaseConverter):
	def __init__(self):
		super().__init__()

		self.extension = "aiff"
		self.sample_rate = 44100
		self.sample_format = "s16"
		self.codec = "pcm_s16be"

	def convert(self, input: str, output: str) -> None:
		self._run([
            ffmpeg.ffmpeg_path, "-y", "-i", input,
            "-map_metadata", "0", "-map", "0:a",
            "-ar", str(self.sample_rate),
            "-sample_fmt", self.sample_format,
            "-c:a", self.codec,
            output,
            "-loglevel", self._ffmpeg_log_level
		])