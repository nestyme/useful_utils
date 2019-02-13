import numpy as np
import scipy.io.wavfile as wav

# enable librosa if you want to convert .oggs. Be carefull -- it might take much more time
# import librosa 

from python_speech_features import mfcc


def audiofile_to_input_vector(audio_filename, numcep, numcontext):
    # Load audio files
    fs, audio = wav.read(audio_filename)
    
    # audio, fs = librosa.load(audio_filename)
    # Get mfcc coefficients
    # print('numcep: {}, numcontext: {}'.format(numcontext, numcep))
    features = mfcc(audio,samplerate=fs, numcep=numcep, nfft=512, winlen=0.032, winstep=0.02, winfunc=np.hamming)
    
    # Add empty initial and final contexts
    empty_context = np.zeros((numcontext, numcep), dtype=features.dtype)
    features = np.concatenate((empty_context, features, empty_context))
    
    # print('processed: {}'.format(audio_filename))
    return features
