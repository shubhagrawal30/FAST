import openai
import os
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

class Tutor():
    def __init__(self, subject):
        self.subject = subject

    def ask(self, question):
        return "This is a placeholder response."
