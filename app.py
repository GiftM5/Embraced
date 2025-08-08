# app.py
import streamlit as st
from pages import live_detection, location_page, twilio_alert
from auth import check_authentication

st.set_page_config(page_title="Embracelet", layout="wide")

# --- Login & Signup ---
if not check_authentication():
    st.stop()  # prevent access to the rest of the app

# --- Navigation Sidebar ---
st.sidebar.title("Embracelet Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🎤 Live Emotion Detection", "📍 Live Location", "📳 Emergency Alerts"])

# --- Page Router ---
if page == "🏠 Home":
    st.title("Welcome to Embracelet")
    st.markdown("""
    #### Your AI-powered safety net in crisis moments.
    - Detects emotional distress in real time from speech.
    - Sends alerts with your location using Twilio.
    - Keeps a record of incidents for evidence and reporting.
    """)
    st.image("static/hero.png")  # Optional: hero image

elif page == "🎤 Live Emotion Detection":
    live_detection.show()

elif page == "📍 Live Location":
    location_page.show()

elif page == "📳 Emergency Alerts":
    twilio_alert.show()
