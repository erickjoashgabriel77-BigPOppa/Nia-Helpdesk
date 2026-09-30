import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    """Initializes connection to Supabase using Streamlit Secrets."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def load_local_data():
    """Fetches employees, tickets, ticket counter, and admin key directly from Supabase."""
    try:
        supabase = get_supabase_client()
        
        # 1. Fetch Employees
        emp_res = supabase.table("employees").select("*").execute()
        employees = emp_res.data if emp_res.data else []

        # 2. Fetch Tickets
        tic_res = supabase.table("tickets").select("*").order("id", desc=True).execute()
        tickets = tic_res.data if tic_res.data else []

        # 3. Calculate Next Ticket Counter
        counter = (tickets[0]["id"] + 1) if tickets else 107

        # 4. Fetch Admin Passkey from Secrets (or fallback)
        admin_key = st.secrets.get("ADMIN_PASSKEY", "ADMIN2026")

        return employees, tickets, counter, admin_key
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return [], [], 107, "ADMIN2026"

def save_local_data(employees=None, tickets=None, counter=None, admin_key=None):
    """Compatibility function that syncs state updates back to Supabase."""
    supabase = get_supabase_client()
    
    if employees is not None:
        for emp in employees:
            supabase.table("employees").upsert(emp).execute()

    if tickets is not None:
        for ticket in tickets:
            supabase.table("tickets").upsert(ticket).execute()

def save_ticket_to_cloud(ticket_data):
    """Inserts a single new ticket into Supabase."""
    supabase = get_supabase_client()
    supabase.table("tickets").insert(ticket_data).execute()

def update_ticket_chat_in_cloud(ticket_id, updated_chat_list):
    """Updates live chat history for a specific ticket."""
    supabase = get_supabase_client()
    supabase.table("tickets").update({"chat": updated_chat_list}).eq("id", ticket_id).execute()

def logout():
    """Resets session variables."""
    st.session_state.current_role = None
    st.session_state.logged_in_employee = None
    st.session_state.is_admin_authenticated = False