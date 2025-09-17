"""Unit tests for the linter.

These tests exercise the basic scoring and plan generation logic.  They
are not comprehensive but demonstrate how to instantiate the linter and
feed it a simple context.
"""

from novelty_engine.linter.lint import Linter, load_clichés, load_cooldowns


def test_linter_no_intervention_when_clean() -> None:
    dictionary = {"syn": [], "rhythm": []}
    clichés = []
    cooldowns = {}
    linter = Linter(dictionary, clichés, cooldowns, threshold=1.0)
    plan = linter.inspect("hello world", [])
    assert plan.mode == "none"


def test_linter_intervenes_on_cliché() -> None:
    dictionary = {"syn": [], "rhythm": []}
    clichés = ["as a matter of fact"]
    cooldowns = {}
    linter = Linter(dictionary, clichés, cooldowns, threshold=0.0)
    plan = linter.inspect("As a matter of fact, it works.", [])
    assert plan.mode == "micro"
    assert "as a matter of fact" in plan.remove
