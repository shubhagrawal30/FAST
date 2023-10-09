# the server script for the admin side of FASTphysics
# an app that inputs entries through streamlit forms and prints the entries

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

collection_name, document_name = "prompts", "demo"
subject_field_name, initp_field_name = "subject", "init"

if __name__ == "__main__":
    firestore_key = json.loads(st.secrets["FIRESTORE_KEY"])
    creds = service_account.Credentials.from_service_account_info(firestore_key)
    db = firestore.Client(credentials=creds)
    
    # load current values from the database
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    if doc.exists:
        subject = doc.get(subject_field_name)
        initp = doc.get(initp_field_name)
    else:
        subject = "physics"
        initp = "You are a Friendly Awesome Smart Tutor for physics!"
    
    st.title("FASTphysics Admin")
    # entry box for the subject
    subject = st.text_input("Subject", subject)
    # entry box for the initialization prompt
    initp = st.text_input("Prompt", initp)
    
    # set up the inputs in the database
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({subject_field_name: subject, initp_field_name: initp})
    else:
        doc_ref.set({subject_field_name: subject, initp_field_name: initp})
