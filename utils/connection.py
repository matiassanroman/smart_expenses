"""IMAP connection helpers."""

import imaplib
import logging

from config.settings import IMAP_SERVER, EMAIL_USER, EMAIL_PASS

logger = logging.getLogger(__name__)


# IMAP SSL Establish Connection
def establish_connection(server: str = IMAP_SERVER):
    """
    Establish an IMAP SSL connection and return the IMAP object.

    Returns None on failure.
    """
    try:
        imap = imaplib.IMAP4_SSL(server)
        logger.debug("Created IMAP connection to %s", server)
        return imap
    except Exception as e:
        logger.exception("Failed to establish IMAP connection: %s", e)
        return None


# Login
def login(imap: imaplib.IMAP4_SSL, user: str = EMAIL_USER, password: str = EMAIL_PASS):
    """
    Log in to IMAP server. Returns (resp_code, response) or (None, None) on error.
    """
    if not imap:
        logger.error("IMAP object is None, cannot login.")
        return None, None

    try:
        resp_code, response = imap.login(user, password)
        logger.info("Logged in to IMAP server: %s", resp_code)
        return resp_code, response
    except Exception as e:
        logger.exception("IMAP login failed: %s", e)
        return None, None


# Logout
def logout(imap):
    """
    Logout and close the IMAP connection.
    """
    if not imap:
        logger.debug("IMAP object is None in logout().")
        return None, None

    try:
        resp_code, response = imap.logout()
        logger.info("Logged out from IMAP: %s", resp_code)
        return resp_code, response
    except Exception as e:
        logger.exception("Error during IMAP logout: %s", e)
        return None, None


# If you want quick local testing:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    imap = establish_connection()
    login(imap)
    logout(imap)
