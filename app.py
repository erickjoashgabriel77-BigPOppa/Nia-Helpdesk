import base64
import os
import sys
import streamlit as st

# --- 1. BASE DIRECTORY SETUP & MEDIA HELPERS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def get_media_path(filename_base):
    for ext in ["png", "jpg", "jpeg", "PNG", "JPG"]:
        p = os.path.join(BASE_DIR, "Media", f"{filename_base}.{ext}")
        if os.path.exists(p):
            return p
    return None


LOGO_PATH = get_media_path("media-2668332601")
HEADER_PATH = get_media_path("TicketSLIP_header")
FOOTER_PATH = get_media_path("TicketSLIP_Footer")

icon = LOGO_PATH if LOGO_PATH and os.path.exists(LOGO_PATH) else "🌾"

# --- 2. STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Quirino Irrigation Management Office IT Help Desk System",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- 3. CLEAN CUSTOM BACKGROUND & UI STYLING (NO HEADER HIDING) ---
def apply_custom_background():
    media_dir = os.path.join(BASE_DIR, "Media")

    bckg_b64 = ""
    for ext in ["png", "jpg", "jpeg", "webp"]:
        file_path = os.path.join(media_dir, f"bckg_color.{ext}")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                bckg_b64 = base64.b64encode(f.read()).decode("utf-8")
            break

    if bckg_b64:
        background_style = f"""
        .stApp {{
            background: url("data:image/png;base64,{bckg_b64}") no-repeat center center fixed;
            background-size: cover;
        }}
        """
    else:
        background_style = """
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        }
        """

    st.markdown(
        f"""
        <style>
        {background_style}

        /* HIDE TOP-RIGHT TOOLBAR (Share, Star, Edit, GitHub) */
        [data-testid="stToolbar"],
        [data-testid="stHeaderActionElements"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* OVERALL TEXT VISIBILITY */
        html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {{
            color: #FFFFFF !important;
            text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.7);
        }}

        /* Glassmorphism Containers */
        [data-testid="stForm"], div[data-testid="stExpander"], div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            padding: 16px;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: rgba(10, 15, 29, 0.90) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* Input Fields */
        input, select, textarea, div[role="combobox"] {{
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #0F172A !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
        }}
        
        input:focus, select:focus, textarea:focus {{
            border-color: #10B981 !important;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.4) !important;
        }}

        /* Buttons Styling */
        .stButton > button {{
            background: linear-gradient(90deg, #059669 0%, #10B981 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.4);
        }}

        /* Metric Widgets */
        div[data-testid="stMetricValue"] {{
            color: #34D399 !important;
            font-weight: bold !important;
        }}
        
        div[data-testid="stMetricLabel"] {{
            color: #E2E8F0 !important;
        }}

        iframe {{
            background: #FFFFFF !important;
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_custom_background()

# --- 4. IMPORTS & DATA INITIALIZATION ---
from config import AFS_SECTION, EOS_SECTION
from utils import load_local_data, logout, save_local_data
from views.admin import render_admin_views
from views.auth import render_login_screen
from views.client import render_client_views

if HEADER_PATH and os.path.exists(HEADER_PATH):
    with open(HEADER_PATH, "rb") as f:
        st.session_state["slip_header_b64"] = base64.b64encode(f.read()).decode("utf-8")

if FOOTER_PATH and os.path.exists(FOOTER_PATH):
    with open(FOOTER_PATH, "rb") as f:
        st.session_state["slip_footer_b64"] = base64.b64encode(f.read()).decode("utf-8")

if LOGO_PATH and os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as f:
        st.session_state["logo_b64"] = base64.b64encode(f.read()).decode("utf-8")


def init_session_state():
    saved_emp, saved_tic, saved_cnt, saved_key, saved_channels, saved_admins = load_local_data()

    if "current_role" not in st.session_state:
        st.session_state.current_role = None

    if "login_stage" not in st.session_state:
        st.session_state.login_stage = "choose_role"

    if "logged_in_employee" not in st.session_state:
        st.session_state.logged_in_employee = None

    if "logged_in_admin" not in st.session_state:
        st.session_state.logged_in_admin = None

    if "is_admin_authenticated" not in st.session_state:
        st.session_state.is_admin_authenticated = False

    if "ticket_counter" not in st.session_state:
        st.session_state.ticket_counter = saved_cnt if saved_cnt is not None else 107

    if "employees" not in st.session_state:
        st.session_state.employees = saved_emp if saved_emp else []

    if "tickets" not in st.session_state:
        st.session_state.tickets = saved_tic if saved_tic else []

    if "admin_passkey" not in st.session_state:
        st.session_state.admin_passkey = saved_key if saved_key else "ADMIN2026"

    if "chat_channels" not in st.session_state:
        st.session_state.chat_channels = saved_channels if isinstance(saved_channels, dict) else {}

    if "admin_users" not in st.session_state:
        st.session_state.admin_users = saved_admins if saved_admins else []


init_session_state()


# --- 5. SIDEBAR LIVE CHAT ---
def render_sidebar_live_chat():
    with st.sidebar:
        with st.expander("💬 **IT Live Support Chat**", expanded=False):
            if st.session_state.get("current_role") == "admin":
                active_admin = st.session_state.get("logged_in_admin")
                admin_display_name = active_admin["name"] if active_admin and active_admin.get("name") else "IT Support Admin"

                st.caption(f"🛡️ Active Admin: **{admin_display_name}**")

                emp_list = st.session_state.get("employees", [])
                if not emp_list:
                    st.info("No registered clients found.")
                    return

                emp_map = {f"{e['name']} ({e['id']})": e["id"] for e in emp_list}
                selected_emp_label = st.selectbox("Select Client Chat Thread:", list(emp_map.keys()))
                target_client_id = emp_map[selected_emp_label]

                @st.fragment(run_every="3s")
                def render_admin_chat_thread():
                    _, _, _, _, latest_channels, _ = load_local_data()
                    st.session_state.chat_channels = latest_channels

                    client_messages = st.session_state.chat_channels.get(
                        target_client_id,
                        [{"sender": "IT Help Desk Admin", "role": "assistant", "content": "Hello! How can the IT Help Desk assist you today?"}],
                    )

                    for msg in client_messages:
                        sender = msg.get("sender", "User")
                        with st.chat_message(msg["role"]):
                            st.markdown(f"**{sender}**")
                            st.write(msg["content"])

                    if user_input := st.chat_input("Reply to client...", key=f"chat_input_admin_{target_client_id}"):
                        new_msg = {"sender": admin_display_name, "role": "assistant", "content": user_input}
                        if target_client_id not in st.session_state.chat_channels:
                            st.session_state.chat_channels[target_client_id] = [
                                {"sender": "IT Help Desk Admin", "role": "assistant", "content": "Hello! How can the IT Help Desk assist you today?"}
                            ]
                        st.session_state.chat_channels[target_client_id].append(new_msg)
                        save_local_data()
                        st.rerun()

                render_admin_chat_thread()

            elif st.session_state.get("logged_in_employee"):
                emp = st.session_state.logged_in_employee
                client_id = emp["id"]
                client_name = emp["name"]

                st.caption("🔒 Private Line to IT Help Desk Admin")

                @st.fragment(run_every="3s")
                def render_client_chat_thread():
                    _, _, _, _, latest_channels, _ = load_local_data()
                    st.session_state.chat_channels = latest_channels

                    client_messages = st.session_state.chat_channels.get(
                        client_id,
                        [{"sender": "IT Help Desk Admin", "role": "assistant", "content": f"Hello {client_name}! How can the IT Help Desk assist you today?"}],
                    )

                    for msg in client_messages:
                        sender = msg.get("sender", "User")
                        with st.chat_message(msg["role"]):
                            st.markdown(f"**{sender}**")
                            st.write(msg["content"])

                    if user_input := st.chat_input("Type message to IT...", key=f"chat_input_client_{client_id}"):
                        new_msg = {"sender": client_name, "role": "user", "content": user_input}
                        if client_id not in st.session_state.chat_channels:
                            st.session_state.chat_channels[client_id] = [
                                {"sender": "IT Help Desk Admin", "role": "assistant", "content": f"Hello {client_name}! How can the IT Help Desk assist you today?"}
                            ]
                        st.session_state.chat_channels[client_id].append(new_msg)
                        save_local_data()
                        st.rerun()

                render_client_chat_thread()

            else:
                st.info("Please log in to start a private chat with IT support.")


# --- 6. SIDEBAR NAVIGATION ---
client_menu, admin_menu = None, None

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
            admin_user = st.session_state.get("logged_in_admin")
            admin_name = admin_user["name"] if admin_user else "IT Admin"
            admin_role = admin_user.get("role", "Computer Maintenance Technologist I") if admin_user else "Computer Maintenance Technologist I"

            st.success(f"🛡️ Logged in as: **{admin_name}**")
            st.caption(f"Position: **{admin_role}**")
            st.markdown("---")
            admin_menu = st.radio(
                "Admin Navigation",
                ["📊 Ticket Management Dashboard", "👥 Employee / Client Management", "🔑 IT Admin Account Management"],
            )

        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True, key="sb_logout"):
            logout()
            st.rerun()

# --- 7. MAIN VIEW ROUTING ---
if st.session_state.current_role is None:
    render_login_screen(LOGO_PATH)
elif st.session_state.current_role == "client":
    render_client_views(client_menu)
elif st.session_state.current_role == "admin":
    render_admin_views(admin_menu)

render_sidebar_live_chat()