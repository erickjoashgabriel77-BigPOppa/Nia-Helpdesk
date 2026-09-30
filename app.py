import os
import sys
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Auto-refresh the application every 5 seconds (5000ms) for live cross-device syncing
st_autorefresh(interval=5000, limit=None, key="helpdesk_live_sync")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import EOS_SECTION, AFS_SECTION
from utils import load_local_data, logout
from views.auth import render_login_screen
from views.client import render_client_views
from views.admin import render_admin_views

# Load images safely across multiple extension formats (.png / .jpg / .jpeg)
def get_media_path(filename_base):
    for ext in ["png", "jpg", "jpeg", "PNG", "JPG"]:
        p = os.path.join(BASE_DIR, "Media", f"{filename_base}.{ext}")
        if os.path.exists(p):
            return p
    return None

LOGO_PATH = get_media_path("media-2668332601")
HEADER_PATH = get_media_path("TicketSLIP_header")
FOOTER_PATH = get_media_path("TicketSLIP_Footer")

if HEADER_PATH and os.path.exists(HEADER_PATH):
    with open(HEADER_PATH, "rb") as f:
        st.session_state["slip_header_b64"] = base64.b64encode(f.read()).decode("utf-8")

if FOOTER_PATH and os.path.exists(FOOTER_PATH):
    with open(FOOTER_PATH, "rb") as f:
        st.session_state["slip_footer_b64"] = base64.b64encode(f.read()).decode("utf-8")

icon = LOGO_PATH if LOGO_PATH and os.path.exists(LOGO_PATH) else "🌾"

st.set_page_config(
    page_title="Quirino Irrigation Management Office IT Help Desk System",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

if LOGO_PATH and os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        st.session_state["logo_b64"] = base64.b64encode(f.read()).decode("utf-8")

def init_session_state():
    saved_emp, saved_tic, saved_cnt, saved_key = load_local_data()

    if "current_role" not in st.session_state:
        st.session_state.current_role = None

    if "login_stage" not in st.session_state:
        st.session_state.login_stage = "choose_role"

    if "logged_in_employee" not in st.session_state:
        st.session_state.logged_in_employee = None

    if "is_admin_authenticated" not in st.session_state:
        st.session_state.is_admin_authenticated = False

    if "ticket_counter" not in st.session_state:
        st.session_state.ticket_counter = saved_cnt if saved_cnt is not None else 107

    # Always reload fresh employee and ticket data on session init/refresh
    st.session_state.employees = saved_emp if saved_emp else []
    st.session_state.tickets = saved_tic if saved_tic else []

    if "admin_passkey" not in st.session_state:
        st.session_state.admin_passkey = saved_key if saved_key else "ADMIN2026"

init_session_state()

def inject_floating_live_chat():
    """Renders a fixed floating chat widget at the bottom right corner."""
    st.markdown("""
    <style>
        .chat-widget-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 60px;
            height: 60px;
            background-color: #059669;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 4px 20px rgba(5, 150, 105, 0.5);
            cursor: pointer;
            z-index: 999999;
            transition: transform 0.2s ease, background-color 0.2s ease;
        }

        .chat-widget-btn:hover {
            transform: scale(1.1);
            background-color: #10b981;
        }

        .chat-status-dot {
            position: absolute;
            top: 2px;
            right: 2px;
            width: 14px;
            height: 14px;
            background-color: #22c55e;
            border: 2px solid #030712;
            border-radius: 50%;
        }
    </style>
    
    <div class="chat-widget-btn" title="Open IT Help Support Chat">
        💬
        <div class="chat-status-dot"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        with st.expander("💬 **IT Live Chat Support**", expanded=False):
            st.caption("Direct line to Quirino IMO IT Help Desk")
            st.info("🟢 **Status:** IT Technician Online")
            
            if "chat_messages" not in st.session_state:
                st.session_state.chat_messages = [
                    {"role": "assistant", "content": "Hello! How can the IT Help Desk assist you today?"}
                ]

            for msg in st.session_state.chat_messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if user_input := st.chat_input("Type your message...", key="chat_input_field"):
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": "Thank you for reaching out. An IT technician has been notified on the LAN queue."
                })
                st.rerun()

with st.sidebar:
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=80)
    st.title("NIA-Quirino IMO")
    st.caption("IT Help Desk System (EOS & AFS)")
    st.markdown("---")

    if st.session_state.current_role is not None:
        if st.session_state.current_role == "client":
            emp = st.session_state.logged_in_employee
            st.success(f"👤 Logged in as: **{emp['name']}**")
            st.write(f"**ID:** `{emp['id']}`")
            st.write(f"**Section:** {emp['section']}")
            st.write(f"**Unit:** {emp['unit']}")
            st.markdown("---")
            client_menu = st.radio("Client Navigation", ["📝 Create Ticket", "📋 My Tickets & Rate Service"])
        else:
            st.info("🛡️ **IT / Admin Mode**")
            st.markdown("---")
            admin_menu = st.radio("Admin Navigation", ["📊 Ticket Management Dashboard", "👥 Employee / Client Management"])

        st.markdown("---")
        if st.button("⬅️ Return to Last Page", use_container_width=True, key="sb_back"):
            logout()
            st.rerun()
        if st.button("🚪 Log Out", use_container_width=True, key="sb_logout"):
            logout()
            st.rerun()

if st.session_state.current_role is None:
    render_login_screen(LOGO_PATH)
elif st.session_state.current_role == "client":
    render_client_views(client_menu)
elif st.session_state.current_role == "admin":
    render_admin_views(admin_menu)

# Execute floating live chat
inject_floating_live_chat()