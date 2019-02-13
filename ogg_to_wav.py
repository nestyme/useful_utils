import librosa

def ogg_to_wav(ogg_file):
    tmp_audio, sr = librosa.load(ogg_file)
    wavfile = ogg_file.split('.')[0] + '.wav'
    librosa.output.write_wav(wavfile, tmp_audio, sr)
    return wavfile
