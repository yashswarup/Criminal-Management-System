import streamlit as st
from db_operations import get_user  # Assuming you have a function to retrieve users from a database

def login():
    st.title("Login")

    # Role selection for Admin or Operator
    role = st.radio("Select Role", ("Admin", "Operator"), key="role_selection").lower()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button and verification based on role
    if st.button("Login", key="login_button"):
        user = get_user(username)  # Fetch user data from the database

        # Check if user exists and password matches
        if user and user["password"] == password:
            user_role = user["role"].lower()  # Convert to lowercase for comparison
            if user_role == role:  # Verify if the selected role matches the user's actual role
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = role.capitalize()  # Store the role in capitalized form
                st.success(f"Welcome, {role.capitalize()} {username}!")
            else:
                st.error(f"Role mismatch. Expected role: {user['role']}, Selected role: {role.capitalize()}")
        else:
            st.error("Invalid username or password")

    # Redirect to Signup
    st.write("Don't have an account? Sign up here:")
    if st.button("Go to Signup", key="login_to_signup"):
        st.session_state["current_page"] = "Signup"
