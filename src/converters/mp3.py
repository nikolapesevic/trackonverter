from . import base
import ffmpeg
import subprocess

EXTENSION = "mp3"
SAMPLE_RATE = 44100
SAMPLE_FORMAT = "s16p"
CODEC = "libmp3lame"
BITRATE = "320k"

class MP3Converter(base.BaseConverter):
	def convert(self, input: str, output: str) -> None:
		command = [
			ffmpeg.ffmpeg_path, "-y", "-i", input,
			"-map_metadata", "0", "-map", "0",
			"-ar", str(SAMPLE_RATE),
			"-sample_fmt", SAMPLE_FORMAT,
			"-c:a", CODEC,
			"-b:a", BITRATE,
			"-id3v2_version", str(base.ID3_VERSION),
			output,
			"-loglevel", base.FFMPEG_LOG_LEVEL
		]
		subprocess.run(command, check=True)