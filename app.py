import streamlit as st
import numpy as np
import pandas as pd
import random
from utils import extract_features, predict_emotion
import time

st.set_page_config(page_title="Embracelet Demo", layout="centered")

st.title("💜 Embracelet - Real-Time GBV Detection Demo")

# Simulate vitals
hr = random.randint(80, 160)
temp = round(random.uniform(36.5, 39.5), 1)

st.subheader("📍 Live Vitals (Simulated)")
st.metric("Heart Rate (BPM)", hr, delta=None)
st.metric("Body Temperature (°C)", temp, delta=None)

# Upload audio
st.subheader("🎙️ Voice Emotion Detection")
audio_file = st.file_uploader("Upload a scream/speech audio", type=["wav"])

if audio_file:
    st.audio(audio_file, format='audio/wav')
    features = extract_features(audio_file)
    emotion, confidence = predict_emotion(features)
    
    st.success(f"Detected Emotion: **{emotion.upper()}** with {int(confidence * 100)}% confidence")

    if emotion.lower() in ['fear', 'anger'] and hr > 130:
        st.error("⚠️ High stress detected! Alert triggered.")
        st.write("📩 Sending alert to emergency contact...")
        time.sleep(1)
        st.success("✅ Alert sent.")

# Show event timeline
st.subheader("📊 Timeline of Detected Events")
df = pd.DataFrame({
    "Time": ["08:12", "08:17", "08:19"],
    "Emotion": ["Fear", "Fear", "Anger"],
    "HeartRate": [145, 138, 142]
})
st.dataframe(df)
