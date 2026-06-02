"""English-only translation module.

Loads ``data/public/lang/en.json`` once at import. ``t(key)`` returns the
English string for a key, falling back to the key itself if missing.
"""

import json
from typing import Optional

from tostl.config import PUBLIC_DIR

LOCALE = "en_US"
LANGUAGE = "en"
COUNTRY = "US"

_LANG_FILE = PUBLIC_DIR / "lang" / "en.json"

try:
    TRANSLATIONS = json.loads(_LANG_FILE.read_text(encoding="utf-8"))
except (OSError, ValueError):
    TRANSLATIONS = {}


def t(text: str) -> str:
    return TRANSLATIONS.get(text, text)


def store_tesla_locale(_locale_value: Optional[str]) -> None:
    return None


class use_default_language:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False
