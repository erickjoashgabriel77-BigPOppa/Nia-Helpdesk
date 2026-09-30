import streamlit as st
import streamlit.components.v1 as components
from config import EOS_SECTION, AFS_SECTION, ORGANIZATIONAL_UNITS, IT_TECHNICIANS
from utils import save_local_data, generate_printable_ticket_html

def render_admin_views(selected_menu):
    """Renders IT admin dashboard for ticket management, employee directory, and admin management."""
    st.title("🛡️ IT Admin Management Console")
    st.markdown("---")

    if selected_menu == "📊 Ticket Management Dashboard":
        st.subheader("Central Ticket Queue")

        total = len(st.session_state.tickets)
        pending = sum(1 for t in st.session_state.tickets if t.get("status") in ["Pending", "In Progress"])
        resolved = sum(1 for t in st.session_state.tickets if t.get("status") in ["Resolved", "Closed"])

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tickets", total)
        m2.metric("Active / Pending", pending)
        m3.metric("Resolved / Closed", resolved)
        st.markdown("---")

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
                
                with st.form(f"admin_update_{ticket['id']}"):
                    allowed_statuses = ["Pending", "In Progress", "Resolved", "Cancelled", "Closed"]
                    current_status = ticket.get("status", "Pending")
                    
                    if current_status not in allowed_statuses:
                        allowed_statuses.append(current_status)
                        
                    new_status = st.selectbox(
                        "Update Status:", 
                        allowed_statuses, 
                        index=allowed_statuses.index(current_status)
                    )
                    
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

                if st.button("🖨️ Print Service Slip", key=f"print_admin_{ticket['id']}"):
                    st.session_state[f"show_admin_print_{ticket['id']}"] = not st.session_state.get(f"show_admin_print_{ticket['id']}", False)

                if st.session_state.get(f"show_admin_print_{ticket['id']}", False):
                    st.markdown("---")
                    st.caption("📄 **Printable Service Slip Preview:**")
                    html_code = generate_printable_ticket_html(ticket)
                    components.html(html_code, height=520, scrolling=True)

    elif selected_menu == "👥 Employee / Client Management":
        st.subheader("Registered Employee Directory")
        
        with st.expander("➕ Register New Employee", expanded=False):
            emp_name = st.text_input("Full Name (e.g., Juan Dela Cruz)")
            
            # Direct encodable text input for Designation
            emp_designation = st.text_input("Designation / Position Title (e.g., Engineer A, Admin Aide VI)")

            emp_section = st.selectbox("Section", [EOS_SECTION, AFS_SECTION])
            available_units = ORGANIZATIONAL_UNITS.get(emp_section, [])
            emp_unit = st.selectbox("Unit / Division", available_units)
            
            if st.button("Register Employee", type="primary", key="btn_register_emp"):
                if not emp_name.strip():
                    st.error("Employee Name is required.")
                elif not emp_designation.strip():
                    st.error("Employee Designation / Position Title is required.")
                else:
                    prefix = "EOS" if emp_section == EOS_SECTION else "AFS"
                    new_id = f"EMP-{prefix}-{(len(st.session_state.employees) + 1):03d}"
                    
                    st.session_state.employees.append({
                        "id": new_id,
                        "name": emp_name.strip(),
                        "designation": emp_designation.strip(),
                        "section": emp_section,
                        "unit": emp_unit
                    })
                    save_local_data()
                    st.success(f"Employee **{emp_name.strip()}** ({emp_designation.strip()}) registered successfully with ID: `{new_id}`")
                    st.rerun()

        st.markdown("---")
        
        if st.session_state.employees:
            for emp in st.session_state.employees:
                with st.container(border=True):
                    st.markdown(f"**{emp['name']}** — *{emp.get('designation', 'N/A')}*")
                    st.caption(f"ID: `{emp['id']}` | {emp['section']} — {emp['unit']}")
        else:
            st.info("No employees registered yet.")

    elif selected_menu == "🔑 IT Admin Account Management":
        st.subheader("🔑 IT Support & Admin Management")
        st.caption("Manage Computer Maintenance Technologist I accounts.")

        with st.expander("➕ Add New IT Admin Personnel", expanded=False):
            with st.form("add_admin_form", clear_on_submit=True):
                admin_name = st.text_input("Admin / Technician Name (e.g., Alex Reyes)")
                
                # Position strictly set to Computer Maintenance Technologist I
                st.text_input("Position / Designation:", value="Computer Maintenance Technologist I", disabled=True)
                admin_role = "Computer Maintenance Technologist I"
                
                admin_key = st.text_input("Assign Access Passkey / Password:", type="password")
                
                if st.form_submit_button("Create Admin Account", type="primary"):
                    if not admin_name.strip() or not admin_key.strip():
                        st.error("Both Admin Name and Access Passkey are required.")
                    else:
                        admins = st.session_state.get("admin_users", [])
                        new_id = f"ADM-{(len(admins) + 1):03d}"
                        
                        admins.append({
                            "id": new_id,
                            "name": admin_name.strip(),
                            "role": admin_role,
                            "passkey": admin_key.strip()
                        })
                        st.session_state.admin_users = admins
                        save_local_data()
                        st.success(f"New IT Admin **{admin_name}** (`{new_id}`) created as **{admin_role}**!")
                        st.rerun()

        st.markdown("---")
        st.subheader("Registered IT Administrators & Staff")

        admins = st.session_state.get("admin_users", [])
        if not admins:
            st.info("No admin accounts configured.")
        else:
            for idx, adm in enumerate(admins):
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"🛡️ **{adm['name']}** (`{adm['id']}`)")
                        st.caption(f"Position: **{adm.get('role', 'Computer Maintenance Technologist I')}**")
                    with c2:
                        if len(admins) > 1:
                            if st.button("🗑️ Remove", key=f"del_admin_{adm['id']}_{idx}"):
                                admins.pop(idx)
                                st.session_state.admin_users = admins
                                save_local_data()
                                st.warning(f"Admin {adm['name']} has been removed.")
                                st.rerun()
                        else:
                            st.caption("🔒 System Primary")