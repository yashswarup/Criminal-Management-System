import streamlit as st
from create import create_entry
from read import read_entries
from update import update_entry
from delete import delete_entry
from login import login
from signup import signup
from db_connection import get_connection

def set_background(image_file):
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("file:///{image_file}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def search_data(table, column, search_term):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM {table} WHERE {column} LIKE %s"
        cursor.execute(query, ('%' + search_term + '%',))
        results = cursor.fetchall()
        return results
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

def view_all_records(table):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

def get_case_summary(case_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM case_details WHERE Case_ID = %s"
        cursor.execute(query, (case_id,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def add_crime(crime_type, crime_date, criminal_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("add_crime", (crime_type, crime_date, criminal_id))
        conn.commit()
        st.success("Crime added successfully.")
    except Exception as e:
        st.error(f"Failed to add crime: {e}")
    finally:
        conn.close()

def update_criminal_info(criminal_id, new_name, new_dob, new_address):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("update_criminal_info", (criminal_id, new_name, new_dob, new_address))
        conn.commit()
        st.success("Criminal information updated successfully.")
    except Exception as e:
        st.error(f"Failed to update criminal info: {e}")
    finally:
        conn.close()

def get_total_cases_for_criminal(criminal_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT get_total_criminal_cases(%s);", (criminal_id,))
        total_cases = cursor.fetchone()[0]
        return total_cases
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def main():
    # Set `bgnd.jpg` as the background for the entire app
    set_background("bgnd.jpg")
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Criminal Management System</h1>", unsafe_allow_html=True)

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Login"

    # Sidebar Navigation
    st.sidebar.title("Criminal Management System")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    if not st.session_state["logged_in"]:
        # Sidebar content for Login/Signup pages
        st.sidebar.markdown("Welcome to the Criminal Management System. Please log in to manage records.")

        # Links for Login and Signup
        if st.session_state["current_page"] == "Login":
            st.sidebar.write("Don't have an account? [Sign up here](#signup)")
            if st.sidebar.button("Go to Signup", key="sidebar_signup"):
                st.session_state["current_page"] = "Signup"
        elif st.session_state["current_page"] == "Signup":
            st.sidebar.write("Already have an account? [Log in here](#login)")
            if st.sidebar.button("Go to Login", key="sidebar_login"):
                st.session_state["current_page"] = "Login"

        # Display login or signup form
        if st.session_state["current_page"] == "Login":
            login()
        elif st.session_state["current_page"] == "Signup":
            signup()
    else:
        # Sidebar content for logged-in state
        st.sidebar.write(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
        if st.sidebar.button("Logout", key="logout"):
            # Clear session state values
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["role"] = ""
            st.session_state["current_page"] = "Login"

        # Choose table and operation
        table = st.sidebar.selectbox("Choose a table", ["case_details", "court_hearing", "crime", "criminal", "criminal_family", "lawyer", "victim", "witness", "evidence"])

        # Restrict operation choices based on role
        if st.session_state["role"] == "Admin":
            operation = st.sidebar.selectbox("Choose an operation", ["Create", "Read", "Update", "Delete", "View All Records", "Case Summary", "Get Total Cases"])
        elif st.session_state["role"] == "Operator":
            st.sidebar.write("Access restricted to read-only mode.")
            operation = "Read"  # Automatically set to Read for Operators

        # Execute CRUD operations and other actions
        if operation == "Create":
            create_entry(table)
        elif operation == "Read":
            read_entries(table)
        elif operation == "Update":
            update_entry(table)
        elif operation == "Delete":
            delete_entry(table)
        elif operation == "View All Records":
            results = view_all_records(table)
            if results:
                for row in results:
                    st.write(row)
            else:
                st.write("No records found.")
        elif operation == "Case Summary":
            case_id = st.text_input("Enter Case ID to View Summary")
            if case_id and st.button("View Summary"):
                case_summary = get_case_summary(case_id)
                if case_summary:
                    st.write(f"**Case Summary for Case ID {case_id}:**")
                    st.write(case_summary)
                else:
                    st.write("No case found with the provided Case ID.")
        elif operation == "Get Total Cases":
            criminal_id = st.number_input("Enter Criminal ID", min_value=1, step=1)
            if st.button("Get Total Cases"):
                total_cases = get_total_cases_for_criminal(criminal_id)
                st.write(f"Total Cases for Criminal {criminal_id}: {total_cases}")

if __name__ == "__main__":
    main()
