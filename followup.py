# followup.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_NAME, FROM_EMAIL
from sheets_handler import get_leads_for_followup, mark_followup
import os


def load_template(name):
    """Load HTML email from templates folder."""
    path = os.path.join("templates", name + ".html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def send_email(to_email, subject, html_body):
    """Send email with SMTP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())


def process_followups():
    """Send 3-day and 7-day followups automatically."""

    print("Checking for 3-day followups...")
    leads_3 = get_leads_for_followup(3)

    for row_index, row in leads_3:
        name = row.get("Name")
        email = row.get("E-Mail")
        firm = row.get("Firm")

        html = load_template("followup1")
        html = html.replace("{name}", name)
        html = html.replace("{firm}", firm)

        subject = "Quick Follow-up"

        try:
            send_email(email, subject, html)
            mark_followup(row_index, 1)
            print(f"Sent 3-day followup → {name} ({email})")

        except Exception as e:
            print(f"Error sending followup to {email}: {e}")

    print("Checking for 7-day followups...")
    leads_7 = get_leads_for_followup(7)

    for row_index, row in leads_7:
        name = row.get("Name")
        email = row.get("E-Mail")
        firm = row.get("Firm")

        html = load_template("followup2")
        html = html.replace("{name}", name)
        html = html.replace("{firm}", firm)

        subject = "Following Up Again"

        try:
            send_email(email, subject, html)
            mark_followup(row_index, 2)
            print(f"Sent 7-day followup → {name} ({email})")

        except Exception as e:
            print(f"Error sending followup to {email}: {e}")


if __name__ == "__main__":
    process_followups()
