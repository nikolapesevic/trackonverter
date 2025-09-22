#!/usr/bin/env python3

import sys
import os
import output
from track_converter import TrackConverter

DEFAULT_FOLDER = "tracks"

def main():
	args = sys.argv

	user_path = None
	if len(args) == 2:
			user_path = args[1]
	else:
		user_path = output.prompt("Drag a folder into this window or type the path and press Enter", DEFAULT_FOLDER)
		if os.path.isdir(user_path):
			output.info("Using input folder: " + user_path)
		else:
			output.error(f"No input folder specified and no '{DEFAULT_FOLDER}' folder found in current directory")
			sys.exit(1)

	track_converter = TrackConverter(user_path)

	# Optional parameters can be set here before running

	track_converter.run()


if __name__ == "__main__":
	main()