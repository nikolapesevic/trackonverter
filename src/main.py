#!/usr/bin/env python3

import sys
import os
import subprocess
import output
import ffmpeg
from pathlib import Path
from track_converter import TrackConverter

DEFAULT_FOLDER = "tracks"

# Allow running terminal from macOS app bundle with the right cwd
def is_app_bundle():
	return getattr(sys, 'frozen', False) and '.app/Contents/MacOS' in sys.executable

def launch_in_terminal():
	script_path = sys.executable
	app_parent_dir = str(Path(script_path).parents[3])
	applescript = f'''
	tell application "Terminal"
		activate
		do script "clear && cd '{app_parent_dir}' && '{script_path}'"
	end tell
	'''
	subprocess.run(['osascript', '-e', applescript])

def main():
	print(os.getcwd())

	# If running from app bundle and no terminal is attached, launch in Terminal
	if is_app_bundle() and not sys.stdin.isatty() and '--terminal' not in sys.argv:
		launch_in_terminal()
		return
		
	if ffmpeg.ensure():
		try: 
			args = sys.argv
			user_path = None
			if len(args) == 2:
				user_path = args[1]
			else:
				user_path = output.prompt("Drag a folder into this window or type the path and press ➡️  Enter.", DEFAULT_FOLDER)
				if os.path.isdir(user_path):
					output.info("Using input folder: " + user_path)
				else:
					output.error(f"No input folder specified and no '{DEFAULT_FOLDER}' folder found in current directory")

			track_converter = TrackConverter(user_path)
			track_converter.additional_converters = ["aiff"]
			track_converter.run()
		except KeyboardInterrupt:
			output.info("Interupted by user")
		except Exception as e:
			output.error(f"Unexpected error - {e}")

	output.wait_for_key()


if __name__ == "__main__":
	main()