import streamlit as st
from db_operations import create_user

def signup():
    st.title("Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin", "operator"])

    if st.button("Signup"):
        create_user(username, password, role)
        st.success(f"Account created successfully for '{username}'!")
    
    # Redirect to Login
    st.write("Already have an account? Login here:")
    if st.button("Go to Login"):
        st.session_state["current_page"] = "Login"
