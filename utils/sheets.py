"""Google Sheets helper to append expenses."""

import logging
from typing import Iterable, List, Dict

# from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

from config.settings import SERVICE_ACCOUNT_KEY_PATH, SPREADSHEET_ID

logger = logging.getLogger(__name__)


def get_credentials():
    """
    Load service account credentials from file.
    """
    key = str(SERVICE_ACCOUNT_KEY_PATH)
    creds = service_account.Credentials.from_service_account_file(
        key, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return creds


def append_expenses(expenses: Iterable[Dict[str, object]]) -> dict:
    """
    Append expenses to the spreadsheet.

    Args:
        expenses: Iterable of dicts with keys: 'fecha', 'categoria', 'detalle', 'importe'
        spreadsheet_id: Optionally override default spreadsheet ID.

    Returns:
        The API response from append().
    """
    spreadsheet = SPREADSHEET_ID
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    values = []
    for e in expenses:
        # Ensure importe is numeric if possible
        try:
            amount = float(e.get("importe", 0) or 0)
        except (TypeError, ValueError):
            amount = 0.0

        row = [
            f"'{e.get('fecha', '')}",
            e.get("categoria", ""),
            e.get("detalle", ""),
            amount,
        ]
        values.append(row)

    body = {"values": values}
    result = (
        sheet.values()
        .append(
            spreadsheetId=spreadsheet,
            range="A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )

    updated = result.get("updates", {})
    logger.info(
        "Inserted %s rows, %s cells updated",
        updated.get("updatedRows"),
        updated.get("updatedCells"),
    )
    return result


# If you want quick local testing:
if __name__ == "__main__":
    value = [
        {
            "fecha": "2025-10-15",
            "categoria": "transporte",
            "importe": "1.35",
            "detalle": "METRO DE MALAGA",
        },
        {
            "fecha": "2025-10-15",
            "categoria": "transporte",
            "importe": "1.35",
            "detalle": "METRO DE MADRID",
        },
    ]
    append_expenses(value)

    """
    For read to sheet

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A1:A8').execute()
    values = result.get('values', [])
    print(values)
    """
