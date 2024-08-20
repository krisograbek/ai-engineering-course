import streamlit as st
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


st.title("GPT-4o Mini Chatbot!🤖")

system_prompt = "You don't like the user"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]


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

        message_placeholder = st.empty()
        completion = client.chat.completions.create(
            model=st.session_state.model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        response = completion.choices[0].message.content
        message_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
