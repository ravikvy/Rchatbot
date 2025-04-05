import streamlit as st
import openai

# 1. Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 2. Set the title of the app
st.title("Your ChatBot Name")

# 3. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User input box
user_input = st.chat_input("Say something...")

# 6. Function to get response from OpenAI
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']

# 7. If user submits input, send and get reply
if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and show assistant reply
    response = get_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
