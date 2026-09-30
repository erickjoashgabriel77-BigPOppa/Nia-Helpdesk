import os
import sys

# Force parent/root directory into sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

# Safe import for utils
try:
    import utils
    get_employee_by_id = utils.get_employee_by_id
except ImportError:
    from .. import utils
    get_employee_by_id = utils.get_employee_by_id


def render_login_screen():
    st.title("🔑 NIA IT Helpdesk")

    emp_tab, admin_tab = st.tabs(["👤 Employee Login", "🛡️ Admin Access"])

    with emp_tab:
        emp_id = st.text_input("Enter Employee ID", key="emp_id_input")
        if st.button("Log In", key="emp_login_btn", type="primary"):
            if emp_id.strip():
                try:
                    employee = get_employee_by_id(emp_id.strip())
                    if employee:
                        st.session_state["user"] = employee
                        st.session_state["role"] = "employee"
                        st.success(f"Welcome back, {employee.get('name', 'Employee')}!")
                        st.rerun()
                    else:
                        st.error("Employee ID not found. Please check and try again.")
                except Exception as e:
                    st.error(f"Database error: {e}")
            else:
                st.warning("Please enter your Employee ID.")

    with admin_tab:
        passkey = st.text_input("Enter Admin Passkey", type="password", key="admin_pass_input")
        if st.button("Access Admin Portal", key="admin_login_btn"):
            actual_passkey = st.secrets.get("ADMIN_PASSKEY", "ADMIN2026")
            if passkey == actual_passkey:
                st.session_state["user"] = {"name": "Administrator", "role": "admin"}
                st.session_state["role"] = "admin"
                st.success("Admin authenticated successfully!")
                st.rerun()
            else:
                st.error("Invalid Admin Passkey.")