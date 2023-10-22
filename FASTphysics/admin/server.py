# the server script for the admin side of FASTphysics
# an app that inputs entries through streamlit forms and prints the entries
import firestore as fs
import streamlit as st

collection_name, document_name = "prompts", "active"
subject_field_name, initp_field_name, firstp_field_name = "subject", "init", "first"

# default fall-back values
DEFAULT_SUBJECT = "physics"
DEFAULT_INITP = lambda subject: f"You are a Friendly Awesome Smart Tutor for {subject}!"
DEFAULT_FIRSTP = lambda subject: \
    f"Hey there, my tutor for {subject}! I am the student and here to learn more about {subject}!"

# list of buttons that admin can set values to
set_to_buttons_doc_names = ["astro-demo", "physics-demo"]
button_text_field_name = "button_text"

def set_to_button_click(db, button_doc_name):
    try:
        doc = fs.get_doc(db, collection_name, button_doc_name)
        st.session_state.subject = doc.get(subject_field_name)
        st.session_state.initp = doc.get(initp_field_name)
        st.session_state.firstp = doc.get(firstp_field_name)
        # update active document
        fs.update_doc_dict(db, collection_name, document_name, \
            {subject_field_name: st.session_state.subject, initp_field_name: st.session_state.initp, \
                firstp_field_name: st.session_state.firstp})
    except:
        print(f"Error in setting to {button_doc_name}.")

if __name__ == "__main__":
    db = fs.get_database()

    # load current values from the database
    doc = fs.get_doc(db, collection_name, document_name)
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
    
    # show current settings
    st.header("Current settings:")
    st.subheader("Subject:")
    st.write(st.session_state.subject)
    st.subheader("Instructions:")
    st.write(st.session_state.initp)
    st.subheader("First Student Input:")
    st.write(st.session_state.firstp)
        
    # several buttons that set the values to some preset values
    for button_doc_name in set_to_buttons_doc_names:
        button_text = fs.get_doc(db, collection_name, button_doc_name).get(button_text_field_name)
        st.button(f"Set to {button_text}", on_click=set_to_button_click, args=(db, button_doc_name))
        
    # a reset-to-default button
    if st.button("Reset to Default"):
        fs.update_doc_dict(db, collection_name, document_name, \
            {subject_field_name: DEFAULT_SUBJECT, initp_field_name: DEFAULT_INITP(DEFAULT_SUBJECT), \
                firstp_field_name: DEFAULT_FIRSTP(DEFAULT_SUBJECT)})
        st.session_state.subject = DEFAULT_SUBJECT
        st.session_state.initp = DEFAULT_INITP(DEFAULT_SUBJECT)
        st.session_state.firstp = DEFAULT_FIRSTP(DEFAULT_SUBJECT)

    # entry box for the subject
    subject = st.text_input("Subject", st.session_state.subject, key="subject-box")
    # entry box for the initialization prompt, box is multiline and bigger
    initp = st.text_area("Prompt", st.session_state.initp, height=200, key="initp-box")
    # entry box for the first prompt, box is multiline and bigger
    firstp = st.text_area("First Student Input", st.session_state.firstp, height=200, key="firstp-box")
    
    # set up the inputs in the database
    doc = fs.get_doc(db, collection_name, document_name)
    if doc.exists:
        fs.update_doc_dict(db, collection_name, document_name, \
            {subject_field_name: subject, initp_field_name: initp, firstp_field_name: firstp})
        st.session_state.subject, st.session_state.initp, st.session_state.firstp = subject, initp, firstp
    else:
        fs.set_doc_dict(db, collection_name, document_name, \
            {subject_field_name: subject, initp_field_name: initp, firstp_field_name: firstp})
        st.session_state.subject, st.session_state.initp, st.session_state.firstp = subject, initp, firstp
