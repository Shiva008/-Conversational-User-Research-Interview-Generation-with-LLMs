import streamlit as st
import random
import time
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv

import openai
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Chatbot : ChatGPT and Streamlit Chat")
st.subheader("Interviewer:")

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'messages' not in st.session_state:
    st.session_state.messages = get_initial_message()

query = st.text_input("Query: ", key="input")   

if query:
    with st.spinner("generating..."):
        messages = st.session_state.messages
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.messages = messages
        
if st.session_state.messages:
    st.write("Conversation:")
    # Display messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        st.markdown(word + " ")
        time.sleep(0.05)

# Accept user input
if prompt := st.text_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response_generator()
    # Add user message and assistant response to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
