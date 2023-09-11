import streamlit as st
from FASTphysics.tutor import tutor

class Interface:
    def __init__(self, tu: tutor) -> None:
        self.tutor = tu
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def memory(self):
        st.title("Welcome to FASTphysics!")
        for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    def prompt(self):
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in self.tutor.ask(prompt):
                    full_response += response
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    def main(self):
        self.memory()
        self.prompt()
