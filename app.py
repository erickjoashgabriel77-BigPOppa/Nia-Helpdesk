import sys
from pathlib import Path

# Force root directory to path position 0
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from views.auth import render_login_screen
from views.client import render_client_dashboard
from views.admin import render_admin_dashboard

st.set_page_config(page_title="NIA IT Helpdesk", page_icon="🎫", layout="wide")


def main():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = None

    if st.session_state["user"] is None:
        render_login_screen()
    elif st.session_state["role"] == "employee":
        render_client_dashboard()
    elif st.session_state["role"] == "admin":
        render_admin_dashboard()


if __name__ == "__main__":
    main()