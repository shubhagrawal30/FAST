import streamlit as st
from interface import interface
from tutor import tutor

if __name__ == "__main__":
    if "tutor" not in st.session_state:
        st.session_state.tutor = tutor.Tutor("physics")
    if "interface" not in st.session_state:
        st.session_state.interface = interface.Interface(st.session_state.tutor)
    st.session_state.interface.main() 