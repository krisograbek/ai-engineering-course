import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


# I'll work with it at the very end, because it's bad for development now
# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


client = OpenAI()
# Sidebar
st.sidebar.title("Configuration")

if "model" not in st.session_state:
    st.session_state["model"] = "gpt-4o-mini"


def model_callback():
    st.session_state["model"] = st.session_state["model_selected"]


st.session_state.model = st.sidebar.radio(
    "Select OpenAI Model",
    ("gpt-4o-mini", "gpt-4o"),
    index=0 if st.session_state["model"] == "gpt-4o-mini" else 1,
    on_change=model_callback,
    key="model_selected",
)

st.sidebar.markdown(
    f"""
    ### ℹ️ <span style="white-space: pre-line; font-family: Arial; font-size: 14px;">Current model: {st.session_state.model}.</span>
    """,
    unsafe_allow_html=True,
)

st.title("GPT-4o Mini Chatbot!🤖")


initial_system_prompt = "The user's name is Kris, he's 37 from Poland"

# Check if the messages exist in session_state, if not, initialize them
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": initial_system_prompt,
        }
    ]

# Ensure the system prompt key exists in session_state
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = initial_system_prompt


def system_prompt_callback():
    # Update the system prompt in messages based on the current input
    st.session_state.messages[0]["content"] = st.session_state["system_prompt"]


st.sidebar.text_input(
    "System Prompt",
    value=st.session_state["system_prompt"],
    on_change=system_prompt_callback,
    key="system_prompt",
)

# For debugging (when needed)
# st.sidebar.write(st.session_state.messages)

# Main App


for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# initialize model
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

# user input
if user_prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=st.session_state["model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token is not None:
                full_response += token
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
