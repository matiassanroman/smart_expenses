"""Main application entrypoint."""

import logging
import sys

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
    expenses = retrieve_expenses()
    if not expenses:
        logger.warning("No expenses retrieved. Exiting.")
        return

    classified = classify_expenses(expenses)
    result = append_expenses(classified)
    logger.info("Append result: %s", result)


if __name__ == "__main__":
    main()
