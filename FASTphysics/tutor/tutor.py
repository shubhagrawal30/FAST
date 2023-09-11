import openai
import os

with open(os.path.join(os.path.dirname(__file__), "..", ".OPENAI-API-KEY")) as f:
    openai.api_key = f.read().strip()

class Tutor():
    def __init__(self, subject):
        self.subject = subject

    def ask(self, question):
        return "This is a placeholder response."
