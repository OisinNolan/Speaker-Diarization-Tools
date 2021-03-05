import argparse
import ovl
import dia

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('method', help='Name of method to be applied to audio. Options are \'ovl\', for overlapped speech detection, and \'dia\', for speaker diarization.')
    parser.add_argument('audio_file', help='Path to .wav audio file to be processed.')
    parser.add_argument('audio_uri', help='Unique identifier for audio file.')
    parser.add_argument('--outfile', nargs='?', help='Path & filename for output file. By default, output file will be given the same name as the input .wav file, but with a .ovl.txt or .dia.txt extension depending on the chosen method.')
    parser.add_argument('--model', nargs='?', help='Name of pretrained model to be used. Options are \'ami\' and \'dihard\'. Default is \'dihard\'. See pyannote.audio for more detail on these models.')
    parser.add_argument('--ovl_threshold', nargs='?', help='Decimal number between 0 and 1 specifying the threshold deciding whether or not overlapped speech is present. 0 --> all overlap, 1 --> no overlap, 0.55 is default.')
    args = parser.parse_args()
    
    method = args.method
    if method != 'ovl' and method != 'dia':
        print('Error: method argument must be either \'ovl\' or \'dia\'.')
        return

    in_file = args.audio_file

    # Model is ovl_dihard / dia_dihard by default, or ovl_ami / dia_ami if specified
    model = f'{method}_ami' if args.model == 'ami' else f'{method}_dihard'

    # Output files will be .ovl.txt for overlapped speech, .dia.txt for diarization
    out_file = args.outfile if args.outfile else in_file.replace('.wav', f'.{method}.txt')

    uri = args.audio_uri

    if method == 'ovl':
        threshold = float(args.ovl_threshold) if args.ovl_threshold else 0.55
        ovl_segments = ovl.get_overlapping_speech(in_file, model, threshold)
        ovl.output_ovl(uri, out_file, ovl_segments)
    elif method == 'dia':
        dia_annotation = dia.get_diarized_speech(in_file, model)
        dia.output_dia(uri, out_file, dia_annotation)

if __name__ == '__main__':
    main()