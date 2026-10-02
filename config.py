# ==========================================
# config.py
# ==========================================
import os

# --- 1. DIRECTORY SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "helpdesk_data.json")

# --- 2. SECURITY & ADMIN DEFAULTS ---
ADMIN_PASSKEY = "1234"

DEFAULT_ADMINS = [
    {
        "id": "ADM-001",
        "name": "LeBron James",
        "role": "Computer Maintenance Technologist I",
        "passkey": "ADMIN2026"
    }
]

# --- 3. AGENCY SECTIONS & UNITS ---
EOS_SECTION = "Engineering & Operations Section (EOS)"
AFS_SECTION = "Administrative & Finance Section (AFS)"

ORGANIZATIONAL_UNITS = {
    EOS_SECTION: [
        "Construction Management Unit",
        "Planning, Design and Survey Unit",
        "Equipment Management Unit",
        "Institutional Development Unit"
    ],
    AFS_SECTION: [
        "Administrative Unit",
        "Finance Unit"
    ]
}

IT_TECHNICIANS = [
    "Unassigned",
    "Computer Maintenance Technologist I"
]

# --- 4. DEFAULT MOCK DATA ---
DEFAULT_EMPLOYEES = [
    {
        "id": "EMP-EOS-001",
        "name": "Engr. Juan Dela Cruz",
        "designation": "Engineer A",
        "section": EOS_SECTION,
        "unit": "Construction Management Unit"
    },
    {
        "id": "EMP-AFS-001",
        "name": "Maria Santos",
        "designation": "Administrative Officer I",
        "section": AFS_SECTION,
        "unit": "Administrative Unit"
    }
]

# Unified Ticket Schema
DEFAULT_TICKETS = [
    {
        "id": "TIC-105",
        "client_id": "EMP-EOS-001",
        "client_name": "Engr. Juan Dela Cruz",
        "section": EOS_SECTION,
        "unit": "Construction Management Unit",
        "position": "Engineer A",
        "supervisor": "N/A",
        "request_type": "Hardware Repair / Maintenance",
        "urgency": "Medium",
        "equipment_type": "Desktop PC",
        "serial_number": "SN-001",
        "description": "Initial configuration and LAN deployment test for NIA-Quirino IMO Help Desk.",
        "status": "Completed",
        "date_created": "2026-09-28 10:00 AM",
        "action_taken": "Verified local server connection across office network.",
        "serviced_by": "Computer Maintenance Technologist I",
        "rating": 5,
        "feedback": "Great service!"
    }
]