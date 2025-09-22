import audio
from pathlib import Path
import converters.mp3

class TrackConverter:
	def __init__(self, input: str):
		self.input = Path(input)
		self.output_parent = self.input.parent

		self.mp3_converter = converters.mp3.MP3Converter()

	def run(self) -> None:
		for audio_path in audio.get_audio_paths(self.input):	
			relative_path = audio_path.relative_to(self.input)
			output_path = self.output_parent / (self.input.name + "_" + converters.mp3.EXTENSION) / relative_path.with_suffix("." + converters.mp3.EXTENSION)
			output_path.parent.mkdir(parents=True, exist_ok=True)
			
			self.mp3_converter.convert(str(audio_path), str(output_path))