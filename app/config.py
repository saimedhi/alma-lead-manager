import os
from dotenv import load_dotenv

# Load variables from .env in project root
load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")

# Internal API key
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "alma-admin-98765")

# Attorney fallback email
ATTORNEY_EMAIL = os.getenv("ATTORNEY_EMAIL", "helpdesk@alma-legal.com")

# SMTP settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USER or "")

# Debug to confirm envs are loaded
print("SMTP_DEBUG:", SMTP_HOST, SMTP_USER, bool(SMTP_PASSWORD))
