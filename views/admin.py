import streamlit as st
import streamlit.components.v1 as components
from config import EOS_SECTION, AFS_SECTION, ORGANIZATIONAL_UNITS, IT_TECHNICIANS
from utils import save_local_data, generate_printable_ticket_html

def render_admin_views(selected_menu):
    """Renders IT admin dashboard for ticket management and directory."""
    st.title("🛡️ IT Admin Management Console")
    st.markdown("---")

    if selected_menu == "📊 Ticket Management Dashboard":
        st.subheader("Central Ticket Queue")

        # Top-level metrics
        total = len(st.session_state.tickets)
        pending = sum(1 for t in st.session_state.tickets if t.get("status") in ["Pending", "In Progress"])
        resolved = sum(1 for t in st.session_state.tickets if t.get("status") in ["Resolved", "Closed"])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tickets", total)
        m2.metric("Active / Pending", pending)
        m3.metric("Resolved / Closed", resolved)
        st.markdown("---")

        # Filtering options
        f_col1, f_col2 = st.columns(2)
        status_filter = f_col1.selectbox("Filter by Status:", ["All", "Pending", "In Progress", "Resolved", "Cancelled", "Closed"])
        sec_filter = f_col2.selectbox("Filter by Section:", ["All", EOS_SECTION, AFS_SECTION])

        filtered_tickets = st.session_state.tickets
        if status_filter != "All":
            filtered_tickets = [t for t in filtered_tickets if t.get("status") == status_filter]
        if sec_filter != "All":
            filtered_tickets = [t for t in filtered_tickets if t.get("section") == sec_filter]

        if not filtered_tickets:
            st.info("No tickets match the current filters.")

        # Display Ticket Queue
        for ticket in filtered_tickets:
            status_emoji = {
                "Pending": "🟡", 
                "In Progress": "🔵", 
                "Resolved": "🟢", 
                "Closed": "🟢",
                "Cancelled": "🔴"
            }.get(ticket.get("status", "Pending"), "⚪")
            
            with st.expander(f"{status_emoji} {ticket['id']} - {ticket['category']} | {ticket.get('employee_name')} ({ticket.get('status', 'Unknown')})"):
                st.write(f"**Date Submitted:** {ticket.get('date')} | **Unit:** {ticket.get('unit')}")
                st.write(f"**Client Description:** {ticket.get('description')}")
                st.markdown("---")
                
                # Update Form
                with st.form(f"admin_update_{ticket['id']}"):
                    # Safely handle the status index to prevent ValueErrors
                    allowed_statuses = ["Pending", "In Progress", "Resolved", "Cancelled", "Closed"]
                    current_status = ticket.get("status", "Pending")
                    
                    # If a legacy status exists in the JSON, append it so the UI doesn't crash
                    if current_status not in allowed_statuses:
                        allowed_statuses.append(current_status)
                        
                    new_status = st.selectbox(
                        "Update Status:", 
                        allowed_statuses, 
                        index=allowed_statuses.index(current_status)
                    )
                    
                    # Safely handle assigned_tech index
                    tech_index = 0
                    if ticket.get("assigned_tech") in IT_TECHNICIANS:
                        tech_index = IT_TECHNICIANS.index(ticket.get("assigned_tech"))
                        
                    new_tech = st.selectbox("Assign IT Technician:", IT_TECHNICIANS, index=tech_index)
                    new_notes = st.text_area("Resolution / IT Notes:", value=ticket.get("resolution_notes", ""))
                    
                    submitted = st.form_submit_button("Update Ticket", type="primary")
                    if submitted:
                        ticket["status"] = new_status
                        ticket["assigned_tech"] = new_tech
                        ticket["resolution_notes"] = new_notes
                        save_local_data()
                        st.success(f"Ticket {ticket['id']} updated successfully!")
                        st.rerun()

                # Print ISO Slip Button
                if st.button("🖨️ Print Service Slip", key=f"print_admin_{ticket['id']}"):
                    st.session_state[f"show_admin_print_{ticket['id']}"] = not st.session_state.get(f"show_admin_print_{ticket['id']}", False)

                if st.session_state.get(f"show_admin_print_{ticket['id']}", False):
                    st.markdown("---")
                    st.caption("📄 **Printable Service Slip Preview:**")
                    html_code = generate_printable_ticket_html(ticket)
                    components.html(html_code, height=520, scrolling=True)

    elif selected_menu == "👥 Employee / Client Management":
        st.subheader("Registered Employee Directory")
        
        # Add New Employee Form
        with st.expander("➕ Register New Employee", expanded=False):
            with st.form("new_employee_form", clear_on_submit=True):
                emp_name = st.text_input("Full Name (e.g., Juan Dela Cruz)")
                emp_section = st.selectbox("Section", [EOS_SECTION, AFS_SECTION])
                
                # Combine units for simple dropdown selection
                all_units = ORGANIZATIONAL_UNITS[EOS_SECTION] + ORGANIZATIONAL_UNITS[AFS_SECTION]
                emp_unit = st.selectbox("Unit / Division", all_units)
                
                if st.form_submit_button("Register Employee", type="primary"):
                    if not emp_name:
                        st.error("Employee Name is required.")
                    else:
                        prefix = "EOS" if emp_section == EOS_SECTION else "AFS"
                        new_id = f"EMP-{prefix}-{(len(st.session_state.employees) + 1):03d}"
                        
                        st.session_state.employees.append({
                            "id": new_id,
                            "name": emp_name.strip(),
                            "section": emp_section,
                            "unit": emp_unit
                        })
                        save_local_data()
                        st.success(f"Employee {emp_name} registered successfully with ID: {new_id}")
                        st.rerun()

        st.markdown("---")
        
        # Display Existing Employees list
        if st.session_state.employees:
            for emp in st.session_state.employees:
                with st.container(border=True):
                    st.markdown(f"**{emp['name']}**")
                    st.caption(f"ID: `{emp['id']}` | {emp['section']} - {emp['unit']}")
        else:
            st.info("No employees registered yet.")