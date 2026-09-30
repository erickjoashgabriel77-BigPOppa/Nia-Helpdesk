import datetime
import streamlit as st
import streamlit.components.v1 as components
from utils import save_local_data, generate_printable_ticket_html

def render_client_views(selected_menu):
    """Renders client-side ticket submission, tracking, rating, and printing."""
    emp = st.session_state.logged_in_employee

    if not emp:
        st.error("No active employee session found. Please log in.")
        return

    st.title(f"Welcome, {emp['name']}")
    st.caption(f"Section: {emp['section']} | Unit: {emp['unit']} | Employee ID: {emp['id']}")
    st.markdown("---")

    if selected_menu == "📝 Create Ticket":
        st.subheader("📝 Submit a New IT Service Request")

        with st.form("create_ticket_form", clear_on_submit=True):
            category = st.selectbox(
                "Select Issue Category:",
                [
                    "Hardware / Workstation",
                    "Software & Applications",
                    "Network & Internet",
                    "Printer & Scanners",
                    "User Accounts & Passwords",
                    "Other Technical Assistance"
                ]
            )

            description = st.text_area(
                "Detailed Description of the Issue:",
                placeholder="Describe the technical issue, computer error message, or assistance required..."
            )

            submitted = st.form_submit_button("Submit Request ➔", type="primary", use_container_width=True)

            if submitted:
                if not description.strip():
                    st.error("Please enter a detailed description of your issue before submitting.")
                else:
                    new_id = f"TIC-{st.session_state.ticket_counter}"
                    st.session_state.ticket_counter += 1

                    new_ticket = {
                        "id": new_id,
                        "employee_id": emp["id"],
                        "employee_name": emp["name"],
                        "section": emp["section"],
                        "unit": emp["unit"],
                        "category": category,
                        "description": description.strip(),
                        "status": "Pending",
                        "date": datetime.date.today().strftime("%Y-%m-%d"),
                        "assigned_tech": "Unassigned",
                        "resolution_notes": "Pending inspection by IT staff.",
                        "rating": None,
                        "feedback": ""
                    }

                    st.session_state.tickets.insert(0, new_ticket)
                    save_local_data()
                    st.success(f"Ticket **{new_id}** submitted successfully! Our IT team has been notified.")
                    st.rerun()

    elif selected_menu == "📋 My Tickets & Rate Service":
        st.subheader("📋 My Submitted Tickets & Service History")

        my_tickets = [
            t for t in st.session_state.tickets
            if t.get("employee_id") == emp["id"]
        ]

        if not my_tickets:
            st.info("You have not submitted any technical support tickets yet.")
            return

        for ticket in my_tickets:
            status_symbol = {
                "Pending": "🟡",
                "In Progress": "🔵",
                "Resolved": "🟢",
                "Cancelled": "🔴"
            }.get(ticket.get("status", "Pending"), "⚪")

            expander_title = f"{status_symbol} Ticket #{ticket['id']} — {ticket['category']} ({ticket['status']})"

            with st.expander(expander_title):
                st.write(f"**Date Created:** {ticket.get('date', ticket.get('created_at', 'N/A'))}")
                st.write(f"**Issue Description:** {ticket.get('description', '')}")
                st.write(f"**Assigned Technician:** `{ticket.get('assigned_tech', 'Unassigned')}`")
                st.write(f"**Resolution Notes:** {ticket.get('resolution_notes', 'N/A')}")

                st.markdown("---")
                col1, col2 = st.columns(2)

                with col1:
                    if ticket.get("status") == "Pending":
                        if st.button("❌ Cancel Ticket", key=f"cancel_{ticket['id']}"):
                            ticket["status"] = "Cancelled"
                            save_local_data()
                            st.warning(f"Ticket {ticket['id']} has been cancelled.")
                            st.rerun()

                with col2:
                    if st.button("🖨️ Print Service Slip", key=f"print_{ticket['id']}"):
                        key_state = f"show_print_{ticket['id']}"
                        st.session_state[key_state] = not st.session_state.get(key_state, False)

                if st.session_state.get(f"show_print_{ticket['id']}", False):
                    st.markdown("---")
                    st.caption("📄 **ISO Printable Service Slip Preview:**")
                    html_code = generate_printable_ticket_html(ticket)
                    components.html(html_code, height=850, scrolling=True)

                if ticket.get("status") in ["Resolved", "Closed"]:
                    st.markdown("---")
                    st.subheader("⭐ Rate Completed Service")

                    current_rating = ticket.get("rating")
                    if current_rating:
                        st.success(f"You rated this service: **{current_rating} Stars** ⭐")
                        if ticket.get("feedback"):
                            st.caption(f"Feedback: *\"{ticket['feedback']}\"*")
                    else:
                        with st.form(f"rating_form_{ticket['id']}"):
                            rating = st.slider("Service Satisfaction (1 = Poor, 5 = Excellent):", 1, 5, 5)
                            feedback = st.text_input("Feedback / Comments (Optional):")
                            if st.form_submit_button("Submit Rating"):
                                ticket["rating"] = rating
                                ticket["feedback"] = feedback
                                save_local_data()
                                st.success("Thank you for your feedback!")
                                st.rerun()