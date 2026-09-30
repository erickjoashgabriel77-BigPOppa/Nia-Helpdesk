import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "helpdesk_data.json")

# Security & Admin defaults
ADMIN_PASSKEY = "1234"

DEFAULT_ADMINS = [
    {
        "id": "ADM-001",
        "name": "LeBron James",
        "role": "Computer Maintenance Technologist I",
        "passkey": "ADMIN2026"
    }
]

# Agency Sections
EOS_SECTION = "Engineering & Operations Section (EOS)"
AFS_SECTION = "Administrative & Finance Section (AFS)"

# Official Organizational Units mapped to their respective Sections
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

# Standard IT Technicians for ticket assignment
IT_TECHNICIANS = [
    "Unassigned",
    "Computer Maintenance Technologist I"
]

# Default fallback employee roster for local JSON store
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

# Default sample ticket entries
DEFAULT_TICKETS = [
    {
        "id": "TIC-105",
        "employee_id": "EMP-EOS-001",
        "employee_name": "Engr. Juan Dela Cruz",
        "section": EOS_SECTION,
        "unit": "Construction Management Unit",
        "category": "Hardware / Workstation",
        "description": "Initial configuration and LAN deployment test for NIA-Quirino IMO Help Desk.",
        "status": "Resolved",
        "date": "2026-09-28",
        "assigned_tech": "Computer Maintenance Technologist I",
        "resolution_notes": "Verified local server connection across office network.",
        "rating": None,
        "feedback": ""
    }
]