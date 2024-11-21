import streamlit as st
from db_connection import get_connection

def update_entry(table):
    st.subheader(f"Update Entry in {table}")
    conn = get_connection()
    cursor = conn.cursor()

    if table == "case_details":
        case_id = st.text_input("Case ID")
        new_description = st.text_area("New Case Description")
        new_status = st.selectbox("New Case Status", ["Open", "Closed"])
        new_date_open = st.date_input("New Date Open")
        new_date_close = st.date_input("New Date Close")

        if st.button("Update Case"):
            cursor.execute("UPDATE case_details SET Case_Description = %s, Case_Status = %s, Date_Open = %s, Date_Close = %s WHERE Case_ID = %s", 
                           (new_description, new_status, new_date_open, new_date_close, case_id))
            conn.commit()
            st.success("Case details updated successfully")

    elif table == "court_hearing":
        hearing_id = st.text_input("Hearing ID")
        new_hearing_date = st.date_input("New Hearing Date")
        new_verdict = st.selectbox("New Verdict", ["Pending", "Guilty", "Not Guilty"])

        if st.button("Update Hearing"):
            cursor.execute("UPDATE court_hearing SET Hearing_Date = %s, Verdict = %s WHERE Hearing_ID = %s", 
                           (new_hearing_date, new_verdict, hearing_id))
            conn.commit()
            st.success("Court hearing details updated successfully")

    elif table == "crime":
        crime_id = st.text_input("Crime ID")
        new_crime_type = st.text_input("New Crime Type")
        new_crime_date = st.date_input("New Crime Date")

        if st.button("Update Crime"):
            cursor.execute("UPDATE crime SET crime_type = %s, crime_date = %s WHERE crime_id = %s", 
                           (new_crime_type, new_crime_date, crime_id))
            conn.commit()
            st.success("Crime details updated successfully")

    elif table == "criminal":
        criminal_no = st.text_input("Criminal Number")
        new_name = st.text_input("New Criminal Name")
        new_nickname = st.text_input("New Nickname")
        new_arrest_date = st.date_input("New Arrest Date")
        new_date_of_crime = st.date_input("New Date of Crime")
        new_address = st.text_input("New Address")
        new_age = st.number_input("New Age", min_value=0, max_value=120)
        new_occupation = st.text_input("New Occupation")
        new_birthmark = st.text_input("New Birthmark")
        new_crimetype = st.text_input("New Crime Type")
        new_father_name = st.text_input("New Father Name")
        new_gender = st.selectbox("New Gender", ["Male", "Female"])
        new_wanted = st.selectbox("New Wanted Status", ["Yes", "No"])

        if st.button("Update Criminal"):
            cursor.execute("""
                UPDATE criminal SET Criminal_name = %s, Nick_name = %s, arrest_date = %s, dateOfcrime = %s, address = %s, 
                age = %s, occupation = %s, BirthMark = %s, crimetype = %s, fatherName = %s, gender = %s, wanted = %s 
                WHERE Criminal_no = %s
            """, (new_name, new_nickname, new_arrest_date, new_date_of_crime, new_address, new_age, 
                  new_occupation, new_birthmark, new_crimetype, new_father_name, new_gender, new_wanted, criminal_no))
            conn.commit()
            st.success("Criminal details updated successfully")

    elif table == "criminal_family":
        family_id = st.text_input("Family ID")
        new_family_member_name = st.text_input("New Family Member Name")
        new_relationship = st.text_input("New Relationship")

        if st.button("Update Family Member"):
            cursor.execute("UPDATE criminal_family SET family_member_name = %s, relationship = %s WHERE family_id = %s", 
                           (new_family_member_name, new_relationship, family_id))
            conn.commit()
            st.success("Criminal family details updated successfully")

    elif table == "lawyer":
        lawyer_id = st.text_input("Lawyer ID")
        new_lawyer_name = st.text_input("New Lawyer Name")
        new_specialization = st.text_input("New Specialization")

        if st.button("Update Lawyer"):
            cursor.execute("UPDATE lawyer SET Lawyer_name = %s, specialization = %s WHERE Lawyer_id = %s", 
                           (new_lawyer_name, new_specialization, lawyer_id))
            conn.commit()
            st.success("Lawyer details updated successfully")

    elif table == "victim":
        victim_id = st.text_input("Victim ID")
        new_name = st.text_input("New Victim Name")
        new_address = st.text_input("New Address")
        new_contact_info = st.text_input("New Contact Info")

        if st.button("Update Victim"):
            cursor.execute("UPDATE victim SET Name = %s, Address = %s, Contact_Info = %s WHERE Victim_ID = %s", 
                           (new_name, new_address, new_contact_info, victim_id))
            conn.commit()
            st.success("Victim details updated successfully")

    elif table == "witness":
        witness_id = st.text_input("Witness ID")
        new_name = st.text_input("New Witness Name")
        new_contact_info = st.text_input("New Contact Info")

        if st.button("Update Witness"):
            cursor.execute("UPDATE witness SET Name = %s, Contact_Info = %s WHERE Witness_ID = %s", 
                           (new_name, new_contact_info, witness_id))
            conn.commit()
            st.success("Witness details updated successfully")

    elif table == "evidence":
        evidence_id = st.text_input("Evidence ID")
        new_evidence_type = st.text_input("New Evidence Type")
        new_description = st.text_area("New Description")
        new_date_collected = st.date_input("New Date Collected")
        new_location_found = st.text_input("New Location Found")

        if st.button("Update Evidence"):
            cursor.execute("""
                UPDATE evidence SET evidence_type = %s, description = %s, date_collected = %s, location_found = %s 
                WHERE evidence_id = %s
            """, (new_evidence_type, new_description, new_date_collected, new_location_found, evidence_id))
            conn.commit()
            st.success("Evidence details updated successfully")

    conn.close()
