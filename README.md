Luri Outreach Automation System:
Automated Email Outreach • Follow-ups • Google Sheets Integration • Weekly PDF Reports
🚀 Overview

The Luri Outreach Automation System is an end-to-end outreach automation tool designed to:

✔ Send personalized initial outreach emails
✔ Track email status inside Google Sheets
✔ Automatically send 3-day & 7-day follow-up emails
✔ Generate weekly analytics reports as a PDF
✔ Email the weekly report to managers
✔ Allow multiple email templates (A/B versions)

This automation removes all manual work from outreach and follow-up cycles.

🧩 Features
1️⃣ Automated Email Outreach

Picks unsent leads from Google Sheets

Sends personalized emails using HTML templates

Updates status (Sent) and reply types in the sheet

2️⃣ Automated Follow-ups

3-day follow-ups
7-day follow-ups
Tracks follow-up stage in Google Sheets

3️⃣ Weekly PDF Report

Total leads
Emails sent
Replies received
A/B test performance
Automatically emailed to designated recipients

4️⃣ Google Sheets Integration

Reads/writes data through Google Sheets API
Uses service account authentication

📁 Project Structure:
Luri_automation/
│
├── templates/
│     ├── complainer_a.html
│     ├── complainer_b.html
│     ├── suite_a.html
│     ├── suite_b.html
│     ├── followup1.html
│     └── followup2.html
│
├── send_emails.py
├── followup.py
├── weekly_report.py
├── sheets_handler.py
├── config.py
├── requirements.txt
└── service_account.json.example

⚙️ Installation & Setup:
1️⃣ Create Virtual Environment
python -m venv .venv
.\.venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Google Service Account Key

Go to Google Cloud Console
Create a service account
Generate a JSON key
Rename it to:service_account.json

Automate with Task Scheduler (Windows)
You can automate scripts daily/weekly:
Daily at 10 AM (Outreach & Follow-up)
Create Task → Run:
python F:\Luri_automation\send_emails.py
python F:\Luri_automation\followup.py
Weekly Monday 9 AM (Weekly Report):
python F:\Luri_automation\weekly_report.py



👨‍💻 Technology Stack
Python
Google Sheets API
Gmail SMTP
ReportLab (PDF Generation)
HTML Templates
Virtual Environment

