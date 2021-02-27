import argparse
import ovl
import dia

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='Name of method to be applied to audio. Options are \'ovl\', for overlapped speech detection, and \'dia\', for speaker diarization.')
    parser.add_argument('audio_file', help='Path to .wav audio file to be processed.')
    parser.add_argument('audio_uri', help='Unique identifier for audio file.')
    parser.add_argument('--outfile', nargs='?', help='Path & filename for output file.')
    parser.add_argument('--model', nargs='?', help='Name of pretrained model to be used. Options are \'ami\' and \'dihard\'. Default is \'dihard\'')
    args = parser.parse_args()
    
    method = args.method
    if method != 'ovl' and method != 'dia':
        print('Error: method argument must be either \'ovl\' or \'dia\'.')
        return

    in_file = args.audio_file

    model = f'{method}_dihard'
    if args.model == 'ami':
        model = f'{method}_ami'

    # Output files will be .ovl.txt for overlapped speech, .dia.txt for diarization
    out_file = in_file.replace('.wav', f'.{method}.txt')
    if args.outfile:
        out_file = args.outfile

    uri = args.audio_uri

    if method == 'ovl':
        ovl_segments = ovl.get_overlapping_speech(in_file, model)
        ovl.output_ovl(uri, out_file, ovl_segments)
    elif method == 'dia':
        dia_annotation = dia.get_diarized_speech(in_file, model)
        dia.output_dia(uri, out_file, dia_annotation)

if __name__ == '__main__':
    main()