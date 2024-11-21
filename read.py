import streamlit as st
from db_connection import get_connection

def read_entries(table):
    st.subheader(f"Read Entries from {table}")
    conn = get_connection()
    cursor = conn.cursor()

    # Dynamically execute the query for the selected table
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()

    if rows:
        st.write(f"Data from {table} table:")

        # Loop through the rows to display each record
        for row in rows:
            with st.container():
                # Create columns for each field in the row
                columns = st.columns(len(row))  # Create a column for each field

                # Display each field with its respective label (column name)
                for idx, col in enumerate(row):
                    columns[idx].write(f"**{column_names[idx]}:** {col}")

                # Optional: Add a divider between rows
                st.divider()
    else:
        st.write("No data available.")

# Streamlit main function
def main():
    st.title("DBMS for Criminal Management System")

    # Dropdown to select a table
    table = st.selectbox(
        "Select Table to View Data",
        ["case_details", "court_hearing", "crime", "criminal", "criminal_family", "lawyer", "victim", "witness", "evidence"]
    )
    
    # Call the function to read and display entries from the selected table
    read_entries(table)

if __name__ == "__main__":
    main()
