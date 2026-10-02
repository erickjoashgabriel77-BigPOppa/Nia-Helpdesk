# ==========================================
# views/admin.py
# ==========================================
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from utils import save_local_data, generate_printable_ticket_html, generate_official_ticket_slip

def render_admin_views(admin_menu):
    tickets = st.session_state.get("tickets", [])
    admin_user = st.session_state.get("logged_in_admin", {})
    admin_name = admin_user.get("name", "IT Admin")

    if admin_menu == "📊 Ticket Management Dashboard":
        st.header("📊 IT Support Ticket Dashboard")

        # Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tickets", len(tickets))
        c2.metric("Pending", len([t for t in tickets if t.get("status") == "Pending"]))
        c3.metric("In Progress", len([t for t in tickets if t.get("status") == "In Progress"]))
        c4.metric("Completed", len([t for t in tickets if t.get("status") == "Completed"]))
        
        st.markdown("---")

        if not tickets:
            st.info("No tickets recorded in the system.")
            return

        # Search & Filters
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            search_query = st.text_input("🔍 Search tickets...", placeholder="Search by Client Name, ID, or Description").lower()
        with col_f2:
            status_filter = st.selectbox("Filter Status", ["All", "Pending", "In Progress", "Completed", "Cancelled"])
        with col_f3:
            df = pd.DataFrame(tickets)
            if not df.empty:
                st.download_button("📥 Export Tickets CSV", data=df.to_csv(index=False).encode('utf-8'), file_name="IT_Tickets_Report.csv", mime="text/csv", use_container_width=True)

        status_options = ["Pending", "In Progress", "Completed", "Cancelled"]

        # Filter Logic
        filtered_tickets = [t for t in tickets if 
                            (status_filter == "All" or t.get("status") == status_filter) and 
                            (search_query in str(t.values()).lower())]

        for t in reversed(filtered_tickets):
            t_id = t.get("id", "N/A")
            status = t.get("status", "Pending")
            status_index = status_options.index(status) if status in status_options else 0

            with st.expander(f"🎫 **{t_id}** | {t.get('client_name', 'Unknown')} ({t.get('section', 'N/A')}) - Status: {status}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Category:** {t.get('request_type', 'N/A')}")
                    st.write(f"**Equipment:** {t.get('equipment_type', 'N/A')}")
                    st.write(f"**Serial No.:** {t.get('serial_number', 'N/A')}")
                    st.write(f"**Date Submitted:** {t.get('date_created', 'N/A')}")
                with col2:
                    st.write(f"**Urgency:** {t.get('urgency', 'N/A')}")
                    st.write(f"**Description:** {t.get('description', 'N/A')}")

                st.markdown("---")
                act_col1, act_col2 = st.columns([2, 2])

                # Live Update Form
                with act_col1:
                    new_status = st.selectbox("Update Status", status_options, index=status_index, key=f"status_select_{t_id}")
                    action_taken = st.text_area("Resolution / Action Taken", value=t.get("action_taken", ""), key=f"action_{t_id}")
                    serviced_by = st.text_input("Serviced By (IT Tech)", value=t.get("serviced_by", admin_name), key=f"tech_{t_id}")

                    if st.button("Update Ticket Details", key=f"btn_update_{t_id}"):
                        t["status"] = new_status
                        t["action_taken"] = action_taken
                        t["serviced_by"] = serviced_by
                        save_local_data()
                        st.success(f"Ticket {t_id} updated successfully!")
                        st.rerun()

                # Document Generation
                with act_col2:
                    st.write("**Printable & Downloadable Slip**")
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        with st.popover("🖨️ View Slip", use_container_width=True):
                            components.html(generate_printable_ticket_html(t), height=520, scrolling=True)
                    with b_col2:
                        docx_stream = generate_official_ticket_slip(t)
                        if docx_stream:
                            st.download_button("📄 Word Slip", data=docx_stream, file_name=f"Ticket_{t_id}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key=f"dl_docx_{t_id}")

    elif admin_menu == "👥 Employee / Client Management":
        st.header("👥 Client / Employee Directory")
        employees = st.session_state.get("employees", [])
        st.dataframe(pd.DataFrame(employees), use_container_width=True)

        with st.expander("➕ Register New Employee"):
            with st.form("add_emp_form"):
                emp_id = st.text_input("Employee ID", placeholder="EMP-EOS-010")
                emp_name = st.text_input("Full Name")
                section = st.selectbox("Section", ["Engineering & Operations Section (EOS)", "Administrative & Finance Section (AFS)"])
                unit = st.text_input("Unit")
                if st.form_submit_button("Add Employee"):
                    if emp_id and emp_name:
                        st.session_state.employees.append({"id": emp_id, "name": emp_name, "section": section, "unit": unit})
                        save_local_data()
                        st.success(f"Employee {emp_name} registered successfully!")
                        st.rerun()

    elif admin_menu == "🔑 IT Admin Account Management":
        st.header("🔑 IT Admin Passkey Management")
        new_key = st.text_input("Change Admin Passkey:", value=st.session_state.get("admin_passkey", "ADMIN2026"), type="password")
        if st.button("Save Passkey"):
            st.session_state.admin_passkey = new_key
            save_local_data()
            st.success("Admin passkey updated successfully!")