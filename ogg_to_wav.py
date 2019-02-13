import librosa

# TUA: ffmpeg package must be installed!
def ogg_to_wav(ogg_file):
    tmp_audio, sr = librosa.load(ogg_file)
    wavfile = ogg_file.split('.')[0] + '.wav'
    librosa.output.write_wav(wavfile, tmp_audio, sr)
    return wavfile

# parallel usage example

from multiprocessing import Pool

with Pool() as p:
    print(p.map(ogg_to_wav,tqdm_notebook([file for file in train['wav_filename']])))
