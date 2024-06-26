from openai import OpenAI
import streamlit as st

st.title("Ask >nearly< a Politician")

client = OpenAI(api_key=st.secrets["TOKEN_CHATGPT"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    prompt = "Please answer the following question like a politician in two sentences. This means that you go into the topic as little as possible and don't say anything important about it, but just talk around it. The question:" + user_input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
