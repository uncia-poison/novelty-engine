"""Domain router for controlling linter intervention.

The router decides whether the linter should run in full mode, rhythm‑only
mode or be disabled entirely based on the type of the current task.  For
example, in highly sensitive domains such as medical advice or legal
reasoning you might turn off the novelty intervention and rely solely
on fact preservation.  In creative storytelling you might enable the
full pipeline.

Domain mappings are configured in ``domains.yml``.  The default
implementation here reads the YAML file and returns a simple string
indicating the mode.  You can extend this to include more granular
policies.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any


def load_domains(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Router:
    def __init__(self, config_path: str) -> None:
        self.domains = load_domains(config_path)

    def mode_for_domain(self, domain: str) -> str:
        """Return the linter mode for a given domain.

        If the domain is not in the config, return ``full`` by default.
        """
        return self.domains.get(domain, "full")
