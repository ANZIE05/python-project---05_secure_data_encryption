import streamlit as st
from utils import hash_passkey, encrypt_data, decrypt_data
from session_manager import initialize_session

# Initialize session
initialize_session()

st.title("🔐 Secure Data Encryption System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigate", menu)

# ------------------ Home Page ------------------ #
if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

# ------------------ Store Data ------------------ #
elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter the data to secure:")
    passkey = st.text_input("Enter a passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed = hash_passkey(passkey)
            encrypted = encrypt_data(user_data)
            st.session_state.stored_data[encrypted] = {"passkey": hashed}
            st.success("✅ Data encrypted and stored!")
            st.code(encrypted, language='text')
        else:
            st.error("⚠️ Both fields are required.")

# ------------------ Retrieve Data ------------------ #
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Encrypted Data")

    if not st.session_state.is_logged_in:
        st.warning("🔐 You must log in again after 3 failed attempts.")
        st.rerun()

    encrypted_input = st.text_area("Enter your encrypted text:")
    passkey_input = st.text_input("Enter your passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_input and passkey_input:
            hashed_input = hash_passkey(passkey_input)
            stored = st.session_state.stored_data.get(encrypted_input)

            if stored and stored["passkey"] == hashed_input:
                decrypted = decrypt_data(encrypted_input)
                st.success(f"✅ Decrypted Data: {decrypted}")
                st.session_state.failed_attempts = 0  # Reset on success
            else:
                st.session_state.failed_attempts += 1
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")

                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts. Please reauthorize.")
                    st.session_state.is_logged_in = False
                    st.rerun()
        else:
            st.error("⚠️ All fields are required.")

# ------------------ Login Page ------------------ #
elif choice == "Login":
    st.subheader("🔑 Reauthorization Login")
    login_input = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_input == "admin123":  # Change this in real app
            st.session_state.failed_attempts = 0
            st.session_state.is_logged_in = True
            st.success("✅ Logged in successfully. You may now retrieve data.")
        else:
            st.error("❌ Incorrect master password.")
