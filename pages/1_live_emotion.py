# pages/1_Live_Emotion.py
import streamlit as st
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
import torch
import torchaudio
from utils.ml_model import predict_emotion

st.set_page_config(page_title="Live Emotion Detection", layout="centered")
st.title("🎙️ Live Emotion Detection")
st.markdown("Record your voice and let our AI detect emotional distress.")

DURATION = 5  # seconds
SAMPLE_RATE = 44100

if 'recording' not in st.session_state:
    st.session_state.recording = False

# Button to record
if st.button("🎤 Start Recording"):
    st.session_state.recording = True
    st.success("Recording started for 5 seconds...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    # Save to temp WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav.write(tmp.name, SAMPLE_RATE, recording)
        tmp_path = tmp.name

    st.audio(tmp_path)

    # Load and predict
    emotion, confidence = predict_emotion(tmp_path)
    st.subheader(f"🧠 Detected Emotion: **{emotion}**")
    st.caption(f"Confidence: {confidence:.2f}%")

    # Clean up
    os.remove(tmp_path)
