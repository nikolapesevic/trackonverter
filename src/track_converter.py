import file
import os
import output
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, MofNCompleteColumn, SpinnerColumn

import converters.base
import converters.mp3
import converters.aiff


MAX_WORKERS = 8

class TrackConverter:
	def __init__(self, input: str) -> None:
		self._converters = {
			"mp3": converters.mp3.MP3Converter(),
			"aiff": converters.aiff.AIFFConverter()
		}

		self.additional_converters = {} # Other than mp3, by extension/converter name from above

		self.input = Path(input)
		self.output_parent = self.input.parent


	def _convert_single_file(self, audio_path: Path, converter: converters.base.BaseConverter) -> tuple[Path, bool]: # Returns true if skipped
		# Figure out the proper output path and ensure it exists
		relative_path = audio_path.relative_to(self.input)
		output_path = self.output_parent / (self.input.name + "_" + converter.extension) / relative_path.with_suffix("." + converter.extension)
		output_path.parent.mkdir(parents=True, exist_ok=True)

		# Skip if output exists (we assume it's identical, otherwise it would cost the same to check)
		if output_path.exists():
			return output_path, True
		
		converter.convert(str(audio_path), str(output_path))
		return output_path, False

	def _convert_parallel(self, audio_paths: list[Path], converter: converters.base.BaseConverter, callback) -> tuple[dict[str, str], list[str]]:
		max_workers = min(os.cpu_count(), MAX_WORKERS)
		conversion_errors = []
		skipped_files = []
		converted_files = {}

		with Progress(
			TextColumn("[progress.description]{task.description}"),
			BarColumn(complete_style="green"),
			MofNCompleteColumn(),
		) as progress:
			task_id = progress.add_task(f"Converting to {str.upper(converter.extension)}", total=len(audio_paths))

			with ThreadPoolExecutor(max_workers=max_workers) as executor:
				file_progress = Progress(
					SpinnerColumn(),
					TextColumn("[progress.description]{task.description}")
				)
				file_progress.start()
				file_progress_tasks = {}

				future_to_path = {}
				for input_path in audio_paths:
					file_progress_tasks[input_path] = file_progress.add_task(file.shorten_filename(input_path.with_suffix("").name + "." + converter.extension), total=None)

					future = executor.submit(self._convert_single_file, input_path, converter)
					future_to_path[future] = input_path
				
				for future in as_completed(future_to_path.keys()):
					audio_path = future_to_path[future]

					try:
						result, skipped = future.result()
					except Exception as e:
						conversion_errors.append((audio_path, str(e)))
					else: 
						converted_files[str(audio_path)] = str(result)
						if skipped:
							skipped_files.append(str(audio_path))
					finally:
						file_progress.remove_task(file_progress_tasks[audio_path])
						progress.advance(task_id)
						callback()

				file_progress.stop()
			progress.remove_task(task_id)

		# Display any errors that occurred after progress is complete
		for audio_path, error_msg in conversion_errors:
			output.warn(f"Could not convert {audio_path}")
			output.error(error_msg)

		return converted_files, skipped_files


	def run(self) -> None:
		with Progress() as progress:
			read_task = progress.add_task("Reading audio files", total=None)
			audio_paths = file.get_audio_paths(self.input)
			progress.remove_task(read_task)

		def convert_format(converter: converters.base.BaseConverter, callback) -> dict[str, str]: # Input -> Output audio paths for each succesful conversion
			converted, skipped = self._convert_parallel(audio_paths=audio_paths, converter=self._converters[converter.extension], callback=callback)
			
			# Report skipped files
			if skipped:
				output.info(f"Skipped {len(skipped)} tracks because they are identical.")

			if len(converted) == len(audio_paths):
				output.success(f"All {len(audio_paths)} tracks converted to {str.upper(converter.extension)} successfully!")
			else:
				output.info(f"{len(audio_paths) - len(converted)} tracks could not be converted to {str.upper(converter.extension)}. See above for details.")
			
			return converted
		
		with Progress(
			TextColumn("[progress.description]{task.description}"),
			BarColumn(complete_style="green"),
			MofNCompleteColumn(),
			TimeRemainingColumn(),
		) as progress:
			output.console = progress.console # Use main progress console for output to keep things tidy
			task_id = progress.add_task("Converting tracks", total=(len(self.additional_converters) + 1) * len(audio_paths))
			
			def file_completed():
				progress.advance(task_id)

			mp3_converted = convert_format(self._converters["mp3"], file_completed) # Always convert to mp3 (necessary for other formats)

			# Convert all other formats
			for converter_name in self.additional_converters:
				converter = self._converters.get(converter_name)
				if converter:
					converter.mp3_paths = mp3_converted
					convert_format(converter, file_completed)
					progress.update(task_id, advance=len(audio_paths))
				else:
					output.error(f"Unknown converter {str.upper(converter.extension)}.")

			progress.remove_task(task_id)
			progress.stop()

