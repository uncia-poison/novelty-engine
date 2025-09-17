"""Apply a rewrite plan to a draft response.

This module receives a draft string and a :class:`~novelty_engine.linter.Plan`
object describing what changes are allowed.  It then interacts with your
chosen generative model (or a simple rule‑based editor) to perform a
minimal edit that removes clichés, injects fresh patterns and preserves
locked facts.  After rewriting it calls fact guards to ensure numbers,
dates and named entities remain unchanged.

The default implementation here is a stub that simply returns the
original draft.  To use the full pipeline you should implement your
preferred rewriting strategy.  For example, you can prompt your model
with explicit instructions derived from the plan, or you can train a
small edit model on pairs of (draft, plan) → rewrite.
"""

from __future__ import annotations

from typing import List

from .fact_locks import extract_facts, check_facts
from ..linter.lint import Plan


def apply_plan(draft: str, plan: Plan, model) -> str:
    """Rewrite ``draft`` according to ``plan`` using ``model``.

    ``model`` should expose a callable interface such as
    ``model.generate(prompt: str) -> str``.  You are responsible for
    constructing a prompt that instructs the model to remove phrases,
    inject patterns and preserve locked facts.  After generation the
    function checks that all facts have been preserved; if not, it
    returns the original draft or triggers a regeneration with a more
    conservative plan.

    The default implementation returns the draft unchanged.
    """
    # Extract facts from the original draft
    facts = extract_facts(draft)

    # TODO: build prompt from plan and ask model to rewrite
    # For now we skip rewriting
    rewritten = draft

    # Check that facts are preserved
    if not check_facts(facts, rewritten):
        # If facts differ, fall back to original draft
        return draft
    return rewritten
