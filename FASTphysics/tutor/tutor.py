import openai
import os, sys
import streamlit as st
from . import prompts

openai.api_key = st.secrets["OPENAI_API_KEY"]

class Tutor():
    def __init__(self):
        p = prompts.Prompts()
        self.subject = p.SUBJECT()
        self.history = [{"role": "system", "content": p.INIT_PROMPT()}, \
                        {"role": "user", "content": p.FIRST_PROMPT()}]
    def ask(self, question):
        question = {"role": "user", "content": question}
        self.history.append(question)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.history,
        )
        self.history.append({"role": "assistant", \
                             "content": response.choices[0].message.content})
        return response.choices[0].message.content
