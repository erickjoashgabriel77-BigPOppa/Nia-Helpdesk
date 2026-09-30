import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils import submit_ticket


def render_client_dashboard():
    user = st.session_state["user"]

    st.sidebar.title(f"👤 {user.get('name', 'Employee')}")
    st.sidebar.caption(f"Employee ID: {user.get('employee_id', 'N/A')}")
    if st.sidebar.button("Log Out", type="secondary"):
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.rerun()

    st.title("📝 Submit IT Helpdesk Ticket")

    with st.form("ticket_form", clear_on_submit=True):
        issue_type = st.selectbox(
            "Issue Category",
            ["Hardware", "Software / Software License", "Network / Internet", "Printer", "Account Access / Password", "Other"]
        )
        priority = st.select_slider("Priority Level", options=["Low", "Medium", "High", "Urgent"])
        description = st.text_area("Describe the issue in detail")

        submitted = st.form_submit_button("Submit Ticket", type="primary")
        if submitted:
            if description.strip():
                result = submit_ticket(user.get("employee_id"), issue_type, description, priority)
                if result:
                    st.success("Ticket submitted successfully! IT support staff will review it shortly.")
            else:
                st.warning("Please provide a description of the issue.")