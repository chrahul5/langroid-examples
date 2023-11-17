'''
This file defines the streamlit front end to interact with cloud-langroid.
'''
import streamlit as st
import requests

# Function to send the message to the Flask API
def send_message(message, file):
    url = "http://127.0.0.1:8080/langroid/agent/completions"
    # Assuming your Flask API expects a JSON payload with 'message' and 'file'
    payload = {'prompt': message}
    files = {'file': file.getvalue()} if file else None
    response = requests.post(url, json=payload, files=files)
    print(response.json())
    return response.json()

# Chat display area
chat_container = st.container()

# Input for the message
message = st.text_input("Type your message here...")

# File uploader
file = st.file_uploader("Attach a document", type=['pdf', 'docx', 'txt'])

# Send button
if st.button('Send'):
    chat_response = send_message(message, file)
    with chat_container:
        st.write(f"You: {message}")
        st.write(f"Bot: {chat_response.get('message')}")  # assuming your API returns a 'reply'

# This part would be where you display the chat history. You would need to store
# the chat history in a session state or an external database to preserve the state
# across multiple interactions.
