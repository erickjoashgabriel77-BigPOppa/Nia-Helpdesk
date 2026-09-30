import os
import json
import base64
import streamlit as st
from config import DATA_FILE, DEFAULT_EMPLOYEES, DEFAULT_TICKETS, ADMIN_PASSKEY, DEFAULT_ADMINS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_local_data():
    """Loads helpdesk data, admin users, and chat channels from local JSON storage."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return (
                    data.get("employees", []),
                    data.get("tickets", []),
                    data.get("ticket_counter", 107),
                    data.get("admin_passkey", ADMIN_PASSKEY),
                    data.get("chat_channels", {}),
                    data.get("admin_users", DEFAULT_ADMINS)
                )
        except Exception:
            pass
    return DEFAULT_EMPLOYEES, DEFAULT_TICKETS, 107, ADMIN_PASSKEY, {}, DEFAULT_ADMINS

def save_local_data():
    """Saves current session state including admin users to local JSON file."""
    data = {
        "employees": st.session_state.get("employees", []),
        "tickets": st.session_state.get("tickets", []),
        "ticket_counter": st.session_state.get("ticket_counter", 107),
        "admin_passkey": st.session_state.get("admin_passkey", ADMIN_PASSKEY),
        "chat_channels": st.session_state.get("chat_channels", {}),
        "admin_users": st.session_state.get("admin_users", DEFAULT_ADMINS)
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_employee_by_id(emp_id):
    """Finds employee dictionary by employee ID."""
    for emp in st.session_state.get("employees", []):
        if emp.get("id") == emp_id:
            return emp
    return None

def logout():
    """Clears user session state on logout."""
    st.session_state.current_role = None
    st.session_state.logged_in_employee = None
    st.session_state.is_admin_authenticated = False
    st.session_state.login_stage = "choose_role"

def generate_printable_ticket_html(ticket):
    """Generates an ISO-formatted printable service slip using the assigned technician's name."""
    header_b64 = st.session_state.get("slip_header_b64", "")
    footer_b64 = st.session_state.get("slip_footer_b64", "")

    if not header_b64:
        for ext in ["png", "jpg", "jpeg"]:
            hp = os.path.join(BASE_DIR, "Media", f"TicketSLIP_header.{ext}")
            if os.path.exists(hp):
                with open(hp, "rb") as f:
                    header_b64 = base64.b64encode(f.read()).decode("utf-8")
                break

    if not footer_b64:
        for ext in ["png", "jpg", "jpeg"]:
            fp = os.path.join(BASE_DIR, "Media", f"TicketSLIP_Footer.{ext}")
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    footer_b64 = base64.b64encode(f.read()).decode("utf-8")
                break

    header_img_tag = f'<img src="data:image/png;base64,{header_b64}" style="width: 100%; max-height: 105px; object-fit: contain; display: block; margin: 0 auto;">' if header_b64 else ""
    footer_img_tag = f'<img src="data:image/png;base64,{footer_b64}" style="width: 100%; height: 100%; object-fit: fill; display: block;">' if footer_b64 else ""

    emp_name = ticket.get('employee_name', '')
    
    # Retrieve designation from employee profile
    emp_obj = get_employee_by_id(ticket.get('employee_id'))
    designation = emp_obj.get('designation', '') if emp_obj else ''

    req_date = ticket.get('date', ticket.get('created_at', ''))
    office = f"{ticket.get('section', '')} / {ticket.get('unit', '')}"
    problem = ticket.get('description', '')
    remarks = ticket.get('resolution_notes', '')
    
    # Extract IT Technician Name (filter out position titles and 'Unassigned')
    assigned_tech = ticket.get('assigned_tech', '')
    if assigned_tech in ["Computer Maintenance Technologist I", "Unassigned", None]:
        tech_display = ""
    else:
        tech_display = str(assigned_tech).upper()

    rating = str(ticket.get('rating', ''))
    vs_check = "☑" if rating == "5" else "☐"
    s_check = "☑" if rating in ["4", "3"] else "☐"
    n_check = "☑" if rating == "2" else "☐"
    p_check = "☑" if rating == "1" else "☐"
    feedback = ticket.get('feedback', '')

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IT SERVICE TICKET - {ticket.get('id', 'N/A')}</title>
        <style>
            @page {{ size: A4 portrait; margin: 4mm 6mm; }}
            html, body {{ height: 100%; margin: 0; padding: 0; background: #fff; font-family: 'Times New Roman', serif; color: #000; font-size: 12pt; }}
            .ticket-box {{ border: 2px solid #000; padding: 10px 14px 0 14px; width: 100%; max-width: 820px; min-height: 97vh; margin: 0 auto; box-sizing: border-box; position: relative; display: flex; flex-direction: column; justify-content: space-between; page-break-inside: avoid; }}
            .content-wrapper {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 2; }}
            .html-header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 4px; margin-bottom: 4px; }}
            .ticket-title {{ text-align: center; margin: 4px 0 6px 0; }}
            .ticket-title h2 {{ margin: 0; font-size: 17pt; font-weight: bold; text-decoration: underline; letter-spacing: 1px; }}
            .section-title {{ font-weight: bold; background-color: #e5e7eb; border: 1px solid #000; padding: 4px 6px; text-align: center; font-size: 12pt; margin-top: 8px; margin-bottom: 4px; text-transform: uppercase; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 12pt; table-layout: fixed; }}
            td {{ border: 1px solid #000; padding: 5px 8px; vertical-align: top; word-wrap: break-word; word-break: break-word; overflow-wrap: anywhere; }}
            .label {{ font-weight: bold; }}
            .signature-block {{ text-align: center; margin-top: 25px; }}
            .signature-line {{ border-top: 1px solid #000; width: 85%; margin: 0 auto; padding-top: 2px; font-size: 9.5pt; }}
            .blank-space {{ min-height: 36px; word-wrap: break-word; word-break: break-word; overflow-wrap: anywhere; white-space: pre-wrap; line-height: 1.3; }}
            .html-footer {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 80px; border-top: 2px solid #059669; z-index: 1; }}
            @media print {{ .no-print {{ display: none; }} html, body {{ height: 100%; width: 100%; }} .ticket-box {{ border: 2px solid #000; padding: 8px 12px 0 12px; height: 98vh; min-height: 98vh; }} }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 12px;">
            <button onclick="window.print()" style="padding: 10px 20px; font-size: 14px; background: #059669; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">🖨️ Print to Single Page A4</button>
        </div>
        
        <div class="ticket-box">
            <div class="content-wrapper">
                <div>
                    <div class="html-header">{header_img_tag}</div>
                    <div class="ticket-title">
                        <h2>IT SERVICE TICKET</h2>
                        <div style="text-align: right; font-size: 11pt; margin-top: 2px;">Ticket ID: <strong>{ticket.get('id', 'N/A')}</strong></div>
                    </div>

                    <div class="section-title">CLIENT DETAILS</div>
                    <table>
                        <tr><td colspan="2"><span class="label">Name:</span> {emp_name}</td></tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Designation:</span> {designation}</td>
                            <td style="width: 50%;"><span class="label">Date:</span> {req_date}</td>
                        </tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Division/Section/Office:</span> {office}</td>
                            <td style="width: 50%;"><span class="label">Time:</span> </td>
                        </tr>
                        <tr>
                            <td colspan="2"><span class="label">Problem reported:</span><br><div class="blank-space">{problem}</div></td>
                        </tr>
                        <tr>
                            <td style="width: 50%;">
                                <span class="label">Client's signature:</span>
                                <div class="signature-block"><div class="signature-line"></div></div>
                            </td>
                            <td style="width: 50%;">
                                <span class="label">Noted by:</span>
                                <div class="signature-block"><div class="signature-line">CLIENT'S SUPERVISOR SIGNATURE<br>OVER PRINTED NAME</div></div>
                            </td>
                        </tr>
                    </table>

                    <div class="section-title">RECEIVED EQUIPMENT DETAILS</div>
                    <table>
                        <tr>
                            <td style="width: 50%;"><span class="label">Date and time received:</span> </td>
                            <td style="width: 50%;"><span class="label">Accessories:</span> </td>
                        </tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Serial number:</span> </td>
                            <td style="width: 50%;"><span class="label">Equipment type:</span> </td>
                        </tr>
                    </table>

                    <div class="section-title">SERVICE DETAILS</div>
                    <table>
                        <tr><td colspan="2"><span class="label">Problem found:</span><div class="blank-space"></div></td></tr>
                        <tr><td colspan="2"><span class="label">IT personnel remarks:</span><div class="blank-space">{remarks}</div></td></tr>
                        <tr>
                            <td style="width: 50%;">
                                <span class="label">Acknowledge by:</span>
                                <div class="signature-block" style="margin-top: 15px;">
                                    <div style="font-weight: bold; margin-bottom: 2px;">{tech_display}</div>
                                    <div class="signature-line">IT PERSONNEL SIGNATURE<br>OVER PRINTED NAME</div>
                                </div>
                                <div style="margin-top: 10px;"><span class="label">Date and time resolved:</span> </div>
                            </td>
                            <td style="width: 50%;">
                                <span class="label">Overall service satisfaction rate:</span><br>
                                <div style="margin-top: 6px; line-height: 1.5;">
                                    {vs_check} Very Satisfied<br>
                                    {s_check} Satisfied<br>
                                    {n_check} Neutral<br>
                                    {p_check} Poor
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2"><span class="label">How can we improve our service?</span><div class="blank-space">{feedback}</div></td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="html-footer">{footer_img_tag}</div>
        </div>
    </body>
    </html>
    """
    """Generates an ISO-formatted printable service slip."""
    header_b64 = st.session_state.get("slip_header_b64", "")
    footer_b64 = st.session_state.get("slip_footer_b64", "")

    if not header_b64:
        for ext in ["png", "jpg", "jpeg"]:
            hp = os.path.join(BASE_DIR, "Media", f"TicketSLIP_header.{ext}")
            if os.path.exists(hp):
                with open(hp, "rb") as f:
                    header_b64 = base64.b64encode(f.read()).decode("utf-8")
                break

    if not footer_b64:
        for ext in ["png", "jpg", "jpeg"]:
            fp = os.path.join(BASE_DIR, "Media", f"TicketSLIP_Footer.{ext}")
            if os.path.exists(fp):
                with open(fp, "rb") as f:
                    footer_b64 = base64.b64encode(f.read()).decode("utf-8")
                break

    header_img_tag = f'<img src="data:image/png;base64,{header_b64}" style="width: 100%; max-height: 105px; object-fit: contain; display: block; margin: 0 auto;">' if header_b64 else ""
    footer_img_tag = f'<img src="data:image/png;base64,{footer_b64}" style="width: 100%; height: 100%; object-fit: fill; display: block;">' if footer_b64 else ""

    emp_name = ticket.get('employee_name', '')
    
    # Retrieve designation from employee profile
    emp_obj = get_employee_by_id(ticket.get('employee_id'))
    designation = emp_obj.get('designation', '') if emp_obj else ''

    req_date = ticket.get('date', ticket.get('created_at', ''))
    office = f"{ticket.get('section', '')} / {ticket.get('unit', '')}"
    problem = ticket.get('description', '')
    remarks = ticket.get('resolution_notes', '')
    assigned_tech = ticket.get('assigned_tech', '')
    
    rating = str(ticket.get('rating', ''))
    vs_check = "☑" if rating == "5" else "☐"
    s_check = "☑" if rating in ["4", "3"] else "☐"
    n_check = "☑" if rating == "2" else "☐"
    p_check = "☑" if rating == "1" else "☐"
    feedback = ticket.get('feedback', '')

    tech_display = assigned_tech.upper() if assigned_tech and assigned_tech != "Unassigned" else ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IT SERVICE TICKET - {ticket.get('id', 'N/A')}</title>
        <style>
            @page {{ size: A4 portrait; margin: 4mm 6mm; }}
            html, body {{ height: 100%; margin: 0; padding: 0; background: #fff; font-family: 'Times New Roman', serif; color: #000; font-size: 12pt; }}
            .ticket-box {{ border: 2px solid #000; padding: 10px 14px 0 14px; width: 100%; max-width: 820px; min-height: 97vh; margin: 0 auto; box-sizing: border-box; position: relative; display: flex; flex-direction: column; justify-content: space-between; page-break-inside: avoid; }}
            .content-wrapper {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 2; }}
            .html-header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 4px; margin-bottom: 4px; }}
            .ticket-title {{ text-align: center; margin: 4px 0 6px 0; }}
            .ticket-title h2 {{ margin: 0; font-size: 17pt; font-weight: bold; text-decoration: underline; letter-spacing: 1px; }}
            .section-title {{ font-weight: bold; background-color: #e5e7eb; border: 1px solid #000; padding: 4px 6px; text-align: center; font-size: 12pt; margin-top: 8px; margin-bottom: 4px; text-transform: uppercase; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 12pt; table-layout: fixed; }}
            td {{ border: 1px solid #000; padding: 5px 8px; vertical-align: top; word-wrap: break-word; word-break: break-word; overflow-wrap: anywhere; }}
            .label {{ font-weight: bold; }}
            .signature-block {{ text-align: center; margin-top: 25px; }}
            .signature-line {{ border-top: 1px solid #000; width: 85%; margin: 0 auto; padding-top: 2px; font-size: 9.5pt; }}
            .blank-space {{ min-height: 36px; word-wrap: break-word; word-break: break-word; overflow-wrap: anywhere; white-space: pre-wrap; line-height: 1.3; }}
            .html-footer {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 80px; border-top: 2px solid #059669; z-index: 1; }}
            @media print {{ .no-print {{ display: none; }} html, body {{ height: 100%; width: 100%; }} .ticket-box {{ border: 2px solid #000; padding: 8px 12px 0 12px; height: 98vh; min-height: 98vh; }} }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: center; margin-bottom: 12px;">
            <button onclick="window.print()" style="padding: 10px 20px; font-size: 14px; background: #059669; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">🖨️ Print to Single Page A4</button>
        </div>
        
        <div class="ticket-box">
            <div class="content-wrapper">
                <div>
                    <div class="html-header">{header_img_tag}</div>
                    <div class="ticket-title">
                        <h2>IT SERVICE TICKET</h2>
                        <div style="text-align: right; font-size: 11pt; margin-top: 2px;">Ticket ID: <strong>{ticket.get('id', 'N/A')}</strong></div>
                    </div>

                    <div class="section-title">CLIENT DETAILS</div>
                    <table>
                        <tr><td colspan="2"><span class="label">Name:</span> {emp_name}</td></tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Designation:</span> {designation}</td>
                            <td style="width: 50%;"><span class="label">Date:</span> {req_date}</td>
                        </tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Division/Section/Office:</span> {office}</td>
                            <td style="width: 50%;"><span class="label">Time:</span> </td>
                        </tr>
                        <tr>
                            <td colspan="2"><span class="label">Problem reported:</span><br><div class="blank-space">{problem}</div></td>
                        </tr>
                        <tr>
                            <td style="width: 50%;">
                                <span class="label">Client's signature:</span>
                                <div class="signature-block"><div class="signature-line"></div></div>
                            </td>
                            <td style="width: 50%;">
                                <span class="label">Noted by:</span>
                                <div class="signature-block"><div class="signature-line">CLIENT'S SUPERVISOR SIGNATURE<br>OVER PRINTED NAME</div></div>
                            </td>
                        </tr>
                    </table>

                    <div class="section-title">RECEIVED EQUIPMENT DETAILS</div>
                    <table>
                        <tr>
                            <td style="width: 50%;"><span class="label">Date and time received:</span> </td>
                            <td style="width: 50%;"><span class="label">Accessories:</span> </td>
                        </tr>
                        <tr>
                            <td style="width: 50%;"><span class="label">Serial number:</span> </td>
                            <td style="width: 50%;"><span class="label">Equipment type:</span> </td>
                        </tr>
                    </table>

                    <div class="section-title">SERVICE DETAILS</div>
                    <table>
                        <tr><td colspan="2"><span class="label">Problem found:</span><div class="blank-space"></div></td></tr>
                        <tr><td colspan="2"><span class="label">IT personnel remarks:</span><div class="blank-space">{remarks}</div></td></tr>
                        <tr>
                            <td style="width: 50%;">
                                <span class="label">Acknowledge by:</span>
                                <div class="signature-block" style="margin-top: 15px;">
                                    <div style="font-weight: bold; margin-bottom: 2px;">{tech_display}</div>
                                    <div class="signature-line">IT PERSONNEL SIGNATURE<br>OVER PRINTED NAME</div>
                                </div>
                                <div style="margin-top: 10px;"><span class="label">Date and time resolved:</span> </div>
                            </td>
                            <td style="width: 50%;">
                                <span class="label">Overall service satisfaction rate:</span><br>
                                <div style="margin-top: 6px; line-height: 1.5;">
                                    {vs_check} Very Satisfied<br>
                                    {s_check} Satisfied<br>
                                    {n_check} Neutral<br>
                                    {p_check} Poor
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2"><span class="label">How can we improve our service?</span><div class="blank-space">{feedback}</div></td>
                        </tr>
                    </table>
                </div>
            </div>

            <div class="html-footer">{footer_img_tag}</div>
        </div>
    </body>
    </html>
    """