"""Unit tests for the rewrite module.

These tests cover the basic interface of ``apply_plan``.  A real
rewriter would need to be validated end-to-end with a model; here we
focus on fact preservation fallbacks.
"""

from novelty_engine.rewriter.rewrite import apply_plan
from novelty_engine.linter.lint import Plan


class DummyModel:
    def generate(self, prompt: str) -> str:
        # returns a fixed string regardless of prompt
        return "modified response"


def test_rewrite_falls_back_when_facts_missing() -> None:
    draft = "Paris has 2.1 million people."
    plan = Plan(mode="micro", locks={"numbers": True}, remove=[], inject=[])
    model = DummyModel()
    # DummyModel doesn't preserve facts; expect fallback to draft
    rewritten = apply_plan(draft, plan, model)
    assert rewritten == draft
