# weekly_report.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sheets_handler import get_analytics
from config import REPORT_RECIPIENTS, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_EMAIL, FROM_NAME
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime


def generate_pdf(filename, analytics):
    """Create a weekly analytics PDF."""
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 16)
    c.drawString(50, 750, "Weekly Outreach Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 700, f"Date: {datetime.date.today()}")

    c.drawString(50, 650, f"Total Leads: {analytics['total']}")
    c.drawString(50, 630, f"Emails Sent: {analytics['sent']}")
    c.drawString(50, 610, f"Replies Received: {analytics['replies']}")

    c.drawString(50, 570, "A/B Test Performance:")
    c.drawString(70, 550, f"Version A Sent: {analytics['a_sent']}")
    c.drawString(70, 530, f"Version B Sent: {analytics['b_sent']}")

    c.save()


def email_pdf(filename):
    """Send the weekly PDF via email."""
    msg = MIMEMultipart()
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = ", ".join(REPORT_RECIPIENTS)
    msg["Subject"] = "Weekly Outreach Report"

    msg.attach(MIMEText("Attached is your weekly outreach performance report.", "plain"))

    with open(filename, "rb") as f:
        pdf = MIMEApplication(f.read(), _subtype="pdf")
        pdf.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(pdf)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, REPORT_RECIPIENTS, msg.as_string())

    print("Weekly report sent!")


def run_weekly_report():
    analytics = get_analytics()
    filename = "weekly_report.pdf"

    generate_pdf(filename, analytics)
    email_pdf(filename)


if __name__ == "__main__":
    run_weekly_report()
