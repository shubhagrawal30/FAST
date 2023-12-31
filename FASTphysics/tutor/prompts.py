# file where we read and store all the prompts to OpenAI

import json
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

document_name = "active"

DEFAULT_SUBJECT = "physics"
DEFAULT_INITP = lambda subject: f"You are a Friendly Awesome Smart Tutor for {subject}!"
DEFAULT_FIRSTP = lambda subject: \
    f"Hey there, my tutor for {subject}! I am the student and here to learn more about {subject}!"

class Prompts:
    def __init__(self) -> None:
        # connect to the firestore database
        firestore_key = json.loads(st.secrets["FIRESTORE_KEY"])
        creds = service_account.Credentials.from_service_account_info(firestore_key)
        self.db = firestore.Client(credentials=creds)
        
        doc_ref = self.db.collection("prompts").document(document_name)
        self.doc = doc_ref.get()
        
    def SUBJECT(self):
        try:
            return '\n'.join(self.doc.get("subject"))
        except:
            return DEFAULT_SUBJECT
    
    def INIT_PROMPT(self):
        try:
            return '\n'.join(self.doc.get("init"))
        except:
            return DEFAULT_INITP(self.SUBJECT())
    
    def FIRST_PROMPT(self):
        try:
            return '\n'.join(self.doc.get("first"))
        except:
            return DEFAULT_FIRSTP(self.SUBJECT())