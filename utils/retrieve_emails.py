"""Email retrieval and extraction of expenses."""

import email
import logging
from typing import List
import re

from config.settings import SEARCH_FROM, SEARCH_SUBJECT, SEARCH_SUBJECT_2

from utils.connection import establish_connection, login, logout
from utils.parser import parse_body, parse_date

logger = logging.getLogger(__name__)


def _get_text_from_message(msg) -> str:
    """
    Extract the text/plain payload from an email.message.Message.
    """
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode("utf-8", errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode("utf-8", errors="ignore")
    return body


def retrieve_expenses(
    since_date: str,
    next_date: str,
    from_filter: str = SEARCH_FROM,
    subject_filter: str = SEARCH_SUBJECT,
    subject_filter_2: str = SEARCH_SUBJECT_2
) -> List[dict]:
    """
    Connects to IMAP, searches emails and returns a list of expense dicts.
    Each dict contains keys: 'fecha', 'importe', 'detalle' (or empty strings if missing).
    """
    imap = establish_connection()
    if imap is None:
        logger.error("Could not establish IMAP connection.")
        return []

    login_resp_code, login_resp = login(imap)
    if login_resp_code is None:
        logger.error("Login failed; aborting email retrieval.")
        return []

    try:
        print(SEARCH_SUBJECT_2) 
        print(SEARCH_SUBJECT)
        imap.select("inbox")
        criteria = (
            f'FROM "{from_filter}" '
            f'OR (SUBJECT "{subject_filter}") (SUBJECT "{subject_filter_2}") '
            f'SINCE {since_date} BEFORE {next_date}'
        )
        status, data = imap.search(None, criteria)

        if status != "OK":
            logger.error("IMAP search failed: %s", status)
            return []

        mail_ids = data[0].split()
        expenses = []
        for mail_id in mail_ids:
            status, fetch_data = imap.fetch(mail_id, "(RFC822)")
            if status != "OK" or not fetch_data:
                logger.warning("Failed to fetch mail id %s", mail_id)
                continue
            
            raw_email = fetch_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            body = _get_text_from_message(msg)

            parsed = parse_body(parse_date(msg.get("Date", "")), body)
            if parsed:
                expenses.append(parsed)

        return expenses
    finally:
        logout(imap)

# If you want quick local testing:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    since_date = "12-Nov-2025"
    next_date = "13-Nov-2025"
    retrieve_expenses(since_date, next_date)
