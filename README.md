# Speaker Diarization Tools
Command line tool for running some pre-trained [pyannote.audio](https://github.com/pyannote/pyannote-audio) models and saving their output to text files. Use `dia_tools.py` with various arguments to run specific models on audio files.

### Usage
For details on arguments run `$ python3 dia_tools.py -h`:

```
usage: dia_tools.py [-h] [--outfile [OUTFILE]] [--model [MODEL]]
                    method audio_file audio_uri

positional arguments:
  method               Name of method to be applied to audio. Options are
                       'ovl', for overlapped speech detection, and 'dia', for
                       speaker diarization.
  audio_file           Path to .wav audio file to be processed.
  audio_uri            Unique identifier for audio file.

optional arguments:
  -h, --help           show this help message and exit
  --outfile [OUTFILE]  Path & filename for output file. By default, output
                       file will be given the same name as the input .wav
                       file, but with a .ovl.txt or .dia.txt extension
                       depending on the chosen method.
  --model [MODEL]      Name of pretrained model to be used. Options are 'ami'
                       and 'dihard'. Default is 'dihard'. See pyannote.audio
                       for more detail on these models.
```

### Output Files
By default, output files will have the same name as the input `.wav` file, but with the extension `.ovl.txt` or `.dia.txt`, depending on the task being executed (e.g. `C0051.wav` --> `C0051.ovl.txt`). Alternatively, an output file path can be specified using the argument `--outfile` (see above).


Output files are formatted as follows:

**Overlapped speech detection output (`.ovl.txt`)**
```
<audio_id> <NA> <NA> <overlapped_speech_segment_start> <overlapped_speech_segment_start> <NA>
```
In this case, `<NA>` stands for _not applicable_ to the task of overlapped speech detection.

**Speaker diarization output (`.dia.txt`)**
```
<audio_id> <headphone_id> <speaker_id> <speech_segment_start> <speech_segment_end> <speech_transcription>
```
`<headphone_id>` and `<speech_transcription>` are not predicted by the models currently used, and so they are simply replaced with the dummy text `<headphone>` and `<text>` respectively.
