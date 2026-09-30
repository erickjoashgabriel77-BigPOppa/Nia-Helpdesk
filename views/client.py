import datetime
import streamlit as st
from config import AFS_SECTION, EOS_SECTION
from utils import save_local_data


def render_client_views(client_menu):
    emp = st.session_state.logged_in_employee

    if client_menu == "📝 Create Ticket":
        st.header("📝 Create New Technical Support Request")
        st.write(f"Logged in as: **{emp['name']}** (`{emp['id']}`)")

        with st.form("create_ticket_form"):
            col1, col2 = st.columns(2)
            with col1:
                section = st.selectbox(
                    "Section",
                    ["Engineering & Operations Section (EOS)", "Administrative & Finance Section (AFS)"],
                    index=0 if "Engineering" in emp.get("section", "") else 1,
                )
            with col2:
                available_units = EOS_SECTION if "Engineering" in section else AFS_SECTION
                unit = st.selectbox("Unit / Division", available_units)

            request_type = st.selectbox(
                "Request Category",
                [
                    "Computer Hardware Repair / Maintenance",
                    "Network & Internet Connection",
                    "Printer / Scanner Setup & Repair",
                    "Software Installation / Configuration",
                    "User Account / Password Reset",
                    "Others",
                ],
            )

            description = st.text_area("Detailed Problem Description", placeholder="Describe the issue in detail...")
            urgency = st.select_slider("Urgency Level", options=["Low", "Medium", "High", "Critical"], value="Medium")

            submitted = st.form_submit_button("🚀 Submit Ticket", type="primary", use_container_width=True)

            if submitted:
                if not description.strip():
                    st.error("Please provide a description of the issue.")
                else:
                    new_id = f"TICK-{st.session_state.ticket_counter}"
                    st.session_state.ticket_counter += 1

                    new_ticket = {
                        "id": new_id,
                        "client_id": emp["id"],
                        "client_name": emp["name"],
                        "section": section,
                        "unit": unit,
                        "request_type": request_type,
                        "description": description,
                        "urgency": urgency,
                        "status": "Pending",
                        "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "rating": None,
                        "feedback": "",
                    }

                    st.session_state.tickets.append(new_ticket)
                    save_local_data()
                    st.success(f"✅ Ticket **{new_id}** created successfully!")
                    st.rerun()

    elif client_menu == "📋 My Tickets & Rate Service":
        st.header("📋 My Service Tickets")

        client_tickets = [t for t in st.session_state.tickets if t.get("client_id") == emp["id"]]

        if not client_tickets:
            st.info("You haven't submitted any tickets yet.")
            return

        for t in reversed(client_tickets):
            with st.expander(f"🎫 **{t['id']}** - {t['request_type']} ({t['status']})"):
                st.write(f"**Date Created:** {t['date_created']}")
                st.write(f"**Urgency:** {t['urgency']}")
                st.write(f"**Description:** {t['description']}")
                st.write(f"**Status:** `{t['status']}`")

                if t["status"] == "Completed":
                    st.markdown("---")
                    st.subheader("⭐ Rate IT Service")
                    current_rating = t.get("rating", 5) or 5
                    rating = st.slider("Rating (1 to 5 Stars)", 1, 5, current_rating, key=f"rate_{t['id']}")
                    feedback = st.text_input("Feedback / Comments", value=t.get("feedback", ""), key=f"fb_{t['id']}")

                    if st.button("Submit Rating", key=f"btn_rate_{t['id']}"):
                        t["rating"] = rating
                        t["feedback"] = feedback
                        save_local_data()
                        st.success("Thank you for your feedback!")
                        st.rerun()