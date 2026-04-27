"""Main application entrypoint."""

import logging
import sys

from datetime import date, timedelta

from utils.classifier import classify_expenses
from utils.retrieve_emails import retrieve_expenses
from utils.sheets import append_expenses

LOG_LEVEL = logging.DEBUG


def configure_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    configure_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting expense ingestion pipeline...")
    since_date = (date.today() - timedelta(days=1)).strftime("%d-%b-%Y")
    next_date = (date.today()).strftime("%d-%b-%Y")
    
    #since_date = "24-Apr-2026"
    #next_date = "25-Apr-2026"

    expenses = retrieve_expenses(since_date, next_date)
    
    if not expenses:
        logger.warning("No expenses retrieved.")
        return
    
    classified = classify_expenses(expenses)
    result = append_expenses(classified)
    logger.info("Append result: %s", result)


if __name__ == "__main__":
    main()
