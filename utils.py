import librosa
import numpy as np

def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0).reshape(1, -1)

def predict_emotion(features):
    # Dummy prediction logic (replace with real model)
    import random
    emotions = ['neutral', 'fear', 'anger']
    pred = random.choice(emotions)
    confidence = random.uniform(0.75, 0.95)
    return pred, confidence
