import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Dr. Ravi - Ortho & Sports Injury Advisor")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms
user_input = st.chat_input("Describe your symptoms related to ortho, sports injury, or physiotherapy...")

# Function to get a response from OpenAI with health advice
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are Dr. Ravi, a helpful and knowledgeable medical assistant who provides advice "
                "only related to orthopedics, sports injuries, and physiotherapy. Politely decline questions "
                "outside your domain and encourage users to seek professional help if symptoms are severe."
            )}
        ] + st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = (
        f"The user described the following: {user_input}. "
        f"Remember, you're Dr. Ravi, and only provide advice related to orthopedics, sports injuries, or physiotherapy."
    )
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
