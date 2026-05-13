import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
import json

# Streamlit page settings
st.set_page_config(
    page_title="Sapphire by M.H Chatbot",
    page_icon="💎",
    layout="centered"
)

# OpenAI API Key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize location
if "location" not in st.session_state:
    st.session_state.location = None

# App title
st.title("💎 Sapphire by M.H Chatbot")

# Browser geolocation
location_data = components.html(
    """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };

            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: JSON.stringify(coords)
            }, "*");
        }
    );
    </script>
    """,
    height=0,
)

# Save location
if location_data:
    try:
        st.session_state.location = json.loads(location_data)
    except:
        pass

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask Sapphire anything...")

if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Add location context automatically
    if (
        "current temperature" in prompt.lower()
        or "weather" in prompt.lower()
        or "temperature" in prompt.lower()
    ) and st.session_state.location:

        lat = st.session_state.location["latitude"]
        lon = st.session_state.location["longitude"]

        prompt += (
            f"\nUser current location coordinates are:"
            f" Latitude {lat}, Longitude {lon}"
        )

    # System instruction
    system_message = {
        "role": "system",
        "content": (
            "You are Sapphire by M.H, an intelligent AI assistant. "
            "You remember previous conversation context and respond naturally. "
            "You can use web search for live information."
        )
    }

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        # Include history
        messages_for_api = [system_message]

        for msg in st.session_state.messages:
            messages_for_api.append(msg)

        # Streaming response
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_api,
            stream=True
        )

        for chunk in stream:

            if chunk.choices[0].delta.content:

                full_response += chunk.choices[0].delta.content

                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
