from .base import BaseConverter

import ffmpeg
from mutagen.aiff import AIFF
from mutagen.id3 import TIT2, TPE1, TALB, TCON, TRCK, TYER, APIC
from mutagen.mp3 import MP3

class AIFFConverter(BaseConverter):
	def __init__(self):
		super().__init__()

		self.extension = "aiff"
		self.sample_rate = 44100
		self.sample_format = "s16"
		self.codec = "pcm_s16be"

	def _convert_metadata(self, mp3_path: str, aiff_path: str) -> None:
		mp3 = MP3(mp3_path)
		aiff = AIFF(aiff_path)

		# Clear existing tags and make sure tags exist
		if aiff.tags is None:
			aiff.add_tags()
		aiff.tags.clear()

		# Copy basic metadata
		metadata_mapping = {
			'TIT2': ('title', TIT2),
			'TPE1': ('artist', TPE1),
			'TALB': ('album', TALB),
			'TCON': ('genre', TCON),
			'TRCK': ('track', TRCK),
			'TYER': ('year', TYER)
		}

		def get_id3_text(tag_name: str) -> str:
			if tag_name in mp3.tags:
				tag = mp3.tags[tag_name]
				if hasattr(tag, 'text') and tag.text:
					return str(tag.text[0])
			return None

		for tag_name, (_, tag_class) in metadata_mapping.items():
			value = get_id3_text(tag_name)
			if value:
				if tag_name == 'TYER' and len(value) > 4:
					value = value[:4]
				aiff.tags.add(tag_class(encoding=self._id3_encoding, text=value))

		if hasattr(mp3.tags, 'getall'):
			apics = mp3.tags.getall('APIC')
			if apics:
				apic = apics[0]
				aiff.tags.add(APIC(
					encoding=self._id3_encoding,
					mime=apic.mime,
					type=3,  # Cover (front)
					desc="Cover",
					data=apic.data
				))
			
		aiff.save(v2_version=self._id3_version)


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
			
		self._convert_metadata(self._get_mp3_path(input), output)
