import file
import converters.base
import converters.mp3
import converters.aiff
import os
import output

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress

MAX_WORKERS = 8

class TrackConverter:
	def __init__(self, input: str) -> None:
		self._converters = {
			"mp3": converters.mp3.MP3Converter(),
			"aiff": converters.aiff.AIFFConverter()
		}

		self.enabled_converters = {}
		self.enabled_converters["mp3"] = True
		self.enabled_converters["aiff"] = False
		self.enabled_converters["wav"] = False
		self.enabled_converters["flac"] = False

		self.input = Path(input)
		self.output_parent = self.input.parent


	def _convert_single_file(self, audio_path: Path, converter: converters.base.BaseConverter) -> Path:
		# Figure out the proper output path and ensure it exists
		relative_path = audio_path.relative_to(self.input)
		output_path = self.output_parent / (self.input.name + "_" + converter.extension) / relative_path.with_suffix("." + converter.extension)
		output_path.parent.mkdir(parents=True, exist_ok=True)
		
		converter.convert(str(audio_path), str(output_path))
		return output_path

	def _convert_parallel(self, audio_paths: list[Path], converter: converters.base.BaseConverter) -> int:
		max_workers = min(os.cpu_count(), MAX_WORKERS)
		conversion_errors = []

		with Progress() as progress:
			task_id = progress.add_task(f"Converting to {str.upper(converter.extension)}", total=len(audio_paths))

			with ThreadPoolExecutor(max_workers=max_workers) as executor:
				file_progress = Progress()
				file_progress.start()
				file_progress_tasks = {}

				future_to_path = {}
				for audio_path in audio_paths:
					file_progress_tasks[audio_path] = file_progress.add_task(file.shorten_filename(audio_path.with_suffix("").name + "." + converter.extension), total=None)
					
					future = executor.submit(self._convert_single_file, audio_path, converter)
					future_to_path[future] = audio_path
				
				for future in as_completed(future_to_path.keys()):
					try:
						future.result()
					except Exception as e:
						audio_path = future_to_path[future]
						conversion_errors.append((audio_path, str(e)))
					finally:
						audio_path = future_to_path[future]
						file_progress.remove_task(file_progress_tasks[audio_path])
						progress.advance(task_id)

				file_progress.stop()
			progress.remove_task(task_id)

		# Display any errors that occurred after progress is complete
		for audio_path, error_msg in conversion_errors:
			output.warn(f"Could not convert {audio_path}")
			output.error(error_msg)

		return len(audio_paths) - len(conversion_errors)


	def run(self) -> None:
		with Progress() as progress:
			read_task = progress.add_task("Reading audio files", total=None)
			audio_paths = file.get_audio_paths(self.input)
			progress.remove_task(read_task)

		self.enabled_converters["mp3"] = True # Ensure mp3 is always enabled!

		for converter_name, enabled in self.enabled_converters.items():
			if enabled and converter_name in self._converters:
				converted_succesfully = self._convert_parallel(audio_paths=audio_paths, converter=self._converters[converter_name])
				if converted_succesfully == len(audio_paths):
					output.success(f"All files converted to {str.upper(converter_name)} successfully!")
				else:
					output.info(f"Some files could not be converted to {str.upper(converter_name)}. See above for details.")