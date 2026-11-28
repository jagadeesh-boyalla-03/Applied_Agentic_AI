# program 1: AI Mentor Application Using MCP

# Libraries
import streamlit as st
import pandas as pd

from mcpserver1 import add_student, list_students, students, delete_student,student_advice

st.title("AI Student Mentor")

# student records
st.subheader("Student Records")

st.dataframe(
    [{"id": key, **value} for key, value in students.items()]
)

st.subheader("Add Student")

with st.form("add"):
    sid = st.text_input("Enter the Student Id")
    name = st.text_input("Enter the student name")
    score = st.number_input("Enter the Python subject score", 0, 100, 40)

    if st.form_submit_button("ADD STUDENT"):
        st.write(add_student(sid, name, int(score)))

# deleting the student record
sid = st.text_input("Enter the Student ID to delete")

if st.button("DELETE STUDENT"):
    st.write(delete_student(sid))

# listing the students
st.subheader("List of students")

if st.button("List students"):
    student_list = list_students()
    st.write(pd.DataFrame(student_list))


#using llm for advice
st.subheader("Advice to student")

sid = st.text_input("Enter student id for advice")

if st.button("ADVICE"):
    advice = student_advice(sid)
    st.write(advice)