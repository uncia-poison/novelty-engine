"""Runtime linter for conversational outputs.

This module exposes functions to track recent utterances and compute a
"soapiness" score indicating how formulaic a candidate response might be.
It combines multiple heuristics (n‑gram repetition, KL divergence of the
token distribution, gesture repetition and cliché detection) into a single
metric.  When the score exceeds a configurable threshold the linter
selects one or more relevant style etudes from the dictionary and
returns a plan describing the required edits.

The linter does not perform any rewriting itself.  It simply builds a
structured plan that can be passed to a rewriter module together with
the original draft.  See ``novelty_engine.rewriter.rewrite`` for an
implementation of the plan application.
"""

from __future__ import annotations

import json
import math
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Plan:
    """A description of how to rewrite a draft response.

    When ``mode`` is ``"micro"`` the rewriter should perform a minimal
    edit using the instructions in ``remove`` and ``inject``.  Locks
    indicate which facts must remain untouched.  When ``mode`` is
    ``"none"`` no edits are required.
    """

    mode: str
    locks: Dict[str, bool] = field(default_factory=dict)
    remove: List[str] = field(default_factory=list)
    inject: List[Dict[str, Any]] = field(default_factory=list)
    max_edit_ratio: float = 0.25
    style_constraints: Dict[str, Any] = field(default_factory=lambda: {"voice_weight": 0.9, "temperature_cap": 0.8})


class SoapinessMeter:
    """Maintain state over a sliding window of utterances and compute scores."""

    def __init__(self, window_size: int = 12) -> None:
        self.window_size = window_size
        self.window: deque[str] = deque(maxlen=window_size)
        self.ngram_counter: Counter[str] = Counter()

    def update(self, utterance: str) -> None:
        """Add a new utterance to the buffer and update counters."""
        self.window.append(utterance)
        tokens = utterance.split()
        for n in range(1, 4):
            for i in range(len(tokens) - n + 1):
                ngram = tuple(tokens[i:i + n])
                self.ngram_counter[ngram] += 1

    def repetition_score(self) -> float:
        """Compute a simple repetition score based on n‑gram counts."""
        total = sum(self.ngram_counter.values())
        if total == 0:
            return 0.0
        max_count = max(self.ngram_counter.values())
        return max_count / total

    def kl_divergence(self) -> float:
        """Compute a toy KL divergence between the current token distribution
        and a uniform distribution.  This is a stand‑in for a more
        sophisticated measure.  It returns 0 when the distribution is
        uniform and grows as it becomes peaked.
        """
        counts = Counter()
        for utter in self.window:
            counts.update(utter.split())
        total = sum(counts.values())
        if total == 0:
            return 0.0
        uniform = 1.0 / len(counts)
        kl = 0.0
        for c in counts.values():
            p = c / total
            kl += p * math.log(p / uniform)
        return kl

    def gesture_repetition(self) -> float:
        """Placeholder for gesture repetition.  You should analyse syntactic
        patterns across the window and return a fraction indicating how
        frequently the same gesture repeats.  This stub always returns 0.
        """
        return 0.0

    def cliché_hits(self, draft: str, clichés: List[str]) -> int:
        """Count how many cliché phrases appear in the draft."""
        lower = draft.lower()
        return sum(1 for c in clichés if c in lower)


class Linter:
    """High‑level API for computing soapiness and building plans."""

    def __init__(self, dictionary: Dict[str, List[Dict[str, Any]]], clichés: List[str], cooldowns: Dict[str, int], threshold: float = 0.5) -> None:
        self.dictionary = dictionary
        self.clichés = clichés
        self.cooldowns = cooldowns
        self.threshold = threshold
        self.meter = SoapinessMeter()
        self.pattern_history: Dict[str, int] = {}

    def inspect(self, draft: str, context: List[str]) -> Plan:
        """Inspect a draft response and decide whether to edit it.

        ``context`` should be a list of previous utterances (most recent
        last).  The draft itself will be appended to the meter for
        computing repetition metrics.  The returned plan may have
        ``mode == "none"`` if no intervention is needed.
        """
        # update the window with context and draft
        for utter in context + [draft]:
            self.meter.update(utter)

        rep = self.meter.repetition_score()
        kl = self.meter.kl_divergence()
        gest = self.meter.gesture_repetition()
        cliché_count = self.meter.cliché_hits(draft, self.clichés)

        soapiness = 0.4 * rep + 0.25 * kl + 0.2 * gest + 0.15 * (1 if cliché_count > 0 else 0)

        # decide whether to intervene
        if soapiness < self.threshold:
            return Plan(mode="none")

        # pick patterns (placeholder logic)
        inject = []
        # try one syntactic and one rhythm pattern if available
        syn_pool = self.dictionary.get("syn", [])
        rhythm_pool = self.dictionary.get("rhythm", [])
        if syn_pool:
            inject.append({"type": "syntactic", "pattern": syn_pool[0].get("pattern", {})})
        if rhythm_pool:
            inject.append({"type": "rhythm", "pattern": rhythm_pool[0].get("pattern", {})})

        # locks: freeze numbers and named entities (placeholder booleans)
        locks = {"numbers": True, "named_entities": True, "quotes": True}

        # remove cliché phrases present in draft
        remove = [c for c in self.clichés if c in draft.lower()]

        return Plan(mode="micro", locks=locks, remove=remove, inject=inject, max_edit_ratio=0.25)


def load_clichés(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_cooldowns(path: str) -> Dict[str, int]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
