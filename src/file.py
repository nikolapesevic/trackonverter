from pathlib import Path
import output
import ffmpeg
import subprocess
import os

def shorten_filename(filename: str, max_length: int = 60) -> str:
	if len(filename) <= max_length:
		return filename

	name, ext = os.path.splitext(filename)
	
	# Reserve space for "... " (4 chars) + extension
	available_length = max_length - 4 - len(ext)
	
	if available_length <= 0:
		return f"...{ext}"
	
	# Shorten the name and add ellipsis with extension
	shortened_name = name[:available_length]
	return f"{shortened_name}... {ext}"


def is_audio_file(filepath: str) -> bool:
	try:
		result = subprocess.run(
			[ffmpeg.ffprobe_path, "-v", "error", "-select_streams", "a:0",
			 "-show_entries", "stream=codec_type", "-of", "csv=p=0", filepath],
			capture_output=True, text=True, check=True
		)
		return "audio" in result.stdout
	except subprocess.CalledProcessError:
		return False

def get_audio_paths(input_path: Path) -> list[Path]:
	audio_paths = []

	if not input_path.exists():
		output.error(f"'{str(input_path)}' does not exist.")
		return audio_paths

	if not input_path.is_dir():
		output.error(f"'{str(input_path)}' is not a directory.")
		return audio_paths

	for current_dir, _, file_names in input_path.walk():
		for file_name in file_names:
			if is_audio_file(str(current_dir / file_name)):
				audio_paths.append(Path(str(current_dir / file_name)))

	return audio_paths
