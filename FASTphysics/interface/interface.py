import sys, time
sys.path.append("../")
import streamlit as st
from tutor import tutor

class Interface:
    def __init__(self, tu: tutor) -> None:
        self.tutor = tu
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def memory(self):
        st.title(f"Welcome to FAST{self.tutor.subject}!")
        for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    def stream(self, prompt):
        full_response = ""
        with st.chat_message("assistant"):
            message = st.empty()
            for chunk in self.tutor.ask(prompt):
                full_response += chunk
                message.markdown(full_response + "...")
                time.sleep(0) # can be used to control the speed of the response
            message.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    def prompt(self):
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            self.stream(prompt)
            
    def main(self):
        self.memory()
        self.prompt()
