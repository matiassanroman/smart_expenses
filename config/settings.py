import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# IMAP configuration
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SEARCH_FROM = os.getenv("SEARCH_FROM")
SEARCH_SUBJECT = os.getenv("SEARCH_SUBJECT")

# Google Sheets configuration
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH")
