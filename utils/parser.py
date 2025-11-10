"""Email parsing utilities."""

from email.utils import parsedate_to_datetime
import logging
import re

logger = logging.getLogger(__name__)


def parse_body(date: str, body: str) -> dict:
    """
    Parse the body of an email to extract date, amount and detail.

    Returns a dict with keys: 'fecha', 'importe', 'detalle' or None if parsing fails.
    """
    result_body = None
    if not body:
        logger.debug("No body.")
        return None

    pattern = r"(Te escribimos para comunicarte el pago .*?)(?:\n|$)"
    match = re.search(pattern, body, re.IGNORECASE)

    if not match:
        logger.debug("No matching payment text found in body.")
        return None

    text = match.group(1).strip()

    match_amount = re.search(r"(\d+[.,]\d{2})\s*EUR", text)
    match_detail = re.search(r"en\s+[^.]*en\s+([^.]*)\.", text)

    result_body = {
        "fecha": date,
        "importe": match_amount.group(1) if match_amount else None,
        "detalle": match_detail.group(1) if match_detail else None,
    }

    logger.info(f"Logged out from Parser Body: {result_body}")

    return result_body


def parse_date(date: str):
    """
    Convert RFC2822 date header to YYYY-MM-DD format. Returns empty string on failure.
    """
    try:
        date_obj = parsedate_to_datetime(date).strftime("%Y-%m-%d")
        logger.info("Logged out from Parser Date: %s", date_obj)
        return date_obj
    except Exception:
        logger.exception("Failed to parse date header: %s", date)
        return ""


# If you want quick local testing:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    date = "Thu, 23 Oct 2025 11:32:24 -0600"
    body = "Te escribimos para comunicarte el pago de 1.20 EUR con tu tarjeta acabada en 3096 en CAFETERIA NAVAR."
    result_date = parse_date(date)
    parse_body(result_date, body)
