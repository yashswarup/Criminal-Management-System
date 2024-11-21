import streamlit as st
from db_connection import get_connection

def create_entry(table):
    st.subheader(f"Create Entry in {table}")
    conn = get_connection()
    cursor = conn.cursor()

    if table == "case_details":
        case_id = st.text_input("Case_ID")
        case_description = st.text_area("Case_Description")
        case_status = st.selectbox("Case_Status", ["Open", "Closed"])
        date_open = st.date_input("Date_Open")
        date_close = st.date_input("Date_Close", value=None)

        if st.button("Add Case"):
            cursor.execute("INSERT INTO case_details (Case_ID, Case_Description, Case_Status, Date_Open, Date_Close) VALUES (%s, %s, %s, %s, %s)",(case_id, case_description, case_status, date_open, date_close))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "court_hearing":
        hearing_id = st.text_input("Hearing ID")
        case_id = st.text_input("Case ID")
        hearing_date = st.date_input("Hearing Date")
        verdict = st.selectbox("Verdict", ["Pending", "Guilty", "Not Guilty"])

        if st.button("Add Hearing"):
            cursor.execute("INSERT INTO court_hearing (Hearing_ID, Case_ID, Hearing_Date, Verdict) VALUES (%s, %s, %s, %s)", (hearing_id, case_id, hearing_date, verdict))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "crime":
        crime_id = st.text_input("Crime ID")
        criminal_id = st.text_input("Criminal ID")
        crime_type = st.text_input("Crime Type")
        crime_date = st.date_input("Crime Date")

        if st.button("Add Crime"):
            cursor.execute("INSERT INTO crime (crime_id, criminal_id, crime_type, crime_date) VALUES (%s, %s, %s, %s)", (crime_id, criminal_id, crime_type, crime_date))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "criminal":
        case_id = st.text_input("Case id")
        criminal_no = st.text_input("Criminal No")
        criminal_name = st.text_input("Criminal Name")
        nick_name = st.text_input("Nick Name")
        arrest_date = st.date_input("Arrest Date")
        date_of_crime = st.date_input("Date of Crime")
        address = st.text_area("Address")
        age = st.number_input("Age", min_value=0)
        occupation = st.text_input("Occupation")
        birth_mark = st.text_area("Birth Mark")
        crime_type = st.text_input("Crime Type")
        father_name = st.text_input("Father's Name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        wanted = st.selectbox("Wanted", ["Yes", "No"])

        if st.button("Add Criminal"):
            cursor.execute("INSERT INTO criminal (Criminal_no, Criminal_name, Nick_name, arrest_date, dateOfcrime, address, age, occupation, BirthMark, crimetype, fatherName, gender, wanted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (criminal_no, criminal_name, nick_name, arrest_date, date_of_crime, address, age, occupation, birth_mark, crime_type, father_name, gender, wanted))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "criminal_family":
        family_id = st.text_input("Family ID")
        criminal_id = st.text_input("Criminal ID")
        family_member_name = st.text_input("Family Member Name")
        relationship = st.text_input("Relationship")

        if st.button("Add Family Member"):
            cursor.execute("INSERT INTO criminal_family (family_id, criminal_id, family_member_name, relationship) VALUES (%s, %s, %s, %s)", (family_id, criminal_id, family_member_name, relationship))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "lawyer":
        lawyer_id = st.text_input("Lawyer ID")
        criminal_id = st.text_input("Criminal ID")
        lawyer_name = st.text_input("Lawyer Name")
        specialization = st.text_input("Specialization")

        if st.button("Add Lawyer"):
            cursor.execute("INSERT INTO lawyer (lawyer_id, criminal_id, lawyer_name, specialization) VALUES (%s, %s, %s, %s)", (lawyer_id, criminal_id, lawyer_name, specialization))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "victim":
        victim_id = st.text_input("Victim ID")
        name = st.text_input("Name")
        address = st.text_area("Address")
        contact_info = st.text_input("Contact Info")

        if st.button("Add Victim"):
            cursor.execute("INSERT INTO victim (Victim_ID, Name, Address, Contact_Info) VALUES (%s, %s, %s, %s)", (victim_id, name, address, contact_info))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "witness":
        witness_id = st.text_input("Witness ID")
        name = st.text_input("Name")
        contact_info = st.text_input("Contact Info")

        if st.button("Add Witness"):
            cursor.execute("INSERT INTO witness (Witness_ID, Name, Contact_Info) VALUES (%s, %s, %s)", (witness_id, name, contact_info))
            conn.commit()
            st.success("Entry added successfully")

    elif table == "evidence":
        evidence_id = st.text_input("Evidence ID")
        crime_id = st.text_input("Crime ID")
        evidence_type = st.text_input("Evidence Type")
        description = st.text_area("Description")
        date_collected = st.date_input("Date Collected")
        location_found = st.text_area("Location Found")

        if st.button("Add Evidence"):
            cursor.execute("INSERT INTO evidence (evidence_id, crime_id, evidence_type, description, date_collected, location_found) VALUES (%s, %s, %s, %s, %s, %s)", (evidence_id, crime_id, evidence_type, description, date_collected, location_found))
            conn.commit()
            st.success("Entry added successfully")

    conn.close()
