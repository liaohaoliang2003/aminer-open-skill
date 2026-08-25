# Synthetic Closed-Source Evaluation Dossier

The evaluator must tell SOTA Finder to use only this file and not search externally.

## Source S1 — Primary paper

- Title: Alpha for SyntheticQA
- Source role: primary paper
- Benchmark: SyntheticQA v1
- Dataset/subtask: full test
- Split: test
- Metric: Exact Match, higher is better
- Method: Alpha
- Score: 72.1
- Setting: single model; no external data; no tools
- Evidence locator: Table 2, row Alpha, column Test EM

## Source S2 — Aggregator record

- Title: SyntheticQA result index
- Source role: aggregator
- Benchmark: SyntheticQA v1
- Split: test
- Metric: Exact Match
- Method: Beta
- Score: 73.0
- Setting: not reported
- Original paper/result URL: unavailable
- Evidence locator: leaderboard row Beta

## Source S3 — Author repository

- Title: Gamma official repository
- Source role: author-controlled repository
- Benchmark: SyntheticQA v1
- Split: test
- Metric: Exact Match
- Method: Gamma
- Score: 74.2
- Setting: retrieval tool enabled; external corpus used
- Evidence locator: README section "Results"

## Expected interpretation

Alpha is eligible for a standard closed-book main scope. Beta is reference-only because it has aggregator-only evidence and incomplete setting. Gamma must not be mixed into Alpha's standard closed-book scope because tool access and external data materially change comparability; it may form a separate scope or remain a clearly labeled reference result.
