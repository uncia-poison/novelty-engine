"""Unit tests for extract_etudes.

These tests are minimal placeholders.  You should expand them to
cover tokenisation, scoring logic and diversity selection.  They can
be run with ``pytest``.
"""

from novelty_engine.dreamspace.extract_etudes import diversify


def test_diversify_returns_first_k() -> None:
    candidates = [{"id": i} for i in range(10)]
    selected = diversify(candidates, 3)
    assert len(selected) == 3
    assert selected[0]["id"] == 0
    assert selected[1]["id"] == 1
    assert selected[2]["id"] == 2
