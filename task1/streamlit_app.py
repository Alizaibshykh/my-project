import requests
import streamlit as st

API = "http://127.0.0.1:5001"
st.set_page_config(page_title="Student Management", page_icon="🎓", layout="wide")
st.title("Student Management System")
st.caption("Streamlit frontend connected to the Flask REST API")

def load_students():
    try:
        response = requests.get(f"{API}/students", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Cannot reach Flask. Start task1/app.py first. {exc}")
        return None

students = load_students()
if students is not None:
    st.subheader("All students")
    if students:
        st.dataframe(students, use_container_width=True, hide_index=True)
    else:
        st.info("No students yet. Add one below.")

    left, right = st.columns(2)
    with left:
        st.subheader("Add student")
        with st.form("add_form", clear_on_submit=True):
            sid = st.text_input("Student ID")
            name = st.text_input("Name")
            dept = st.text_input("Department")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Add student")
            if submitted:
                try:
                    res = requests.post(f"{API}/students", json={"student_id":sid,"name":name,"department":dept,"email":email}, timeout=5)
                    if res.status_code == 201:
                        st.success("Student added.")
                        st.rerun()
                    else:
                        st.error(res.json().get("error", "Could not add student"))
                except requests.RequestException as exc:
                    st.error(str(exc))

    with right:
        st.subheader("Update student")
        if students:
            choices = {f'{s["name"]} ({s["student_id"]}) – #{s["id"]}': s for s in students}
            label = st.selectbox("Select student", list(choices), key="edit_choice")
            selected = choices[label]
            with st.form("edit_form"):
                sid = st.text_input("Student ID", selected["student_id"])
                name = st.text_input("Name", selected["name"])
                dept = st.text_input("Department", selected["department"])
                email = st.text_input("Email", selected["email"])
                submitted = st.form_submit_button("Update student")
                if submitted:
                    try:
                        res = requests.put(f'{API}/students/{selected["id"]}', json={"student_id":sid,"name":name,"department":dept,"email":email}, timeout=5)
                        if res.ok:
                            st.success("Student updated.")
                            st.rerun()
                        else:
                            st.error(res.json().get("error", "Could not update student"))
                    except requests.RequestException as exc:
                        st.error(str(exc))
        else:
            st.info("Add a student first.")

    st.divider()
    st.subheader("Delete student")
    if students:
        choices = {f'{s["name"]} ({s["student_id"]}) – #{s["id"]}': s for s in students}
        label = st.selectbox("Choose student", list(choices), key="delete_choice")
        if st.button("Delete selected student"):
            try:
                res = requests.delete(f'{API}/students/{choices[label]["id"]}', timeout=5)
                if res.ok:
                    st.success("Student deleted.")
                    st.rerun()
                else:
                    st.error(res.json().get("error", "Could not delete student"))
            except requests.RequestException as exc:
                st.error(str(exc))
