import sys, time, os
sys.path.append("../")
import streamlit as st
from streamlit_extras.colored_header import colored_header
st.set_page_config(layout="wide")

from tutor import tutor
from utils import info

class Interface:
    def __init__(self, tu: tutor) -> None:
        self.tutor = tu
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
    def sidebar(self):
        sb = st.sidebar
        sb.title("Friendly Awesome Smart Tutor")
        with sb:
            colored_header("Here to help with:", description=f"{self.tutor.subject}", color_name="violet-70")
        
        # add Penn logo and credits
        sb.markdown("----")
        sb.markdown("----")
        logo_path = os.path.join(os.path.dirname(__file__), "../assets/penn_logo.png")
        sb.image(logo_path, width=250)
        sb.caption(f"Student Page @ [{info.student_page_url.split('//')[1]}](%s)" % info.student_page_url)
        sb.caption(f"Teacher Page @ [{info.admin_page_url.split('//')[1]}](%s)" % info.admin_page_url)
        sb.caption("© 2023, S.A. for the FAST team. All rights reserved.")
        sb.caption("Contact [Shubh Agrawal](%s) for comments." % "mailto:shubh@sas.upenn.edu")

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
        if prompt := st.chat_input("Say Hello! to your Friendly Awesome Smart Tutor!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            self.stream(prompt)
            
    def main(self):
        self.sidebar()
        self.memory()
        self.prompt()
