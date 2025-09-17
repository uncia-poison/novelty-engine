# Novelty Engine v0.1

Novelty Engine is an experimental toolkit for refreshing the responses of large language models. It detects stale phrasing and over-used patterns and gently nudges rewrites without destroying the original facts or narrative voice.

## Overview

The project is split into two stages:

* Offline extraction: we mine a corpus of conversations to collect **style etudes**, tiny pieces of form such as rhythm patterns or unusual syntactic turns. These are stored in a JSONL database alongside embeddings and metadata.

* Online linting and rewriting: during inference we monitor the last few turns of a session to estimate “soapiness” – how repetitive or formulaic the current answer is. If it drifts into sameness we look up suitable etudes and build a *rewrite plan* under a set of locks. The actual rewriting can be performed by your own LLM or by a simple text-editing model.

This repository does not depend on any proprietary LLM and can be used with online APIs, local models, or as a source of data for optional fine‑tuning. You can integrate the linter and plan builder with your favourite chat model, or run the offline extractor to curate your own style library.

## Key Concepts

### Style etudes

Style etudes are small patterns of form extracted from your own data. They describe syntactic shapes, rhythm signatures or unusual collocations. They do not contain complete sentences. At runtime these etudes serve as hints to push a rewrite in a fresh direction.

### Linter with metric gating

The linter sits in your inference loop and maintains a sliding window of the most recent utterances. It computes metrics like n‑gram repetition, token distribution divergence, gesture repetition and cliché hits. These metrics are combined into a single soapiness score. If it exceeds a threshold the linter selects one or more relevant etudes (respecting cool-downs and semantic similarity) and produces a plan.

### Rewrite plan under locks

Instead of blindly rewriting, we produce a structured plan that tells the next component what to do. A plan includes locks (facts that must not change), remove (specific clichés or tautologies to delete), inject (one or more etude patterns to use as a formal guide) and a max edit ratio.

## Repository layout

See the accompanying archive (novelty-engine.tar.gz) for the full project structure, including the `dreamspace`, `linter`, `rewriter`, `policy`, `eval`, `scoring`, and `tests` directories. The offline extractor, linter and rewriter scripts can be run independently.

## Usage

1. Extract etudes: run the extractor on your raw dialogue JSONL.
2. Load the style dictionary and configure the linter with your own cliché list and cool-downs.
3. Call the linter on each draft response; if it returns a plan, apply it with your rewriter.

You can also use the extracted etudes and rewrite pairs as training data for preference models or lightweight fine-tuning.

## License

This project is released under the MIT License.
