import smtplib
from email.mime.text import MIMEText
from typing import Optional

from .config import (
    ATTORNEY_EMAIL,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    SENDER_EMAIL,
)


def send_raw_email(recipient: str, subject: str, body: str) -> None:
    # Debug log
    print("SEND_EMAIL_DEBUG:", SMTP_HOST, SMTP_USER, bool(SMTP_PASSWORD), "->", recipient)

    # Build the email
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL or SMTP_USER
    msg["To"] = recipient

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg["From"], [recipient], msg.as_string())
        print("EMAIL_SENT:", recipient)
    except Exception as e:
        print("EMAIL_ERROR:", recipient, e)


def send_email_to_prospect(email: str, lead_id: int) -> None:
    subject = f"Thank you for contacting Alma, lead {lead_id}"
    body = (
        "Thank you for reaching out. "
        "Our team has received your information and someone will contact you soon."
    )
    send_raw_email(email, subject, body)


def send_email_to_attorney(attorney_email: Optional[str], lead_id: int) -> None:
    recipient = attorney_email or ATTORNEY_EMAIL
    subject = f"New lead submitted, id {lead_id}"
    body = (
        f"A new lead has been created with id {lead_id}. "
        "Please review it in the internal tool."
    )
    send_raw_email(recipient, subject, body)
