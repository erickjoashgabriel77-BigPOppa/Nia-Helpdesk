import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "helpdesk_data.json")

# Administrative security passkey for IT Staff login
ADMIN_PASSKEY = "ADMIN2026"

# Agency Sections
EOS_SECTION = "Engineering & Operations (EOS)"
AFS_SECTION = "Administrative & Finance (AFS)"

# Organizational Units mapped to their respective Sections
ORGANIZATIONAL_UNITS = {
    EOS_SECTION: [
        "Planning & Design Unit",
        "Construction Unit",
        "Operations & Maintenance Unit",
        "Equipment Management"
    ],
    AFS_SECTION: [
        "Administrative & Finance Section",
        "Accounting Unit",
        "Human Resources",
        "Procurement & Property"
    ]
}

# IT Staff available for ticket assignment
IT_TECHNICIANS = [
    "Unassigned",
    "IT Admin Lead",
    "Network Technician",
    "Hardware Specialist",
    "Support Staff"
]

# Default fallback employee roster for the local JSON store
DEFAULT_EMPLOYEES = [
    {
        "id": "EMP-EOS-001",
        "name": "Erick Joash Jasmin Gabriel",
        "section": EOS_SECTION,
        "unit": "Planning & Design Unit"
    },
    {
        "id": "EMP-AFS-001",
        "name": "Maria Santos",
        "section": AFS_SECTION,
        "unit": "Administrative & Finance Section"
    }
]

# Default sample ticket entries
DEFAULT_TICKETS = [
    {
        "id": "TIC-105",
        "employee_id": "EMP-EOS-001",
        "employee_name": "Erick Joash Jasmin Gabriel",
        "section": EOS_SECTION,
        "unit": "Planning & Design Unit",
        "category": "Hardware / Workstation",
        "description": "Initial configuration and LAN deployment test for NIA-Quirino IMO Help Desk.",
        "status": "Resolved",
        "date": "2026-09-28",
        "assigned_tech": "IT Admin Lead",
        "resolution_notes": "Verified local server connection across office network.",
        "rating": None,
        "feedback": ""
    }
]