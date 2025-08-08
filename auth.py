import streamlit as st
import json
import hashlib
import os

USERS_DB = "users.json"

def load_users():
    if os.path.exists(USERS_DB):
        with open(USERS_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_DB, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users = load_users()
    hashed_pw = hash_password(password)
    if username in users and users[username] == hashed_pw:
        return True
    return False

def register(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def login_ui():
    st.title("🔐 Embracelet Login")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.subheader("Create New Account")
        username = st.text_input("Username", key="register_user")
        password = st.text_input("Password", type="password", key="register_pass")
        if st.button("Register"):
            if register(username, password):
                st.success("Registration successful. Please log in.")
            else:
                st.warning("Username already exists")
