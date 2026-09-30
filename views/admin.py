import sys
from pathlib import Path

# Add project root directory to sys.path at position 0
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

try:
    import utils
except ImportError:
    from .. import utils

get_all_tickets = utils.get_all_tickets
update_ticket_status = utils.update_ticket_status


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