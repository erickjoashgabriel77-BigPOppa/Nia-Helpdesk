import os
import base64
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

def render_login_screen(logo_path=None):
    """Renders the NIA Quirino IMO IT Help Desk homepage and login screen."""
    
    # --- CENTERED HERO / HEADER BRANDING ---
    st.markdown("<div style='text-align: center; margin-top: -15px; margin-bottom: 25px;'>", unsafe_allow_html=True)
    
    # Glowing Logo Box
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                <div style="background: rgba(15, 23, 42, 0.85); border: 2px solid #10B981; border-radius: 18px; padding: 14px; box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);">
                    <img src="data:image/png;base64,{logo_b64}" style="width: 75px; height: 75px; object-fit: contain; display: block;">
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Title & Badge Section
    st.markdown(
        """
            <div style="display: inline-block; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 20px; padding: 4px 16px; color: #34D399; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">
                🏛️ National Irrigation Administration
            </div>
            <h1 style="font-size: 2.4rem; font-weight: 800; color: #FFFFFF; margin: 0 0 6px 0; letter-spacing: -0.5px;">
                Quirino Irrigation Management Office
            </h1>
            <h2 style="font-size: 1.45rem; font-weight: 700; color: #10B981; margin: 0 0 14px 0;">
                IT Help Desk System
            </h2>
            <p style="max-width: 680px; margin: 0 auto; color: #94A3B8; font-size: 0.95rem; line-height: 1.5;">
                Centralized technical support, job dispatching, and resolution portal for 
                <strong style="color: #F8FAFC;">Engineering & Operations (EOS)</strong> and 
                <strong style="color: #F8FAFC;">Administrative & Finance (AFS)</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2, gap="large")

    # --- CLIENT / EMPLOYEE PORTAL CARD ---
    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="background: rgba(16, 185, 129, 0.15); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; border: 1px solid rgba(16, 185, 129, 0.3);">
                        👤
                    </div>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34D399; font-size: 0.75rem; font-weight: 700; padding: 3px 12px; border-radius: 12px;">
                        Client Portal
                    </span>
                </div>
                <h3 style="margin: 0 0 6px 0; font-size: 1.35rem; color: #FFFFFF; font-weight: 700;">Client / Employee</h3>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 16px; line-height: 1.4;">
                    For department employees and personnel requesting technical assistance for hardware, software, networking, printers, or user accounts.
                </p>
                """,
                unsafe_allow_html=True
            )

            employees = st.session_state.get("employees", [])
            if not employees:
                st.warning("No employees registered in system. Please contact IT Admin.")
            else:
                tab_dropdown, tab_id = st.tabs(["📋 Select Profile", "🆔 Enter ID Number"])
                
                selected_client = None

                # Option 1: Dropdown Profile Select
                with tab_dropdown:
                    emp_options = {f"{e['name']} ({e['id']})": e for e in employees}
                    selected_emp_label = st.selectbox("Select Your Profile:", list(emp_options.keys()), key="select_emp_dropdown")
                    if st.button("Login as Client", type="primary", use_container_width=True, key="btn_login_dropdown"):
                        selected_client = emp_options[selected_emp_label]

                # Option 2: Employee ID Number Search
                with tab_id:
                    input_id = st.text_input("Enter Your Employee ID:", placeholder="e.g., EMP-EOS-001", key="input_emp_id").strip()
                    if st.button("Login via ID", type="primary", use_container_width=True, key="btn_login_id"):
                        if input_id:
                            found_emp = next((e for e in employees if str(e.get("id", "")).strip().lower() == input_id.lower()), None)
                            if found_emp:
                                selected_client = found_emp
                            else:
                                st.error(f"❌ Employee ID '{input_id}' not found. Please check your ID number.")
                        else:
                            st.warning("⚠️ Please enter your Employee ID number.")

                if selected_client:
                    st.session_state.logged_in_employee = selected_client
                    st.session_state.current_role = "client"
                    st.rerun()

            st.markdown(
                """
                <div style="margin-top: 18px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px; font-size: 0.82rem; color: #94A3B8;">
                    <div style="margin-bottom: 6px;">✔ Submit technical support requests</div>
                    <div>✔ Track ticket status & rate completed work</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --- ADMINISTRATOR / IT PORTAL CARD ---
    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="background: rgba(59, 130, 246, 0.15); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; border: 1px solid rgba(59, 130, 246, 0.3);">
                        🛡️
                    </div>
                    <span style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #60A5FA; font-size: 0.75rem; font-weight: 700; padding: 3px 12px; border-radius: 12px;">
                        Admin & IT Staff
                    </span>
                </div>
                <h3 style="margin: 0 0 6px 0; font-size: 1.35rem; color: #FFFFFF; font-weight: 700;">Administrator / IT</h3>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 16px; line-height: 1.4;">
                    For IT Support team members, dispatch coordinators, and system administrators managing tickets across EOS and AFS divisions.
                </p>
                """,
                unsafe_allow_html=True
            )

            with st.form("admin_login_form", border=False):
                entered_passkey = st.text_input("Enter IT Admin Passkey:", type="password", placeholder="Enter your passkey...")
                submit_admin = st.form_submit_button("Login as IT Admin", type="primary", use_container_width=True)

                if submit_admin:
                    matched_admin = next(
                        (adm for adm in st.session_state.get("admin_users", []) if adm.get("passkey") == entered_passkey),
                        None
                    )

                    if matched_admin:
                        st.session_state.is_admin_authenticated = True
                        st.session_state.logged_in_admin = matched_admin
                        st.session_state.current_role = "admin"
                        st.success(f"Welcome back, **{matched_admin['name']}**!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Passkey. Please check your credentials.")

            st.markdown(
                """
                <div style="margin-top: 18px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px; font-size: 0.82rem; color: #94A3B8;">
                    <div style="margin-bottom: 6px;">✔ Central ticketing dashboard & status workflows</div>
                    <div>✔ Search by Ticket ID, requester, or category</div>
                </div>
                """,
                unsafe_allow_html=True
            )