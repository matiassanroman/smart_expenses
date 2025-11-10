import os
from pathlib import Path
from typing import Final

ROOT_DIR = Path(__file__).resolve().parent.parent

# Paths
CATEGORIES_PATH: Final[Path] = Path(
    os.getenv("CATEGORIES_PATH", ROOT_DIR / "config" / "categories.json")
)
