import streamlit as st
import requests
# from dotenv import load_dotenv
# import os

# Load environment variables
# load_dotenv()
FLASK_SERVER_URL = "https://vivekr.pythonanywhere.com/"  # Flask server URL

# Global variable for token storage
if "token" not in st.session_state:
    st.session_state.token = None

# Function to login and retrieve JWT token
def login(username, password):
    response = requests.post(f"{FLASK_SERVER_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json().get("token")
        st.success("Login successful!")
    else:
        st.error("Login failed! Check your credentials.")

# Display login form if not authenticated
st.title("Gemini-Pro Chatbot Interface")
if not st.session_state.token:
    with st.sidebar:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)

# Chat interface once logged in
if st.session_state.token:
    st.subheader("Chat with Google Gemini-Pro!")
    
    # Display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for chat
    user_prompt = st.chat_input("Ask Gemini-Pro anything...")
    if user_prompt:
        # Add user's message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Send message to Flask server with JWT token
        headers = {"x-access-tokens": st.session_state.token}
        response = requests.post(f"{FLASK_SERVER_URL}/chat", json={"message": user_prompt}, headers=headers)

        if response.status_code == 200:
            gemini_response = response.json().get("response")
            st.session_state.chat_history.append({"role": "assistant", "content": gemini_response})

            # Trigger rerun to refresh the chat interface
            st.rerun()
        else:
            st.error("Failed to get a response. Please check your token or login again.")
