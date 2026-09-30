import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from config import ADMIN_PASSKEY

from utils import get_employee_by_id
def inject_custom_design():
    st.markdown("""
    <style>
        /* Hide sidebar on login screen */
        [data-testid="stSidebar"] {
            display: none;
        }

        /* Dark background theme */
        .stApp {
            background-color: #030712 !important;
            color: #f8fafc;
        }

        /* Center container layout */
        .block-container {
            max-width: 1000px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 2rem !important;
        }

        /* AI Studio Logo Card Styling */
        .hero-logo-box {
            width: 130px;
            height: 130px;
            background: #09131d;
            border: 2px solid #059669;
            border-radius: 20px;
            box-shadow: 0 0 35px rgba(16, 185, 129, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem auto;
            padding: 12px;
        }

        .hero-logo-img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 10px;
        }

        /* Pill Badge Styling */
        .pill-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 9999px;
            background-color: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #10b981;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 12px;
        }

        /* Modernized Cards */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: #0b0f19 !important;
            border: 1px solid #1e293b !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
        }

        /* Text Customization */
        .main-title {
            text-align: center;
            font-size: 2.3rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 0px;
            letter-spacing: -0.5px;
        }

        .sub-title {
            text-align: center;
            font-size: 1.35rem;
            font-weight: 700;
            color: #10b981;
            margin-top: 4px;
            margin-bottom: 12px;
        }

        .description-text {
            text-align: center;
            color: #94a3b8;
            font-size: 0.95rem;
            margin-bottom: 2rem;
            line-height: 1.5;
        }

        /* Green Primary Buttons */
        .stButton > button[kind="primary"] {
            background-color: #059669 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1rem !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #10b981 !important;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_login_screen(logo_path):
    inject_custom_design()

    if st.session_state.login_stage == "choose_role":
        logo_b64 = st.session_state.get("logo_b64", "")
        
        # Displays the AI Studio Logo Container
        if logo_b64:
            st.markdown(f'''
                <div class="hero-logo-box">
                    <img src="data:image/jpeg;base64,{logo_b64}" class="hero-logo-img">
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('<div style="text-align: center;"><span class="pill-badge">🏛️ National Irrigation Administration</span></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">Quirino Irrigation Management Office</h1>', unsafe_allow_html=True)
        st.markdown('<h3 class="sub-title">IT Help Desk System</h3>', unsafe_allow_html=True)
        st.markdown('<p class="description-text">Centralized technical support, job dispatching, and resolution portal for <b>Engineering & Operations (EOS)</b> and <b>Administrative & Finance (AFS)</b>.</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            with st.container(border=True):
                st.markdown('<span class="pill-badge">Client Portal</span>', unsafe_allow_html=True)
                st.subheader("👤 Client / Employee")
                st.caption("For department employees and personnel requesting technical assistance for hardware, software, networking, printers, or user accounts.")
                st.markdown("---")
                st.markdown("✓ Submit technical support requests")
                st.markdown("✓ Track ticket status & cancel pending requests")
                st.markdown("✓ Print official ISO-format service slips")
                st.write("")
                if st.button("Continue to Client Login ➔", type="primary", use_container_width=True, key="btn_choose_client"):
                    st.session_state.login_stage = "client_login"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown('<span class="pill-badge" style="color: #38bdf8; border-color: rgba(56,189,248,0.35); background: rgba(56,189,248,0.12);">Admin & IT Staff</span>', unsafe_allow_html=True)
                st.subheader("🛡️ Administrator / IT")
                st.caption("For IT Support team members, dispatch coordinators, and system administrators managing tickets across EOS and AFS divisions.")
                st.markdown("---")
                st.markdown("✓ Central ticketing dashboard & status workflows")
                st.markdown("✓ Search by Ticket ID, requester, or category")
                st.markdown("✓ Assign technicians & log resolution notes")
                st.write("")
                if st.button("Continue to Admin Login ➔", type="secondary", use_container_width=True, key="btn_choose_admin"):
                    st.session_state.login_stage = "admin_login"
                    st.rerun()

    elif st.session_state.login_stage == "client_login":
        if st.button("⬅️ Return to Role Selection", key="btn_back_to_role_client"):
            st.session_state.login_stage = "choose_role"
            st.rerun()
            
        with st.container(border=True):
            st.subheader("👤 Client / Employee Login")
            st.write("Select your registered employee profile to access the Client Portal:")
            
            emp_options = {
                f"{emp['name']} ({emp['id']} - {emp['unit']})": emp['id']
                for emp in st.session_state.employees
            }
            selected_emp_label = st.selectbox("Select Registered Employee:", list(emp_options.keys()))
            manual_id = st.text_input("Or Enter Employee ID manually (e.g., EMP-EOS-001):")
            
            if st.button("Log in to Client Portal", type="primary", use_container_width=True):
                target_id = manual_id.strip() if manual_id.strip() else emp_options[selected_emp_label]
                matched_emp = get_employee_by_id(target_id)
                if matched_emp:
                    st.session_state.logged_in_employee = matched_emp
                    st.session_state.current_role = "client"
                    st.session_state.login_stage = "choose_role"
                    st.success(f"Welcome back, {matched_emp['name']}!")
                    st.rerun()
                else:
                    st.error("Employee ID not found.")

    elif st.session_state.login_stage == "admin_login":
        if st.button("⬅️ Return to Role Selection", key="btn_back_to_role_admin"):
            st.session_state.login_stage = "choose_role"
            st.rerun()
            
        with st.container(border=True):
            st.subheader("🛡️ Administrator / IT Staff Login")
            st.write("Enter your administrative credentials to access the central management console:")
            
            admin_key_input = st.text_input(
                "Enter IT Admin Key / Password:",
                type="password",
                help=f"Default demonstration key: {ADMIN_PASSKEY}"
            )
            st.caption(f"💡 Demo Key: **{ADMIN_PASSKEY}**")
            
            if st.button("Authenticate & Open IT Admin Portal", type="primary", use_container_width=True):
                if admin_key_input == ADMIN_PASSKEY or admin_key_input.lower() == "admin":
                    st.session_state.is_admin_authenticated = True
                    st.session_state.current_role = "admin"
                    st.session_state.login_stage = "choose_role"
                    st.success("Admin credentials verified.")
                    st.rerun()
                else:
                    st.error(f"Invalid Admin Key. (Hint: '{ADMIN_PASSKEY}')")