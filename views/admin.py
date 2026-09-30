import streamlit as st
from utils import save_local_data


def render_admin_views(admin_menu):
    tickets = st.session_state.get("tickets", [])

    if admin_menu == "📊 Ticket Management Dashboard":
        st.header("📊 IT Support Ticket Dashboard")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tickets", len(tickets))
        c2.metric("Pending", len([t for t in tickets if t["status"] == "Pending"]))
        c3.metric("In Progress", len([t for t in tickets if t["status"] == "In Progress"]))
        c4.metric("Completed", len([t for t in tickets if t["status"] == "Completed"]))

        st.markdown("---")

        if not tickets:
            st.info("No tickets recorded in the system.")
            return

        for t in reversed(tickets):
            with st.expander(f"🎫 **{t['id']}** | {t['client_name']} ({t['section']}) - Status: {t['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Category:** {t['request_type']}")
                    st.write(f"**Unit:** {t['unit']}")
                    st.write(f"**Date Submitted:** {t['date_created']}")
                with col2:
                    st.write(f"**Urgency:** {t['urgency']}")
                    st.write(f"**Description:** {t['description']}")

                new_status = st.selectbox(
                    "Update Status",
                    ["Pending", "In Progress", "Completed", "Cancelled"],
                    index=["Pending", "In Progress", "Completed", "Cancelled"].index(t["status"]),
                    key=f"status_select_{t['id']}",
                )

                if st.button("Update Ticket", key=f"btn_update_{t['id']}"):
                    t["status"] = new_status
                    save_local_data()
                    st.success(f"Status for {t['id']} updated to {new_status}!")
                    st.rerun()

    elif admin_menu == "👥 Employee / Client Management":
        st.header("👥 Client / Employee Directory")
        employees = st.session_state.get("employees", [])

        st.dataframe(employees, use_container_width=True)

        with st.expander("➕ Register New Employee"):
            with st.form("add_emp_form"):
                emp_id = st.text_input("Employee ID", placeholder="EMP-EOS-010")
                emp_name = st.text_input("Full Name")
                section = st.selectbox("Section", ["Engineering & Operations Section (EOS)", "Administrative & Finance Section (AFS)"])
                unit = st.text_input("Unit / Position")

                if st.form_submit_button("Add Employee"):
                    if emp_id and emp_name:
                        st.session_state.employees.append({"id": emp_id, "name": emp_name, "section": section, "unit": unit})
                        save_local_data()
                        st.success(f"Employee {emp_name} registered successfully!")
                        st.rerun()

    elif admin_menu == "🔑 IT Admin Account Management":
        st.header("🔑 IT Admin Passkey & Account Management")

        st.write("Current Admin Passkey configured in system.")
        new_key = st.text_input("Change Admin Passkey:", value=st.session_state.get("admin_passkey", "ADMIN2026"), type="password")

        if st.button("Save Passkey"):
            st.session_state.admin_passkey = new_key
            save_local_data()
            st.success("Admin passkey updated successfully!")