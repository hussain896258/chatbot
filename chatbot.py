import streamlit as st
from openai import OpenAI

# Streamlit page config
st.set_page_config(
    page_title="Sana AI Chat Bot",
    page_icon="🤖",
    layout="centered"
)

# OpenAI API Key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 Sana AI Chat Bot")

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask Sana AI something...")

if prompt:

    # Display user message
    st.chat_message("user").markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # OpenAI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
