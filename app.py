import os
import sys

# Force root directory into sys.path before loading local views
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from views.auth import render_login_screen

# Page Configuration
st.set_page_config(page_title="NIA IT Helpdesk", page_icon="🎫", layout="wide")

def main():
    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        render_login_screen()
    else:
        st.write(f"Logged in as {st.session_state['user'].get('name', 'User')}")

if __name__ == "__main__":
    main()