# file where we read and store all the prompts to OpenAI

import json
from google.cloud import firestore
from google.oauth2 import service_account

DEFAULT_SUBJECT = "physics"
DEFAULT_INITP = lambda subject: f"You are a Friendly Awesome Smart Tutor for {subject}!"

class Prompts:
    def __init__(self) -> None:
        # connect to the firestore database
        firestore_key = json.loads(st.secrets["FIRESTORE_KEY"])
        creds = service_account.Credentials.from_service_account_info(firestore_key)
        self.db = firestore.Client(credentials=creds)
        
        doc_ref = self.db.collection("prompts").document("demo")
        self.doc = doc_ref.get()
        
    def SUBJECT(self):
        if self.doc.exists:
            return self.doc.get("subject")
        else:
            return DEFAULT_SUBJECT
    
    def INIT_PROMPT(self):
        if self.doc.exists:
            return self.doc.get("init")
        else:
            return DEFAULT_INITP(self.SUBJECT())