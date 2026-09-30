import os
import sys

# Force root directory into sys.path before loading relative modules
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from views.auth import render_login_screen
from utils import submit_ticket, get_all_tickets, update_ticket_status

# Streamlit Page Setup
st.set_page_config(page_title="NIA IT Helpdesk", page_icon="🎫", layout="wide")


def render_employee_dashboard():
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


def render_admin_dashboard():
    st.sidebar.title("🛡️ Admin Panel")
    if st.sidebar.button("Log Out", type="secondary"):
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.rerun()

    st.title("📊 IT Helpdesk Management Portal")
    
    tickets = get_all_tickets()
    if not tickets:
        st.info("No submitted tickets found.")
        return

    st.subheader(f"Total Tickets Logged: {len(tickets)}")
    
    for ticket in tickets:
        ticket_id = ticket.get("id")
        status = ticket.get("status", "Open")
        priority = ticket.get("priority", "Normal")
        issue = ticket.get("issue_type", "General")
        
        with st.expander(f"Ticket #{ticket_id} — [{priority}] {issue} ({status})"):
            st.write(f"**Employee ID:** {ticket.get('employee_id')}")
            st.write(f"**Submitted Date:** {ticket.get('created_at')}")
            st.write(f"**Description:** {ticket.get('description')}")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                status_options = ["Open", "In Progress", "Resolved", "Closed"]
                current_index = status_options.index(status) if status in status_options else 0
                new_status = st.selectbox(
                    "Update Resolution Status",
                    status_options,
                    index=current_index,
                    key=f"status_{ticket_id}"
                )
            with col2:
                st.write(" ")
                st.write(" ")
                if st.button("Save Status", key=f"btn_{ticket_id}", type="primary"):
                    update_ticket_status(ticket_id, new_status)
                    st.success("Status updated!")
                    st.rerun()


def main():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None

    if st.session_state["user"] is None:
        render_login_screen()
    elif st.session_state["role"] == "employee":
        render_employee_dashboard()
    elif st.session_state["role"] == "admin":
        render_admin_dashboard()


if __name__ == "__main__":
    main()