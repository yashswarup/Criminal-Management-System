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

# Function to execute join query
def execute_join_query():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT 
            criminal.Criminal_no,
            criminal.Criminal_name,
            criminal.age,
            criminal.gender,
            COUNT(DISTINCT crime.crime_id) AS total_crimes,
            GROUP_CONCAT(DISTINCT crime.crime_type) AS crimes_committed,
            GROUP_CONCAT(DISTINCT case_details.Case_Description) AS case_descriptions,
            GROUP_CONCAT(DISTINCT court_hearing.Verdict) AS verdicts
        FROM 
            criminal
        JOIN 
            crime ON criminal.Criminal_no = crime.criminal_id
        JOIN 
            case_details ON criminal.Case_id = case_details.Case_ID
        LEFT JOIN 
            court_hearing ON case_details.Case_ID = court_hearing.Case_ID
        GROUP BY 
            criminal.Criminal_no, criminal.Criminal_name, criminal.age, criminal.gender;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        st.error(f"Error executing join query: {e}")
        return []

# Function to execute nested query
def execute_nested_query():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT Criminal_no, Criminal_name
        FROM criminal
        WHERE Criminal_no IN (
            SELECT criminal_id
            FROM crime
            GROUP BY criminal_id
            HAVING COUNT(DISTINCT crime_type) > 1
        );
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        st.error(f"Error executing nested query: {e}")
        return []

# Function to execute aggregate query
def execute_aggregate_query():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT crime_type, COUNT(*) AS crime_count
        FROM crime
        GROUP BY crime_type
        ORDER BY crime_count DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        st.error(f"Error executing aggregate query: {e}")
        return []


# Function to display aggregate query results
def display_aggregate_query_results():
    st.subheader("Crime Type Frequency")
    results = execute_aggregate_query()
    for row in results:
        st.write(f"Crime Type: {row[0]}, Count: {row[1]}")
        st.write("------")

# Function to search data
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

# Function to view all records in a table
def view_all_records(table):
    st.subheader(f"View All Records from {table}")
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            column_names = [desc[0] for desc in cursor.description]
            st.write(f"Data from {table} table:")

            for row in results:
                with st.container():
                    columns = st.columns(len(row))  # Create a column for each field in the row
                    for idx, col in enumerate(row):
                        columns[idx].write(f"**{column_names[idx]}:** {col}")
                    st.divider()  # Divider between rows
        else:
            st.write("No records found.")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

# Function to get case summary
def get_case_summary(case_id):
    st.subheader(f"Case Summary for Case ID: {case_id}")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT * FROM case_details WHERE Case_ID = %s"
        cursor.execute(query, (case_id,))
        result = cursor.fetchone()

        if result:
            column_names = [desc[0] for desc in cursor.description]
            st.write(f"Case Summary for Case ID: {case_id}")

            with st.container():
                columns = st.columns(len(result))  # Create a column for each field in the result
                for idx, col in enumerate(result):
                    columns[idx].write(f"**{column_names[idx]}:** {col}")
        else:
            st.write(f"No case found with Case ID: {case_id}")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

# Function to add a new crime
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

# Function to update criminal info
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

# Function to get total cases for a criminal
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
    set_background("bgnd.jpg")
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Criminal Management System</h1>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Login"

    st.sidebar.title("Criminal Management System")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    if not st.session_state["logged_in"]:
        if st.session_state["current_page"] == "Login":
            st.sidebar.write("Don't have an account? [Sign up here](#signup)")
            if st.sidebar.button("Go to Signup", key="sidebar_signup"):
                st.session_state["current_page"] = "Signup"
        elif st.session_state["current_page"] == "Signup":
            st.sidebar.write("Already have an account? [Log in here](#login)")
            if st.sidebar.button("Go to Login", key="sidebar_login"):
                st.session_state["current_page"] = "Login"

        if st.session_state["current_page"] == "Login":
            login()
        elif st.session_state["current_page"] == "Signup":
            signup()
    else:
        st.sidebar.write(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
        if st.sidebar.button("Logout", key="logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.session_state["role"] = ""
            st.session_state["current_page"] = "Login"

        table = st.sidebar.selectbox("Choose a table", ["criminal", "criminal_family", "case_details", "crime", "evidence", "court_hearing", "lawyer", "victim", "witness"])

        if st.session_state["role"] == "Admin":
            operation = st.sidebar.selectbox("Choose an operation", ["Create", "Read", "Update", "Delete", "View All Records", "Case Summary", "Get Total Cases", "Aggregate Query"])
        elif st.session_state["role"] == "Operator":
            st.sidebar.write("Access restricted to read-only mode.")
            operation = "Read"

        if operation == "Create":
            create_entry(table)
        elif operation == "Read":
            read_entries(table)
        elif operation == "Update":
            update_entry(table)
        elif operation == "Delete":
            delete_entry(table)
        elif operation == "View All Records":
            records = view_all_records(table)
            for record in records:
                st.write(record)
        elif operation == "Case Summary":
            case_id = st.text_input("Enter Case ID to View Summary")
            if case_id and st.button("View Summary"):
                summary = get_case_summary(case_id)
                st.write(summary)
        elif operation == "Get Total Cases":
            criminal_id = st.number_input("Enter Criminal ID", min_value=1, step=1)
            if st.button("Get Total Cases"):
                total_cases = get_total_cases_for_criminal(criminal_id)
                st.write(f"Total Cases for Criminal {criminal_id}: {total_cases}")
        elif operation == "Aggregate Query":
            display_aggregate_query_results()

if __name__ == "__main__":
    main()
