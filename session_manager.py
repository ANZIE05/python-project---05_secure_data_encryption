import streamlit as st

def initialize_session():
    if "stored_data" not in st.session_state:
        st.session_state.stored_data = {}  # key: encrypted_text, value: {"passkey": hashed_passkey}

    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0

    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = True
