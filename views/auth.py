import base64
import os
import streamlit as st


def render_login_screen(logo_path=None):
    """Renders the single-screen homepage for Quirino Irrigation Management Office IT Help Desk System.

    Includes full CSS overrides for Streamlit Cloud and local deployments to hide top headers and toolbars.
    """

    # --- CUSTOM CSS: HIDE ALL STREAMLIT TOP HEADERS & TOOLBARS (LOCAL & STREAMLIT CLOUD) ---
    st.markdown(
        """
        <style>
        /* Hide all Streamlit top headers, navbars, toolbars, decoration lines, and sidebar controls */
        header,
        header[data-testid="stHeader"],
        div[data-testid="stHeader"],
        div[data-testid="stDecoration"],
        div[data-testid="stToolbar"],
        div[data-testid="stHeaderNav"],
        div[data-testid="stStatusWidget"],
        [data-testid="collapsedControl"],
        #MainMenu,
        footer {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* Disable page-level scrolling */
        html, body, [data-testid="stAppViewContainer"], .main {
            overflow: hidden !important;
        }

        /* Adjust top container spacing */
        .block-container {
            max-width: 980px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* Centered Title Section */
        .header-container {
            text-align: center;
            margin-bottom: 16px;
        }
        .main-title {
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 6px;
            margin-bottom: 2px;
            letter-spacing: -0.5px;
        }
        .subtitle {
            font-size: 18px;
            font-weight: 600;
            color: #10B981;
        }

        /* Logo Card Container */
        .hero-logo-box {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .hero-logo-card {
            background: rgba(15, 23, 42, 0.85);
            border: 2px solid #10B981;
            border-radius: 14px;
            padding: 8px;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.35);
        }

        /* UNIFIED TAB CONTAINER CARD */
        div[data-testid="stTabs"] {
            background-color: rgba(15, 23, 42, 0.88) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 12px !important;
            box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(12px);
            overflow: hidden !important;
        }

        /* OUTER TAB BAR HEADER */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(0, 0, 0, 0.35) !important;
            padding: 6px 10px 0px 10px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
            gap: 8px !important;
        }

        .stTabs [data-baseweb="tab"] {
            height: 40px !important;
            border-radius: 8px 8px 0px 0px !important;
            padding: 0px 18px !important;
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab"] p {
            color: #94A3B8 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }

        /* ACTIVE TAB HIGHLIGHT */
        .stTabs [aria-selected="true"] {
            background-color: rgba(16, 185, 129, 0.2) !important;
            border-bottom: 3px solid #10B981 !important;
        }

        .stTabs [aria-selected="true"] p {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* TAB PANEL CONTENT AREA */
        .stTabs [data-baseweb="tab-panel"] {
            padding: 20px 24px 22px 24px !important;
        }

        /* Green Action Button */
        .stButton > button[kind="primary"] {
            width: 100% !important;
            background-color: #0d8a57 !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 14.5px !important;
            padding: 9px !important;
            border-radius: 6px !important;
            border: none !important;
            transition: all 0.2s ease !important;
            margin-top: 10px !important;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #10b981 !important;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        }

        /* Card Subtext */
        .card-footer-text {
            font-size: 12px;
            color: #94A3B8;
            margin-top: 16px;
            line-height: 1.4;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
        }

        /* Bottom Footer */
        .page-footer {
            text-align: center;
            font-size: 12.5px;
            color: #D0E7DB !important;
            margin-top: 20px;
            padding-bottom: 8px;
        }
        .page-footer a {
            color: #34D399 !important;
            font-weight: 600;
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- LOGO & HEADER ---
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div class="hero-logo-box">
                <div class="hero-logo-card">
                    <img src="data:image/png;base64,{logo_b64}" style="width: 65px; height: 65px; object-fit: contain; display: block;">
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="header-container">
            <div class="main-title">Quirino Irrigation Management Office</div>
            <div class="subtitle">IT Help Desk System</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- UNIFIED TABBED LOGIN CARD ---
    col_left, col_center, col_right = st.columns([1, 2.2, 1])

    with col_center:
        tab_client, tab_admin = st.tabs(
            ["👤 Employee / Client Portal", "🛡️ Administrator / IT Portal"]
        )

        # --- TAB 1: EMPLOYEE / CLIENT PORTAL ---
        with tab_client:
            st.markdown(
                "<h3 style='margin-top:0; margin-bottom: 4px; font-size: 18px; color: #FFFFFF;'>Client / Employee</h3>",
                unsafe_allow_html=True,
            )
            st.caption(
                "For department employees and personnel assistance for equipment, products, or user accounts."
            )

            employees = st.session_state.get("employees", [])

            if not employees:
                st.warning(
                    "No registered employees found in system. Please contact IT Admin."
                )
            else:
                tab_dropdown, tab_id = st.tabs(
                    ["📋 Select Profile", "🆔 Enter ID Number"]
                )

                selected_client = None

                # Option 1: Dropdown Profile Select
                with tab_dropdown:
                    emp_options = {
                        f"{e['name']} ({e['id']})": e for e in employees
                    }
                    selected_emp_label = st.selectbox(
                        "Select Your Profile:",
                        list(emp_options.keys()),
                        key="select_emp_dropdown",
                    )
                    if st.button(
                        "Log in as Employee",
                        type="primary",
                        use_container_width=True,
                        key="btn_login_dropdown",
                    ):
                        selected_client = emp_options[selected_emp_label]

                # Option 2: Employee ID Search
                with tab_id:
                    input_id = st.text_input(
                        "Enter Your Employee ID:",
                        placeholder="e.g., EMP-EOS-001",
                        key="input_emp_id",
                    ).strip()
                    if st.button(
                        "Log in via ID",
                        type="primary",
                        use_container_width=True,
                        key="btn_login_id",
                    ):
                        if input_id:
                            found_emp = next(
                                (
                                    e
                                    for e in employees
                                    if str(e.get("id", "")).strip().lower()
                                    == input_id.lower()
                                ),
                                None,
                            )
                            if found_emp:
                                selected_client = found_emp
                            else:
                                st.error(
                                    f"❌ Employee ID '{input_id}' not found."
                                )
                        else:
                            st.warning("⚠️ Please enter your Employee ID.")

                if selected_client:
                    st.session_state.logged_in_employee = selected_client
                    st.session_state.current_role = "client"
                    st.rerun()

            st.markdown(
                """
                <div class="card-footer-text">
                    Centralized technical support, job dispatching and resolution portal for Engineering and Administrative & Finance (AFS).
                </div>
                """,
                unsafe_allow_html=True,
            )

        # --- TAB 2: ADMINISTRATOR PORTAL ---
        with tab_admin:
            st.markdown(
                "<h3 style='margin-top:0; margin-bottom: 4px; font-size: 18px; color: #FFFFFF;'>Administrator / IT Access</h3>",
                unsafe_allow_html=True,
            )
            st.caption(
                "For IT personnel and system administrators managing ticket queues."
            )

            with st.form("admin_login_form", border=False):
                entered_passkey = st.text_input(
                    "Enter Passkey / Password:",
                    type="password",
                    placeholder="Enter admin passkey...",
                )
                submit_admin = st.form_submit_button(
                    "Log in as Administrator",
                    type="primary",
                    use_container_width=True,
                )

                if submit_admin:
                    matched_admin = next(
                        (
                            adm
                            for adm in st.session_state.get("admin_users", [])
                            if adm.get("passkey") == entered_passkey
                        ),
                        None,
                    )

                    if matched_admin:
                        st.session_state.is_admin_authenticated = True
                        st.session_state.logged_in_admin = matched_admin
                        st.session_state.current_role = "admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid Passkey. Please check your credentials.")

    # --- FOOTER ---
    st.markdown(
        """
        <div class="page-footer">
            Version 2.0 | <a href="#">IT Admin Login</a> | <a href="#">Knowledge Base</a><br>
            © 2026 Quirino Irrigation Management Office. All Rights Reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )