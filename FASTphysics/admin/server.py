# the server script for the admin side of FASTphysics
# an app that inputs entries through streamlit forms and prints the entries

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

collection_name, document_name = "prompts", "demo"
subject_field_name, initp_field_name, firstp_field_name = "subject", "init", "first"

DEFAULT_SUBJECT = "physics"
DEFAULT_INITP = lambda subject: f"You are a Friendly Awesome Smart Tutor for {subject}!"
DEFAULT_FIRSTP = lambda subject: \
    f"Hey there, my tutor for {subject}! I am the student and here to learn more about {subject}!"

if __name__ == "__main__":
    firestore_key = json.loads(st.secrets["FIRESTORE_KEY"])
    creds = service_account.Credentials.from_service_account_info(firestore_key)
    db = firestore.Client(credentials=creds)
    
    # load current values from the database
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    try:
        st.session_state.subject = doc.get(subject_field_name)
        st.session_state.initp = doc.get(initp_field_name)
        st.session_state.firstp = doc.get(firstp_field_name)
    except:
        st.session_state.subject = DEFAULT_SUBJECT
        st.session_state.initp = DEFAULT_INITP(st.session_state.subject)
        st.session_state.firstp = DEFAULT_FIRSTP(st.session_state.subject)
    
    st.title("FAST Admin")
    st.text("Remember to reload the student page after reconfiguration.")
    
    # entry box for the subject
    subject = st.text_input("Subject", st.session_state.subject, key="subject-box")
    # entry box for the initialization prompt, box is multiline and bigger
    initp = st.text_area("Prompt", st.session_state.initp, height=200, key="initp-box")
    # entry box for the first prompt, box is multiline and bigger
    firstp = st.text_area("First Student Input", st.session_state.firstp, height=200, key="firstp-box")
    
    # set up the inputs in the database
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({subject_field_name: subject, initp_field_name: initp, firstp_field_name: firstp})
    else:
        doc_ref.set({subject_field_name: subject, initp_field_name: initp, firstp_field_name: firstp})
        
    # a reset-to-default button
    if st.button("Reset to Default"):
        doc_ref.update({subject_field_name: DEFAULT_SUBJECT, initp_field_name: DEFAULT_INITP(DEFAULT_SUBJECT), \
            firstp_field_name: DEFAULT_FIRSTP(DEFAULT_SUBJECT)})
        st.session_state.subject = DEFAULT_SUBJECT
        st.session_state.initp = DEFAULT_INITP(DEFAULT_SUBJECT)
        st.session_state.firstp = DEFAULT_FIRSTP(DEFAULT_SUBJECT)
        
    # show current settings
    doc_ref = db.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    st.header("Current settings:")
    st.write(f"Subject: {doc.get(subject_field_name)}")
    st.write(f"Prompt: {doc.get(initp_field_name)}")
    st.write(f"First Student Input: {doc.get(firstp_field_name)}")
    