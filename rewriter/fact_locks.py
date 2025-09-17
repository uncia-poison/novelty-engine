"""Extract and check immutable facts in a draft string.

Facts include numbers, dates and named entities.  When rewriting we
freeze these so that they cannot be altered.  The current
implementation uses naive heuristics: it extracts sequences of digits
and very simple capitalised tokens as stand‑ins for numbers and
entities.  You should replace these with proper parsers and NER
systems suitable for your language and domain.
"""

from __future__ import annotations

import re
from typing import List, Tuple, Dict

Number = Tuple[str, int]
Entity = Tuple[str, int]


def extract_facts(text: str) -> Dict[str, List[str]]:
    """Return a dict containing all numbers and candidate named entities."""
    numbers = re.findall(r"\b\d+[\d,.]*\b", text)
    # naive entity extraction: any capitalised word outside sentence start
    entities = [w for w in re.findall(r"\b[A-Z][a-zA-Z]+\b", text) if w.lower() not in {"i", "the"}]
    return {"numbers": numbers, "entities": entities}


def check_facts(original: Dict[str, List[str]], rewritten: str) -> bool:
    """Verify that all facts from ``original`` appear verbatim in ``rewritten``."""
    for fact in original.get("numbers", []) + original.get("entities", []):
        if fact not in rewritten:
            return False
    return True
