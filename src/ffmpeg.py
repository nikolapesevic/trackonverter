import shutil
import sys
import output

ffmpeg_path = shutil.which("ffmpeg")
ffprobe_path = shutil.which("ffprobe")

if ffmpeg_path and ffprobe_path:
	output.success("FFmpeg is installed and found on your system.")
else:
	output.error("FFmpeg is not installed or not found on your system.")
	output.info("FFmpeg is required for audio processing. Please download and install FFmpeg from: https://ffmpeg.org/download.html.\n Start the program again after installing FFmpeg.")
	sys.exit(1)