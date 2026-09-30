import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

def get_employee_by_id(emp_id: str):
    """Fetch employee details from Supabase by employee ID."""
    try:
        response = supabase.table("employees").select("*").eq("employee_id", emp_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Error fetching employee details: {e}")
        return None

def submit_ticket(emp_id: str, issue_type: str, description: str, priority: str):
    """Insert a new IT support ticket into Supabase."""
    try:
        data = {
            "employee_id": emp_id,
            "issue_type": issue_type,
            "description": description,
            "priority": priority,
            "status": "Open"
        }
        response = supabase.table("tickets").insert(data).execute()
        return response.data
    except Exception as e:
        st.error(f"Error submitting ticket: {e}")
        return None

def get_all_tickets():
    """Retrieve all helpdesk tickets sorted by newest first."""
    try:
        response = supabase.table("tickets").select("*").order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching tickets: {e}")
        return []

def update_ticket_status(ticket_id: int, new_status: str):
    """Update the resolution status of a specific ticket."""
    try:
        response = supabase.table("tickets").update({"status": new_status}).eq("id", ticket_id).execute()
        return response.data
    except Exception as e:
        st.error(f"Error updating ticket status: {e}")
        return None