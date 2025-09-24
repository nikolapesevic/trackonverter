# Trackonverter
Convert audio files to MP3 and AIFF formats while preserving metadata and directory structure in the best supported formats for Pioneer DJ software/hardware.

### Features
- Convert various audio formats to MP3 and AIFF (Any input format that [ffmpeg](https://ffmpeg.org/) supports)
- Preserves metadata (ID3 tags, album art, etc.) during conversion
- Multithreaded conversion for faster processing
- Mirrors nested directory structure and file names in the output directory
- Skips conversion if the output file already exists and is identical

### Exported Formats
The input tracks are exported in the following formats:

| Format | Sample Rate | Bitrate | Bit Depth | Codec | Extension |
|---|---|---|---|---|---|
|MP3 | 44100Hz | 320kbps CBR  | N/A   | libmp3lame | .mp3  |
|AIFF| 44100Hz | 1411kbps CBR | 16bit | pcm_s16be  | .aiff |

These formats are chosen for their wide compatibility with Pioneer DJ software and hardware while also preserving metadata effectively.

### Caveats
1. **Obviously, the input tracks are required to already have metadata and be in a lossless format for AIFF to make sense.**
2. AIFF can go up to 24bit, but certain Pioneer DJ gear only supports 16bit, hence the 16bit limitation.
3. Certain metadata fields may not be perfectly preserved due to format limitations, we try our best to map them correctly.
4. MP3s have to be generated, as they are used to extract metadata from the input tracks. *It's much more convenient to convert metadata from MP3 -> AIFF than any format -> AIFF directly.*
5. Already existing converted files will be skipped, but no checks are made if the file is actually identical for performance reasons. If you want to re-convert, delete the output folders first.

## Usage
Trackonverter depends on [ffmpeg](https://ffmpeg.org/) to handle audio conversion. Make sure ffmpeg is installed and accessible in your system's PATH. You will be prompted to manually download and install ffmpeg if it is not found.

### 1. Download and Run
If you just want to use the app, download the latest release from the [Releases](https://github.com/nikolapesevic/trackonverter/releases) page:

**Windows**: Download `trackonverter-windows.exe` and double-click to run.

**macOS**: Download `trackonverter-macos.zip`, extract it, and double-click `Trackonverter.app` to run. 
- On first run, macOS may show a security warning. Go to System Preferences → Security & Privacy and click "Open Anyway"

### 2. Track Selection
There is a plethora of ways you can run Trackonverter on a specific folder:
1. Drag and drop a folder onto the program (Windows).
2. Open the program and drag n' drop a folder into the terminal window, then press Enter.
3. Open the program and paste or type a folder path into the terminal window. *The default is tracks, so you can also just place the program next to a folder named tracks.*
4. Run the program through the terminal and provide the folder path as an argument, e.g. `./trackonverter "~/Documents/tracks"`.

### 3. Conversion
Once you provide a valid folder path, the conversion will start automatically. You will see progress bars indicating the conversion status of each file and overall progress.

### 4. Output
In the same folder where the input folder is located, new folders will appear with the input folders name and _mp3 or _aiff suffixes, containing the converted files in the same directory structure as the input folder.

## Development 
### Running from source
0. Ensure you have Python 3.13 or higher, [Poetry](https://python-poetry.org/docs/#installation) and [ffmpeg](https://ffmpeg.org/download.html) installed and accessible in your system's PATH.
1. Clone the repository.
2. Run `poetry install` to install dependencies.
3. Run `poetry run python src/main.py` to start the application. *VSCode users can also use `Run Task -> Run.`*

### Building the executables
1. Push a version tag to GitHub and the action will run the build process.