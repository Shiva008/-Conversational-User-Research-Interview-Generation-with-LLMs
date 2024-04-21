import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
import openai
import json
# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit app title and subheader
st.title("Chatbot : Conversational User Research Interview Generation with LLM")
st.subheader("Interviewer:")

# Select model
model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4(currently not working)")
)

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

# Display conversation
if st.session_state['generated']:
    st.write("Conversation:")
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
        
# User input for query
query = st.text_input("User: ", key="input")   

# Handle user query
if query:
    with st.spinner("Generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

# # Display conversation
# if st.session_state['generated']:
#     st.write("Conversation:")
#     for i in range(len(st.session_state['generated'])):
#         message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
#         message(st.session_state["generated"][i], key=str(i))
if st.button("Download Conversation as JSON"):
    conversation = {
        "user_messages": st.session_state['past'],
        "assistant_messages": st.session_state['generated']
    }
    with open("conversation.json", "w") as file:
        json.dump(conversation, file)
    st.success("Conversation downloaded as JSON file.")
