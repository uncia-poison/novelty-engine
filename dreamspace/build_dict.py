"""Build a consolidated style dictionary from extracted etudes.

This script reads a JSONL file of etudes (produced by
``extract_etudes.py``) and organises them into separate collections
for lexical, syntactic and rhythm patterns.  It writes out JSON files
under ``dict/`` so that the linter can quickly load them at runtime.

If you wish to maintain additional metadata or compress embeddings,
modify this script accordingly.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a style dictionary from etudes JSONL")
    parser.add_argument("--input", type=str, required=True, help="Path to etudes JSONL")
    parser.add_argument("--out_dir", type=str, required=True, help="Directory to write the dictionary files")
    return parser.parse_args()


def load_etudes(path: str) -> List[Dict[str, Any]]:
    etudes = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                etudes.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return etudes


def build_dictionary(etudes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    lex, syn, rhythm = [], [], []
    for e in etudes:
        types = e.get("type", [])
        if "lexical" in types:
            lex.append(e)
        if "syntactic" in types:
            syn.append(e)
        if "rhythm" in types:
            rhythm.append(e)
    return {"lex": lex, "syn": syn, "rhythm": rhythm}


def save_dict(dictionary: Dict[str, List[Dict[str, Any]]], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for name, items in dictionary.items():
        path = Path(out_dir) / f"{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)


def main() -> None:
    args = parse_args()
    etudes = load_etudes(args.input)
    dictionary = build_dictionary(etudes)
    save_dict(dictionary, args.out_dir)


if __name__ == "__main__":
    main()
