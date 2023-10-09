# the server script for the admin side of FASTphysics
# an app that inputs entries through streamlit forms and prints the entries

import streamlit as st

if __name__ == "__main__":
    st.title("FASTphysics Admin")
    
    # entry box for the subject
    subject = st.text_input("Subject", "physics")
    
    # entry box for the initialization prompt
    initp = st.text_input("Prompt", f"You are a Friendly Awesome Smart Tutor for {subject}!")
    
    print(subject, initp)