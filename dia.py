import torch
import util

def get_diarized_speech(audio_file, model):
    '''
    For a given audio file at path 'audio_file', and model type, which may be
    either 'dia_ami' or 'dia_dihard', calculate who spoke when.

    Returns segments with associated speaker lables in the form of a 
    pyannote.core Annotation
    '''
    pipeline = torch.hub.load('pyannote/pyannote-audio', model)
    diarized_speech = pipeline({'audio': audio_file})
    return diarized_speech

def output_dia(uri, out_file, dia_annotation):
    '''
    Output speaker diarization info to a text file in the following format:
    <audio_id> <headphone_id> <speaker_id> <speech_segment_start> <speech_segment_end> <speech_transcription>

    headhpone_id and speech_transcription are not known so placeholders are used.
    '''
    with open(out_file, 'w') as f:
        for key in list(dia_annotation.itertracks()):
            segment = key[0]
            speaker_label = dia_annotation[key]
            print(f'{uri} <headphone> {speaker_label} {util.dp2(segment.start)} {util.dp2(segment.end)} <text>', file=f)