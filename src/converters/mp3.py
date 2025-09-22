from .base import BaseConverter
import ffmpeg
import subprocess

class MP3Converter(BaseConverter):
	def __init__(self):
		super().__init__()

		self.extension = "mp3"
		self.sample_rate = 44100
		self.sample_format = "s16p"
		self.codec = "libmp3lame"
		self.bitrate = "320k"

	def convert(self, input: str, output: str) -> None:
		self._run([
			ffmpeg.ffmpeg_path, "-y", "-i", input,
			"-map_metadata", "0", "-map", "0",
			"-ar", str(self.sample_rate),
			"-sample_fmt", self.sample_format,
			"-c:a", self.codec,
			"-b:a", self.bitrate,
			"-id3v2_version", str(self._id3_version),
			output,
			"-loglevel", self._ffmpeg_log_level
		])