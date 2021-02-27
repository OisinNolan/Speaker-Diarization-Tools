import torch
import util

def get_overlapping_speech(audio_file, model_type):
    '''
    For a given audio file at path 'audio_file', and model type, which may be
    either 'ovl_ami' or 'ovl_dihard', calculate segments of speech containing
    overlapped speech.

    Segments returned as pyannote.core Timeline
    '''
    model = torch.hub.load('pyannote/pyannote-audio', model_type)
    ovl_scores = model({'audio': audio_file})

    # binarize raw OVL scores
    # NOTE: both onset/offset (decision threshold) values were tuned on AMI dataset.
    # We can change these values according to our needs
    from pyannote.audio.utils.signal import Binarize
    binarize = Binarize(offset=0.55, onset=0.55, log_scale=True, 
                        min_duration_off=0.1, min_duration_on=0.1)

    # overlapped speech regions (as `pyannote.core.Timeline` instance)
    overlap = binarize.apply(ovl_scores, dimension=1)
    return overlap

def output_ovl(uri, out_file, ovl_segments):
    '''
    Output overlapped speech segment info to a text file in the following format:
    <audio_id> <NA> <NA> <overlapped_speech_segment_start> <overlapped_speech_segment_start> <NA>

    <NA> means 'not applicable'
    '''
    with open(out_file, 'w') as f:
        for segment in ovl_segments:
            print(f'{uri} <NA> <NA> {util.dp2(segment.start)} {util.dp2(segment.end)} <NA>', file=f)