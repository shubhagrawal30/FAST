# the server script for the admin side of FASTphysics
# an app that inputs entries through streamlit forms and prints the entries
import sys, re, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from utils import info

import firestore as fs
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.mention import mention
from streamlit_extras.badges import badge
st.set_page_config(layout="wide")

NUM_LINES_SETTINGS = 3
collection_name, document_name = "prompts", "active"
subject_field_name, initp_field_name, firstp_field_name = "subject", "init", "first"

# default fall-back values
DEFAULT_SUBJECT = "physics"
DEFAULT_INITP = lambda subject: f"You are a Friendly Awesome Smart Tutor for {subject}!"
DEFAULT_FIRSTP = lambda subject: \
    f"Hey there, my tutor for {subject}! I am the student and here to learn more about {subject}!"

# list of buttons that admin can set values to
set_to_buttons_doc_names = ["astro-demo", "physics-demo", "eco-demo"]
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
        
def set_to_default_click(db):
    fs.update_doc_dict(db, collection_name, document_name, \
        {subject_field_name: DEFAULT_SUBJECT, initp_field_name: DEFAULT_INITP(DEFAULT_SUBJECT), \
            firstp_field_name: DEFAULT_FIRSTP(DEFAULT_SUBJECT)})
    st.session_state.subject = DEFAULT_SUBJECT
    st.session_state.initp = DEFAULT_INITP(DEFAULT_SUBJECT)
    st.session_state.firstp = DEFAULT_FIRSTP(DEFAULT_SUBJECT)

def update_text_area(fn, db, collection_name, document_name):
    st.session_state[fn] = st.session_state[f"{fn}-box"]
    doc = fs.get_doc(db, collection_name, document_name)
    if doc.exists:
        fs.update_doc_dict(db, collection_name, document_name, {subject_field_name: st.session_state.subject, \
            initp_field_name: st.session_state.initp, firstp_field_name: st.session_state.firstp})
    else:
        fs.set_doc_dict(db, collection_name, document_name, {subject_field_name: st.session_state.subject, \
            initp_field_name: st.session_state.initp, firstp_field_name: st.session_state.firstp})

def add_logo_and_credits():
    st.markdown("----")
    st.markdown("----")
    # add Penn logo and credits
    _, col, _, bcol = st.columns([4, 1, 2, 3])
    logo_path = os.path.join(os.path.dirname(__file__), "../assets/penn_logo.png")
    col.image(logo_path, width=250)
    with bcol:
        badge("github", "shubhagrawal30/FASTphysics")
        mention("shubhagrawal30/FASTphysics", icon="github", url="https://github.com/shubhagrawal30/FASTphysics")
    _, col1, col2, col3, _ = st.columns([2, 5, 5, 5, 1])
    col1.caption(f"Student Page @ [{info.student_page_url.split('//')[1]}](%s)" % info.student_page_url)
    col2.caption("© 2023, S.A. for the FAST team. All rights reserved.")
    col3.caption("Contact [Shubh Agrawal](%s) for comments." % "mailto:shubh@sas.upenn.edu")

def print_setting(text):
    if len(text) == 0:
        return "_<currently empty>_", False
    else:
        sentences = re.split('[.;?!]', text)
        idx = text.find(sentences[NUM_LINES_SETTINGS]) if len(sentences) > NUM_LINES_SETTINGS else len(text)
        return text[:idx], idx < len(text)

def add_current_settings():
    # show current settings
    colored_header("Current settings:", description="", color_name="blue-70")
    for hd, fn in zip(["Subject:", "Instructions:", "First Student Input:"], \
                        ["subject", "initp", "firstp"]):
        st.subheader(hd)
        text, read_more = print_setting(st.session_state[fn])
        if read_more:
            st.markdown(text + "...")
            st.expander(":blue[Read More]", expanded=False).markdown(st.session_state[fn])
        else:
            st.markdown(text)

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
    
    st.title("Control Panel for the Friendly Awesome Smart Tutor!")
    st.text("Remember to reload the student page after reconfiguration.")
    st.empty()
    col1, col2 = st.columns(2)
    
    with col1:
        add_current_settings()
        
    with col2:
        button_cols = col2.columns(3)
        # several buttons that set the values to some preset values
        for ind, button_doc_name in enumerate(set_to_buttons_doc_names):
            button_text = fs.get_doc(db, collection_name, button_doc_name).get(button_text_field_name)
            button_cols[ind % len(button_cols)].button(button_text, type="primary", use_container_width=True, \
                on_click=set_to_button_click, args=(db, button_doc_name))
            
        # a reset-to-default button
        st.button("Reset to Default", type="secondary", use_container_width=True, \
            on_click=set_to_default_click, args=(db,))

        # make entry boxes for the settings
        for text, fn, ht in zip(["Subject:", "Instructions:", "First Student Input:"], \
                            ["subject", "initp", "firstp"], [None, 200, 200]):
            func = st.text_area if fn != "subject" else st.text_input
            kwargs = {"key": f"{fn}-box", "on_change": update_text_area, "args": (fn, db, collection_name, document_name)}
            if fn != "subject":
                kwargs["height"] = ht
            func(text, st.session_state[fn], **kwargs)
    
    add_logo_and_credits()
