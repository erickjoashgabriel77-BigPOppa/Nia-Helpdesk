# ==========================================
# views/auth.py
# ==========================================
import base64
import os
import streamlit as st

def render_login_screen(logo_path=None):
    st.markdown(
        """
        <style>
        .header-container { text-align: center; margin-bottom: 16px; }
        .main-title { font-size: 28px; font-weight: 800; color: #ffffff; margin-top: 6px; margin-bottom: 2px; }
        .subtitle { font-size: 18px; font-weight: 600; color: #10B981; }
        .hero-logo-box { display: flex; justify-content: center; margin-bottom: 10px; }
        .hero-logo-card {
            background: rgba(15, 23, 42, 0.85); border: 2px solid #10B981; border-radius: 14px; padding: 8px; box-shadow: 0 0 20px rgba(16, 185, 129, 0.35);
        }
        div[data-testid="stTabs"] {
            background-color: rgba(15, 23, 42, 0.88) !important; border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 12px !important; box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.5) !important; backdrop-filter: blur(12px); overflow: hidden !important;
        }
        .stTabs [data-baseweb="tab-list"] { background-color: rgba(0, 0, 0, 0.35) !important; padding: 6px 10px 0px 10px !important; gap: 8px !important; }
        .stTabs [data-baseweb="tab"] { height: 40px !important; border-radius: 8px 8px 0px 0px !important; padding: 0px 18px !important; background: transparent !important; }
        .stTabs [data-baseweb="tab"] p { color: #94A3B8 !important; font-size: 14px !important; font-weight: 600 !important; }
        .stTabs [aria-selected="true"] { background-color: rgba(16, 185, 129, 0.2) !important; border-bottom: 3px solid #10B981 !important; }
        .stTabs [aria-selected="true"] p { color: #FFFFFF !important; font-weight: 700 !important; }
        .stTabs [data-baseweb="tab-panel"] { padding: 20px 24px 22px 24px !important; }
        .page-footer { text-align: center; font-size: 12.5px; color: #D0E7DB !important; margin-top: 20px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f'<div class="hero-logo-box"><div class="hero-logo-card"><img src="data:image/png;base64,{logo_b64}" style="width: 65px; height: 65px; object-fit: contain;"></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="header-container"><div class="main-title">Quirino Irrigation Management Office</div><div class="subtitle">IT Help Desk System</div></div>', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2.2, 1])

    with col_center:
        tab_client, tab_admin = st.tabs(["👤 Employee / Client Portal", "🛡️ Administrator / IT Portal"])

        with tab_client:
            employees = st.session_state.get("employees", [])
            if not employees:
                st.warning("No registered employees found. Please contact IT Admin.")
            else:
                tab_dropdown, tab_id = st.tabs(["📋 Select Profile", "🆔 Enter ID Number"])
                selected_client = None

                with tab_dropdown:
                    emp_options = {f"{e['name']} ({e['id']})": e for e in employees}
                    selected_emp_label = st.selectbox("Select Your Profile:", list(emp_options.keys()))
                    if st.button("Log in as Employee", type="primary", use_container_width=True):
                        selected_client = emp_options[selected_emp_label]

                with tab_id:
                    input_id = st.text_input("Enter Your Employee ID:").strip()
                    if st.button("Log in via ID", type="primary", use_container_width=True):
                        if input_id:
                            found_emp = next((e for e in employees if str(e.get("id", "")).strip().lower() == input_id.lower()), None)
                            if found_emp: selected_client = found_emp
                            else: st.error("❌ Employee ID not found.")

                if selected_client:
                    st.session_state.logged_in_employee = selected_client
                    st.session_state.current_role = "client"
                    st.rerun()

        with tab_admin:
            with st.form("admin_login_form", border=False):
                entered_passkey = st.text_input("Enter Passkey / Password:", type="password")
                if st.form_submit_button("Log in as Administrator", type="primary", use_container_width=True):
                    admin_users = st.session_state.get("admin_users", [])
                    matched_admin = next((adm for adm in admin_users if adm.get("passkey") == entered_passkey), None)
                    if not matched_admin and entered_passkey == st.session_state.get("admin_passkey", "ADMIN2026"):
                        matched_admin = {"name": "IT Administrator", "role": "Computer Maintenance Technologist I", "passkey": entered_passkey}
                    
                    if matched_admin:
                        st.session_state.is_admin_authenticated = True
                        st.session_state.logged_in_admin = matched_admin
                        st.session_state.current_role = "admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid Passkey. Please check your credentials.")