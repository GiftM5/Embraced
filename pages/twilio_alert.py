from twilio.rest import Client
import time
import os
import threading
import streamlit as st

# Twilio credentials from your account (use env variables or Streamlit secrets in production)
sid = os.getenv("TWILIO_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
personal_phone_number = os.getenv("PERSONAL_PHONE_NUMBER")  # Replace with the user's phone number

client = Client(sid, token)


def send_twilio_alert(to_number=None, message=None):
    """Sends an SMS alert using Twilio."""
    account_sid = sid
    auth_token = token

    if not to_number:
        to_number = personal_phone_number
    if not message:
        message = "Emergency Alert! Please check on the user immediately."
    if not account_sid or not auth_token:
        st.error("Twilio credentials are not set. Please check your environment variables or secrets.")
        return None

    try:
        client = Client(account_sid, auth_token)
        sent_message = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=to_number
        )
        return sent_message.sid
    except Exception as e:
        st.error(f"Failed to send SMS: {e}")
        return None


def danger_confirmation_timer(user_name, timeout=30):
    """Waits for user response. If no response in `timeout`, send SMS alert."""
    time.sleep(timeout)
    if not st.session_state.get("danger_acknowledged", False):
        st.warning("No user confirmation. Sending emergency alert.")
        send_twilio_alert(user_name)


def show_danger_popup():
    """Shows popup with danger confirmation and starts countdown."""
    st.session_state["danger_acknowledged"] = False
    st.warning("⚠️ Are you in danger? Please confirm.")
    if st.button("I'm Safe"):
        st.session_state["danger_acknowledged"] = True
        st.success("Marked as safe. No alert sent.")

    # Start countdown timer thread
    if not st.session_state.get("timer_started", False):
        st.session_state["timer_started"] = True
        threading.Thread(
            target=danger_confirmation_timer,
            args=(st.session_state.get("user", personal_phone_number),),
            daemon=True
        ).start()
