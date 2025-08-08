import streamlit as st
from auth import login_ui
from pages.twilio_alert import send_twilio_alert,show_danger_popup
from pages.live_location import get_user_location
from models import predict_emotion

# Page Setup
st.set_page_config(page_title="Embracelet App", layout="wide")

# Session Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login or main app
if not st.session_state.logged_in:
    login_ui()
else:
    st.sidebar.title(f"👤 Logged in as {st.session_state['user']}")
    menu = ["Dashboard", "Live Detection", "Location", "Send Alert", "Logout"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Dashboard":
        st.title("📊 Embracelet Dashboard")
        st.write("Welcome to the Embracelet app. Use the sidebar to navigate.")

    elif choice == "Live Detection":
        st.title("🎙️ Real-Time Emotion Detection")
        predict_emotion.show_emotion_ui()

    elif choice == "Location":
        st.title("📍 Live Location")
        location = get_user_location()
        if location:
            st.success(f"Your location: {location}")
        else:
            st.warning("Could not determine location.")

    elif choice == "Send Alert":
        st.title("🚨 Emergency Alert")
        phone_number = st.text_input("Enter phone number to alert (e.g., +1234567890):")
        if st.button("Send Alert"):
            if phone_number:
                send_twilio_alert(phone_number)
                st.success("Alert sent successfully!")
            else:
                st.error("Please enter a valid phone number.")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()

show_danger_popup()