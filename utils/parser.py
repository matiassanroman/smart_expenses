"""Email parsing utilities."""

from email.utils import parsedate_to_datetime
import logging
import re

logger = logging.getLogger(__name__)


def parse_body(date: str, body: str) -> dict:
    """
    Parse the body of an email to extract date, amount and detail.
    Compatible with old and new bank message formats.
    """
    if not body:
        logger.debug("No body.")
        return None

    # Detect relevant line (old + new formats)
    pattern = r"(Te escribimos para comunicarte .*?|te confirmamos que has pagado .*?|te informamos de que .*?)(?:\n|$)"
    match = re.search(pattern, body, re.IGNORECASE)

    if not match:
        logger.debug("No matching payment text found in body.")
        return None

    text = match.group(1).strip()

    # --- IMPORTE ---
    match_amount = re.search(r"(\d+[.,]\d{2})\s*EUR", text)

    # --- DETALLE (varios formatos) ---

    match = re.search(
        r"(?:de que\s+(.+?)\s+ha realizado)"              # Nuevo formato retención: NETFLIX
        r"|(?:por parte de\s+(.+?)\s+con la tarjeta)"     # Antiguo retención: FREIDURIA PACO
        r"|(?:tarjeta(?: acabada| terminada)?\s+en\s+\d{4}\s+en\s+([^.,]+))",  # Pagos: CAFETERIA NAVAR / SUPERMERCADO
        text,
        re.IGNORECASE,
    )

    match_detail = None
    if match:
        match_detail = next((g for g in match.groups() if g), None)
        if match_detail:
            match_detail = match_detail.strip()

    result_body = {
        "fecha": date,
        "importe": match_amount.group(1) if match_amount else None,
        "detalle": match_detail
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

    body = [
        "Te escribimos para comunicarte el pago de 1.20 EUR con tu tarjeta acabada en 1234 en CAFETERIA NAVAR.",
        "Te escribimos para comunicarte que se ha efectuado una retención de 17.40 EUR por parte de FREIDURIA PACO con la tarjeta acabada en 1234.",
        "Matias, te confirmamos que has pagado 1.36 EUR con tu tarjeta terminada en 1234 en SUPERMERCADO.",
        "Matias, te informamos de que NETFLIX ha realizado una retención de 14.76 EUR en tu tarjeta terminada en 1234."
    ]
    
    result_date = parse_date(date)

    for msg in body:    
        parse_body(result_date, msg)
