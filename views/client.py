# ==========================================
# views/client.py
# ==========================================
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from utils import save_local_data, generate_printable_ticket_html, generate_official_ticket_slip

def render_client_views(client_menu):
    st.markdown(
        """
        <style>
        div[data-testid="stTextInput"] input:disabled, div[data-baseweb="input"] input:disabled, input[disabled] {
            -webkit-text-fill-color: #0f172a !important; background-color: #f1f5f9 !important; font-weight: 700 !important;
        }
        div[data-baseweb="input"]:has(input:disabled) { background-color: #f1f5f9 !important; border: 1px solid #94a3b8 !important; }
        div[data-testid="stTextInput"] input:not(:disabled), div[data-testid="stTextArea"] textarea {
            color: #ffffff !important; background-color: #1e293b !important; border: 1px solid #475569 !important;
        }
        label[data-testid="stWidgetLabel"] { color: #f8fafc !important; font-weight: 600 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    emp = st.session_state.get("logged_in_employee", {})

    if client_menu == "📝 Create Ticket":
        st.header("📝 Submit IT Service Request Ticket")
        with st.form("create_ticket_form", clear_on_submit=True):
            st.subheader("👤 Client Information")
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.text_input("Client Name", value=emp.get("name", ""), disabled=True)
            with col_b: st.text_input("Section", value=emp.get("section", ""), disabled=True)
            with col_c: st.text_input("Unit", value=emp.get("unit", ""), disabled=True)

            col_d, col_e = st.columns(2)
            with col_d: position = st.text_input("Position / Designation *", placeholder="e.g., Engineer A")
            with col_e: supervisor = st.text_input("Supervisor Name (Optional)")

            st.markdown("---")
            st.subheader("🛠️ Technical Request Details")
            col1, col2 = st.columns(2)
            with col1:
                request_type = st.selectbox("Service Category / Request Type *", [
                    "Hardware Repair / Maintenance", "Software Installation / Configuration", 
                    "Network / Internet Connectivity", "Printer / Scanner / Peripheral Support", 
                    "System / Database Access / Account Reset", "Others / General IT Support"
                ])
                urgency = st.select_slider("Urgency Level *", options=["Low", "Medium", "High", "Critical / Emergency"], value="Medium")
            with col2:
                equipment_type = st.text_input("Equipment Type (Optional)", placeholder="e.g., Desktop PC")
                serial_number = st.text_input("Serial Number (Optional)")
                date_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                st.text_input("Date & Time of Request", value=date_str, disabled=True)

            description = st.text_area("Detailed Description of Issue / Request *", height=120)

            if st.form_submit_button("🚀 Submit IT Ticket", use_container_width=True):
                if not position.strip() or not description.strip():
                    st.error("Please enter Position and Description before submitting.")
                else:
                    counter = st.session_state.get("ticket_counter", 107)
                    ticket_id = f"TK-{counter:04d}"
                    st.session_state.ticket_counter = counter + 1

                    new_ticket = {
                        "id": ticket_id,
                        "client_id": emp.get("id", "N/A"),
                        "client_name": emp.get("name", "Unknown"),
                        "section": emp.get("section", "N/A"),
                        "unit": emp.get("unit", "N/A"),
                        "position": position,
                        "supervisor": supervisor if supervisor.strip() else "N/A",
                        "request_type": request_type,
                        "urgency": urgency,
                        "equipment_type": equipment_type if equipment_type.strip() else "N/A",
                        "serial_number": serial_number if serial_number.strip() else "N/A",
                        "description": description,
                        "status": "Pending",
                        "date_created": date_str,
                        "action_taken": "",
                        "serviced_by": "",
                        "rating": None,
                        "feedback": ""
                    }
                    st.session_state.tickets.append(new_ticket)
                    save_local_data()
                    st.success(f"✅ Ticket **{ticket_id}** submitted successfully!")
                    st.balloons()
                    st.rerun()

    elif client_menu == "📋 My Tickets & Rate Service":
        st.header("📋 My Submitted Tickets")
        tickets = st.session_state.get("tickets", [])
        my_tickets = [t for t in tickets if t.get("client_id") == emp.get("id")]

        if not my_tickets:
            st.info("You haven't submitted any IT tickets yet.")
            return

        for t in reversed(my_tickets):
            status = t.get("status", "Pending")
            status_color = "🔴" if status == "Pending" else ("🟡" if status == "In Progress" else "🟢")
            t_id = t.get("id", "N/A")

            with st.expander(f"{status_color} **{t_id}** | {t.get('request_type')} - Status: **{status}**"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Date Created:** {t.get('date_created', 'N/A')}")
                    st.write(f"**Equipment:** {t.get('equipment_type')}")
                    st.write(f"**Urgency:** {t.get('urgency')}")
                with col2:
                    st.write(f"**Description:** {t.get('description')}")
                    st.write(f"**Action Taken by IT:** {t.get('action_taken', 'Pending action')}")
                
                st.markdown("---")
                
                # Feedback Section for Completed Tickets
                if status == "Completed":
                    st.subheader("⭐ Rate IT Support Service")
                    current_rating = t.get("rating")
                    rating_val = st.feedback("stars", key=f"rate_{t_id}")
                    feedback_text = st.text_area("Feedback / Suggestions", value=t.get("feedback", ""), key=f"fb_{t_id}")
                    
                    if st.button("Submit Rating", key=f"rate_btn_{t_id}"):
                        t["rating"] = rating_val + 1 if rating_val is not None else None  # +1 because index is 0-4
                        t["feedback"] = feedback_text
                        save_local_data()
                        st.success("Thank you for your feedback!")
                
                st.markdown("---")
                st.write("**Printable & Downloadable Slip**")
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    with st.popover("🖨️ View Slip", use_container_width=True):
                        components.html(generate_printable_ticket_html(t), height=520, scrolling=True)
                with b_col2:
                    docx_stream = generate_official_ticket_slip(t)
                    if docx_stream:
                        st.download_button("📄 Word Slip", data=docx_stream, file_name=f"Ticket_{t_id}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key=f"dl_{t_id}")