import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from utils import save_local_data
from views.admin import generate_ticket_slip_html, generate_filled_docx, HAS_DOCX


def render_client_views(client_menu):
    # High-contrast CSS for text inputs & disabled/autofilled fields
    st.markdown(
        """
        <style>
        /* 1. Target all disabled/auto-filled input fields */
        div[data-testid="stTextInput"] input:disabled,
        div[data-baseweb="input"] input:disabled,
        input[disabled] {
            -webkit-text-fill-color: #0f172a !important;
            color: #0f172a !important;
            background-color: #f1f5f9 !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }

        /* 2. Container style for disabled inputs */
        div[data-baseweb="input"]:has(input:disabled),
        div[data-baseweb="base-input"]:has(input:disabled) {
            background-color: #f1f5f9 !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 6px !important;
        }

        /* 3. Style active editable text inputs and textareas */
        div[data-testid="stTextInput"] input:not(:disabled),
        div[data-testid="stTextArea"] textarea {
            color: #ffffff !important;
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            border-radius: 6px !important;
        }

        /* 4. Placeholder text formatting */
        ::placeholder, 
        textarea::placeholder, 
        input::placeholder {
            color: #94a3b8 !important;
            -webkit-text-fill-color: #94a3b8 !important;
            opacity: 1 !important;
        }

        /* 5. Field labels styling */
        label[data-testid="stWidgetLabel"] {
            color: #f8fafc !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    emp = st.session_state.get("logged_in_employee", {})

    if client_menu == "📝 Create Ticket":
        st.header("📝 Submit IT Service Request Ticket")
        st.caption("Fill out the service request details below. All fields will auto-populate into the official printable/downloadable ticket slip.")

        with st.form("create_ticket_form", clear_on_submit=True):
            st.subheader("👤 Client Information")
            
            # Row 1: Auto-filled Client Info
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.text_input("Client Name", value=emp.get("name", ""), disabled=True)
            with col_b:
                st.text_input("Section", value=emp.get("section", ""), disabled=True)
            with col_c:
                st.text_input("Unit", value=emp.get("unit", ""), disabled=True)

            # Row 2: Fillable Position and Supervisor Name
            col_d, col_e = st.columns(2)
            with col_d:
                position = st.text_input(
                    "Position / Designation *",
                    placeholder="e.g., Computer Maintenance Tech",
                )
            with col_e:
                supervisor = st.text_input(
                    "Supervisor Name (Optional)",
                    placeholder="e.g., Engr. Juan Dela Cruz",
                )

            st.markdown("---")
            st.subheader("🛠️ Technical Request Details")

            col1, col2 = st.columns(2)
            with col1:
                request_type = st.selectbox(
                    "Service Category / Request Type *",
                    [
                        "Hardware Repair / Maintenance",
                        "Software Installation / Configuration",
                        "Network / Internet Connectivity",
                        "Printer / Scanner / Peripheral Support",
                        "System / Database Access / Account Reset",
                        "Preventive Maintenance",
                        "Others / General IT Support",
                    ],
                )
                urgency = st.select_slider(
                    "Urgency / Priority Level *",
                    options=["Low", "Medium", "High", "Critical / Emergency"],
                    value="Medium",
                )

            with col2:
                equipment_type = st.text_input(
                    "Equipment Type / Model (Optional)",
                    placeholder="e.g., Desktop PC, Epson L3210 Printer, Monitor",
                )
                serial_number = st.text_input(
                    "Serial Number (Optional)",
                    placeholder="e.g., SN-2026-987654",
                )
                date_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                st.text_input("Date & Time of Request", value=date_str, disabled=True)

            description = st.text_area(
                "Detailed Description of Issue / Request *",
                placeholder="Please describe the specific problem, error messages, or assistance needed...",
                height=120,
            )

            submitted = st.form_submit_button("🚀 Submit IT Ticket", use_container_width=True)

            if submitted:
                if not position.strip():
                    st.error("Please enter your Position / Designation before submitting.")
                elif not description.strip():
                    st.error("Please provide a description of the issue before submitting.")
                else:
                    counter = st.session_state.get("ticket_counter", 107)
                    ticket_id = f"TK-{counter:04d}"
                    st.session_state.ticket_counter = counter + 1

                    new_ticket = {
                        "id": ticket_id,
                        "client_name": emp.get("name", "Unknown"),
                        "client_id": emp.get("id", "N/A"),
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
                    }

                    st.session_state.tickets.append(new_ticket)
                    save_local_data()
                    st.success(f"✅ Ticket **{ticket_id}** submitted successfully!")
                    st.balloons()
                    st.rerun()

    elif client_menu == "📋 My Tickets & Rate Service":
        st.header("📋 My Submitted Tickets")
        tickets = st.session_state.get("tickets", [])
        my_tickets = [t for t in tickets if t.get("client_id") == emp.get("id") or t.get("client_name") == emp.get("name")]

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
                    st.write(f"**Position:** {t.get('position', 'N/A')}")
                    st.write(f"**Supervisor:** {t.get('supervisor', 'N/A')}")
                    st.write(f"**Equipment Type:** {t.get('equipment_type') or t.get('equipment', 'N/A')}")
                    st.write(f"**Serial No.:** {t.get('serial_number') or t.get('serial_no', 'N/A')}")
                    st.write(f"**Urgency:** {t.get('urgency', 'N/A')}")
                with col2:
                    st.write(f"**Description:** {t.get('description', 'N/A')}")
                    st.write(f"**Action Taken by IT:** {t.get('action_taken', 'Pending action')}")

                st.markdown("---")
                st.write("**Printable & Downloadable Slip**")
                b_col1, b_col2 = st.columns(2)

                with b_col1:
                    with st.popover("🖨️ View Slip", use_container_width=True):
                        slip_html = generate_ticket_slip_html(t)
                        components.html(slip_html, height=520, scrolling=True)

                with b_col2:
                    docx_bytes = generate_filled_docx(t)
                    if docx_bytes:
                        st.download_button(
                            label="📄 Word Slip",
                            data=docx_bytes,
                            file_name=f"Ticket_{t_id}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            key=f"client_dl_docx_{t_id}",
                        )
                    elif not HAS_DOCX:
                        st.caption("⚠️ Add `python-docx` to requirements.txt")
                    else:
                        st.caption("⚠️ Template file missing")