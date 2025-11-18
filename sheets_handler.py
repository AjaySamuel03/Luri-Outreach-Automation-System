# sheets_handler.py

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import SPREADSHEET_NAME, MAIN_SHEET_NAME

# Google Sheets authentication
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet():
    """Connect to Google Sheets and return worksheet."""
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(MAIN_SHEET_NAME)
    return sheet


def get_unsent_leads():
    """Returns all leads where Status = 'Not Sent'."""
    sheet = get_sheet()
    data = sheet.get_all_records()

    unsent = []
    for i, row in enumerate(data, start=2):  # start=2 because row 1 is headers
        if row.get("Status") == "Not Sent":
            unsent.append((i, row))

    return unsent


def update_status(row_index, status):
    """Updates the Status column."""
    sheet = get_sheet()
    sheet.update_cell(row_index, 9, status)  # Column I = Status

    if status == "Sent":
        sheet.update_cell(row_index, 10, datetime.now().strftime("%Y-%m-%d"))  # Date Sent


def update_reply_type(row_index, reply_type):
    """Marks reply type manually if needed."""
    sheet = get_sheet()
    sheet.update_cell(row_index, 11, reply_type)


def mark_followup(row_index, which):
    """Marks follow-up as sent."""
    sheet = get_sheet()
    sheet.update_cell(row_index, 12, f"Follow-up {which}")
    sheet.update_cell(row_index, 13, datetime.now().strftime("%Y-%m-%d"))


def get_leads_for_followup(days):
    """
    Fetch leads where:
    - Status = Sent
    - Follow up not sent
    - Date Sent is X days old
    """
    sheet = get_sheet()
    data = sheet.get_all_records()

    results = []
    today = datetime.now()

    for i, row in enumerate(data, start=2):
        status = row.get("Status")
        date_sent = row.get("Date Sent")
        followup = row.get("Follow Up Sent")

        if status != "Sent" or not date_sent:
            continue

        sent_date = datetime.strptime(date_sent, "%Y-%m-%d")
        diff = (today - sent_date).days

        if diff >= days and (not followup or followup == ""):
            results.append((i, row))

    return results


def get_analytics():
    """Returns total leads, sent emails, replies, A/B stats."""
    sheet = get_sheet()
    data = sheet.get_all_records()

    total = len(data)
    sent = sum(1 for r in data if r.get("Status") == "Sent")
    replies = sum(1 for r in data if r.get("Reply Type"))
    
    a_count = sum(1 for r in data if r.get("A/B Version") == "A" and r.get("Status") == "Sent")
    b_count = sum(1 for r in data if r.get("A/B Version") == "B" and r.get("Status") == "Sent")

    return {
        "total": total,
        "sent": sent,
        "replies": replies,
        "a_sent": a_count,
        "b_sent": b_count
    }
