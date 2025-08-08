import librosa
import numpy as np
import joblib
import os

# Load model once when the module loads
MODEL_PATH = "model/emotion_model.pkl"  # Make sure to place your model here
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Optional: Map numeric prediction to human emotion labels
EMOTIONS = {
    0: "neutral",
    1: "happy",
    2: "sad",
    3: "angry",
    4: "fear"
}

def extract_features(file_path):
    """Extract MFCC features from an audio file."""
    try:
        X, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        return mfccs.reshape(1, -1)
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def predict_emotion_from_audio(file_path):
    """Predict emotion using the pre-trained model."""
    if model is None:
        return "Model not loaded", 0.0

    features = extract_features(file_path)
    if features is not None:
        prediction = model.predict(features)[0]
        confidence = np.max(model.predict_proba(features))  # Only if model has predict_proba
        emotion = EMOTIONS.get(prediction, "unknown")
        return emotion, round(confidence, 2)
    else:
        return "Error", 0.0
