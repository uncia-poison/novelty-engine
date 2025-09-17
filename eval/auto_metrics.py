"""Automatic metrics for evaluating freshness and voice.

This module defines helper functions to compute diversity metrics such as
distinct-n and self-BLEU, as well as a simple interface to a trained
voice classifier.  These functions are intended for batch evaluation
scripts; they are not used by the linter itself.

Actual implementations of the classifier and the diversity metrics are
omitted here.  You should integrate your own models or use existing
libraries to compute them.
"""

from __future__ import annotations

from typing import List


def distinct_n(responses: List[str], n: int = 2) -> float:
    """Return the distinct-n ratio for a list of strings."""
    # TODO: implement
    return 0.0


def self_bleu(responses: List[str]) -> float:
    """Return the self-BLEU score (lower is more diverse)."""
    # TODO: implement
    return 0.0


def voice_score(response: str, clf) -> float:
    """Return a score between 0 and 1 indicating how well ``response`` matches
    your target voice.  ``clf`` is a placeholder for a trained
    classifier.
    """
    # TODO: implement
    return 0.0
