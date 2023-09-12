import openai
import os
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

class Tutor():
    def __init__(self, subject):
        self.subject = subject
        self.history = [{"role": "system", "content": \
                         f"You are a Friendly Awesome Smart Tutor for {subject}!"}]

    def ask(self, question):
        question = {"role": "user", "content": question}
        self.history.append(question)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )
        self.history.append({"role": "assistant", \
                             "content": response.choices[0].message.content})
        return response.choices[0].message.content