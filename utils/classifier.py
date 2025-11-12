"""Classifier utilities for mapping expense details to categories."""

import json
import logging
from typing import Dict, Iterable, List

from config.constants import CATEGORIES_PATH

logger = logging.getLogger(__name__)

Expense = Dict[str, str]
ClassifiedExpense = Dict[str, object]


def load_categories() -> Dict[str, List[str]]:
    """
    Load categories mapping from JSON file.

    Args:
        path: Path to categories.json.

    Returns:
        Mapping of category_name -> list of keywords.
    """
    file_path = CATEGORIES_PATH
    with file_path.open("r", encoding="utf-8") as fh:
        categories = json.load(fh)
    # Normalize keywords to lower-case
    return {cat: [kw.lower() for kw in kws] for cat, kws in categories.items()}


def classify_expenses(expenses: Iterable[Expense]) -> List[ClassifiedExpense]:
    """
    Classify a list/iterable of expense dicts.

    Args:
        expenses: Iterable of dicts with keys: 'fecha', 'importe', 'detalle'.

    Returns:
        List of classified expense dicts with keys: 'fecha', 'importe', 'detalle', 'categoria'.
    """
    categories = load_categories()
    classified: List[ClassifiedExpense] = []

    for exp in expenses:
        detail = str(exp.get("detalle", "")).lower()
        matched_category = "otros"

        for category, keywords in categories.items():
            if any(keyword in detail for keyword in keywords):
                matched_category = category
                break

        classified.append(
            {
                "fecha": exp.get("fecha", ""),
                "importe": exp.get("importe", ""),
                "detalle": exp.get("detalle", ""),
                "categoria": matched_category,
            }
        )
        logger.debug(
            "Classified '%s' as '%s'", exp.get("detalle", ""), matched_category
        )

    return classified


# If you want quick local testing:
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sample = [
        {"fecha": "2025-10-15", "importe": "1.35", "detalle": "METRO DE MALAGA"},
        {"fecha": "2025-10-15", "importe": "1.40", "detalle": "EMPRESA MALAGUE"},
        {"fecha": "2025-10-16", "importe": "4.00", "detalle": "FARMACIA CAMINO"},
    ]
    classify_expenses(sample)
