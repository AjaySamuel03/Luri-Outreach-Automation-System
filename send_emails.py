# send_emails.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_NAME, FROM_EMAIL
from sheets_handler import get_unsent_leads, update_status
import os

def load_template(name):
    """Load HTML email from the templates folder."""
    path = os.path.join("templates", name + ".html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def send_email(to_email, subject, html_body):
    """Send an email using SMTP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())


def process_outreach():
    """Main function to process unsent leads."""
    leads = get_unsent_leads()

    if not leads:
        print("No new leads to send.")
        return

    for row_index, row in leads:
        name = row.get("Name")
        email = row.get("E-Mail")
        firm = row.get("Firm")
        template_name = row.get("Email Template")

        # Load template file
        html = load_template(template_name)

        # Replace placeholders
        html = html.replace("{name}", name)
        html = html.replace("{firm}", firm)

        subject = "Quick Question for " + firm

        try:
            send_email(email, subject, html)
            update_status(row_index, "Sent")
            print(f"Email sent → {name} ({email})")

        except Exception as e:
            print(f"Error sending email to {email}: {e}")


if __name__ == "__main__":
    process_outreach()
