"""Email retrieval and extraction of expenses."""

import email
import logging
from typing import List
import re

from config.settings import SEARCH_FROM, SEARCH_SUBJECT

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
        imap.select("inbox")
        # Using exact FROM and SUBJECT filters
        # criteria = f'(FROM "{from_filter}" SUBJECT "{subject_filter} SINCE "{target_date}")'
        criteria = f'FROM "{from_filter}" SUBJECT "{subject_filter}" SINCE {since_date} BEFORE {next_date}'
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


"""
def retrieve_emails():
  imap = establish_connection()
  login(imap)
  imap.select("inbox")
  status, mail_ids = imap.search(None, f'(FROM "{SEARCH_FROM}" SUBJECT "{SEARCH_SUBJECT}")')
  
  #print("Mail IDs: {}\n".format(mail_ids[0].decode().split()))
  gastos = []
  for mail_id in mail_ids[0].split():
    #tupla
    #('OK', [(b'1702 (RFC822 {3523}', b'MIME-Version: 1.0\r\nFrom: ...'), b')'])
    status, data = imap.fetch(mail_id, "(RFC822)")
    #if status != "OK":
    #    print(f"Error al obtener el email con ID {mail_id}")
    #    continue

    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    body = ""
    if msg.is_multipart():
      for part in msg.walk():
        if part.get_content_type() == "text/plain":
          body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
    
    valid_body = parser_body(parser_date(msg['Date']),body)
    if valid_body:
      #print(f"From: {msg['From']}")
      #print(f"Subject: {msg['Subject']}")
      #print(f"Date: {parser_date(msg['Date'])}")
      #print(valid_body)
      gastos.append(valid_body)
      #print("-" * 40)
    #break
  #print(gastos)
  logout(imap)
  return gastos
"""

# If you want quick local testing:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    since_date = "12-Nov-2025"
    next_date = "13-Nov-2025"
    retrieve_expenses(since_date, next_date)
