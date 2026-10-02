import streamlit as st
import asyncio

from agent.graph import create_pharma_agent, investigate


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="PharmaSafety",
    page_icon="💊",
    layout="wide"
)


# -----------------------------
# Create agent once
# -----------------------------

@st.cache_resource
def get_agent():
    return asyncio.run(create_pharma_agent())


agent = get_agent()


# -----------------------------
# Session state
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-session"


# -----------------------------
# UI
# -----------------------------

st.title("💊 PharmaSafety")
st.caption("Conversational Pharmacovigilance Safety Investigation Agent")


# -----------------------------
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------

user_input = st.chat_input(
    "Ask PharmaSafety anything..."
)


if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Get agent response
    with st.chat_message("assistant"):

        with st.spinner("Investigating..."):

            response = asyncio.run(
                investigate(
                    agent,
                    user_input,
                    st.session_state.thread_id
                )
            )

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )