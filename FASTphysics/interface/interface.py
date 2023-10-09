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
        st.title(f"Welcome to FAST{self.tutor.SUBJECT()}!")
        for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    def stream(self, response):
        full_response = ""
        
        with st.chat_message("assistant"):
            message = st.empty()
            for chunk in response.split():
                full_response += chunk + " "
                message.markdown(full_response + "...")
                time.sleep(0.05)
            message.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    def prompt(self):
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            self.stream(self.tutor.ask(prompt))
            
    def main(self):
        self.memory()
        self.prompt()
