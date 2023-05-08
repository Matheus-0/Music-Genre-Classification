import os

import librosa
import numpy as np
import pandas as pd
from joblib import load
from scipy.stats import kurtosis
from scipy.stats import skew


def get_features(y, sr, n_fft=1024, hop_length=512):
    features = {}

    features['spectral_centroid'] = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['spectral_rolloff'] = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['zero_crossing_rate'] = librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=hop_length).ravel()
    features['rms'] = librosa.feature.rms(y=y, frame_length=n_fft, hop_length=hop_length).ravel()
    features['onset_strength'] = librosa.onset.onset_strength(y=y, sr=sr).ravel()
    features['spectral_contrast'] = librosa.feature.spectral_contrast(y=y, sr=sr).ravel()
    features['spectral_bandwidth'] = librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length).ravel()
    features['spectral_flatness'] = librosa.feature.spectral_flatness(y=y, n_fft=n_fft, hop_length=hop_length).ravel()

    mfcc = librosa.feature.mfcc(y=y, n_fft=n_fft, hop_length=hop_length, n_mfcc=13)

    for index, v_mfcc in enumerate(mfcc):
        features['mfcc_{}'.format(index)] = v_mfcc.ravel()

    def get_moments(descriptors):
        result = {}

        for k, v in descriptors.items():
            result['{}_max'.format(k)] = np.max(v)
            result['{}_min'.format(k)] = np.min(v)
            result['{}_mean'.format(k)] = np.mean(v)
            result['{}_std'.format(k)] = np.std(v)
            result['{}_kurtosis'.format(k)] = kurtosis(v)
            result['{}_skew'.format(k)] = skew(v)

        return result

    additional_features = get_moments(features)
    additional_features['tempo'] = librosa.feature.tempo(y=y, sr=sr)[0]

    return additional_features


music_directory = './test_songs'
music_files = os.listdir(music_directory)

pipe = load('./models/pipe_svm.joblib')

for music in music_files:
    signal, sr = librosa.load(os.path.join(music_directory, music))
    features = get_features(signal, sr)
    song = pd.DataFrame([features])

    pred = pipe.predict(song)[0]

    print(f'{music} é uma música de {pred}')
