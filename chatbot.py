import streamlit as st
from openai import OpenAI

# Streamlit page settings
st.set_page_config(
    page_title="Sana AI Chat Bot",
    page_icon="🤖",
    layout="centered"
)

# OpenAI API Key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("🤖 Sana AI Chat Bot")

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask Sana AI anything...")

if prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate response with web search
    response = client.responses.create(
        model="gpt-4.1-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )

    reply = response.output_text

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
