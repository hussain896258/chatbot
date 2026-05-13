import streamlit as st
from openai import OpenAI
import uuid
import streamlit.components.v1 as components
import json

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="💎 Sapphire by M.H Chatbot",
    page_icon="💎",
    layout="wide"
)

# ---------------- OPENAI ----------------

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------- SESSION STATE ----------------

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:

    first_chat_id = str(uuid.uuid4())

    st.session_state.chats[first_chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat = first_chat_id

if "location" not in st.session_state:
    st.session_state.location = None

# ---------------- LOCATION DETECTION ----------------

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

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("💎 Sapphire")

    # New Chat
    if st.button("➕ New Chat", use_container_width=True):

        new_chat_id = str(uuid.uuid4())

        st.session_state.chats[new_chat_id] = {
            "title": "New Chat",
            "messages": []
        }

        st.session_state.current_chat = new_chat_id

        st.rerun()

    st.divider()

    # Chat History
    for chat_id, chat_data in st.session_state.chats.items():

        chat_title = chat_data["title"]

        if st.button(chat_title, key=chat_id, use_container_width=True):

            st.session_state.current_chat = chat_id

            st.rerun()

# ---------------- CURRENT CHAT ----------------

current_chat = st.session_state.chats[
    st.session_state.current_chat
]

messages = current_chat["messages"]

# ---------------- MAIN UI ----------------

st.title("💎 Sapphire by M.H Chatbot")

# Location status
if st.session_state.location:

    st.caption(
        f"📍 Location detected "
        f"({st.session_state.location['latitude']:.2f}, "
        f"{st.session_state.location['longitude']:.2f})"
    )

else:

    st.caption("📍 Allow browser location access for live weather")

# ---------------- DISPLAY CHAT ----------------

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("Ask Sapphire anything...")

if prompt:

    # Save user message
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Auto title generation
    if current_chat["title"] == "New Chat":

        current_chat["title"] = prompt[:30]

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Add live location automatically
    if (
        "weather" in prompt.lower()
        or "temperature" in prompt.lower()
        or "current location" in prompt.lower()
    ) and st.session_state.location:

        lat = st.session_state.location["latitude"]
        lon = st.session_state.location["longitude"]

        prompt += (
            f"\nUser live coordinates:"
            f" Latitude {lat}, Longitude {lon}."
            f" Use this for accurate live weather/location answers."
        )

    # Assistant response
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        # System prompt
        api_messages = [
            {
                "role": "system",
                "content": (
                    "You are Sapphire by M.H, "
                    "an intelligent AI assistant with live web knowledge."
                )
            }
        ]

        # Add chat history
        api_messages.extend(messages)

        # Add latest prompt
        api_messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Streaming response
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            stream=True
        )

        for chunk in stream:

            if chunk.choices[0].delta.content:

                text = chunk.choices[0].delta.content

                full_response += text

                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    # Save assistant response
    messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
