import streamlit as st
from db_connection import get_connection

def delete_entry(table):
    st.subheader(f"Delete Entry from {table}")
    conn = get_connection()
    cursor = conn.cursor()

    if table == "case_details":
        case_id = st.text_input("Case ID")

        if st.button("Delete Case"):
            cursor.execute("DELETE FROM case_details WHERE Case_ID = %s", (case_id,))
            conn.commit()
            st.success("Case deleted successfully")

    elif table == "court_hearing":
        hearing_id = st.text_input("Hearing ID")

        if st.button("Delete Hearing"):
            cursor.execute("DELETE FROM court_hearing WHERE Hearing_ID = %s", (hearing_id,))
            conn.commit()
            st.success("Court hearing deleted successfully")

    elif table == "crime":
        crime_id = st.text_input("Crime ID")

        if st.button("Delete Crime"):
            cursor.execute("DELETE FROM crime WHERE crime_id = %s", (crime_id,))
            conn.commit()
            st.success("Crime deleted successfully")

    elif table == "criminal":
        criminal_no = st.text_input("Criminal Number")

        if st.button("Delete Criminal"):
            cursor.execute("DELETE FROM criminal WHERE Criminal_no = %s", (criminal_no,))
            conn.commit()
            st.success("Criminal deleted successfully")

    elif table == "criminal_family":
        family_id = st.text_input("Family ID")

        if st.button("Delete Family Member"):
            cursor.execute("DELETE FROM criminal_family WHERE family_id = %s", (family_id,))
            conn.commit()
            st.success("Family member deleted successfully")

    elif table == "lawyer":
        lawyer_id = st.text_input("Lawyer ID")

        if st.button("Delete Lawyer"):
            cursor.execute("DELETE FROM lawyer WHERE Lawyer_id = %s", (lawyer_id,))
            conn.commit()
            st.success("Lawyer deleted successfully")

    elif table == "victim":
        victim_id = st.text_input("Victim ID")

        if st.button("Delete Victim"):
            cursor.execute("DELETE FROM victim WHERE Victim_ID = %s", (victim_id,))
            conn.commit()
            st.success("Victim deleted successfully")

    elif table == "witness":
        witness_id = st.text_input("Witness ID")

        if st.button("Delete Witness"):
            cursor.execute("DELETE FROM witness WHERE Witness_ID = %s", (witness_id,))
            conn.commit()
            st.success("Witness deleted successfully")

    elif table == "evidence":
        evidence_id = st.text_input("Evidence ID")

        if st.button("Delete Evidence"):
            cursor.execute("DELETE FROM evidence WHERE evidence_id = %s", (evidence_id,))
            conn.commit()
            st.success("Evidence deleted successfully")

    conn.close()
