# Research Input and Evidence Contract

The host model prepares one temporary research-input JSON file. `scripts/build_outputs.py` normalizes it, assigns stable IDs, validates mechanical invariants, ranks main claims, and writes the final `evidence.json` plus the three rendered artifacts.

## Top-level input

```json
{
  "research_run": {},
  "coverage": {},
  "scopes": [],
  "sources": [],
  "claims": [],
  "conflicts": []
}
```

## `research_run`

Required fields:

- `topic`: human-readable research topic;
- `query`: original user goal or concise normalized goal;
- `evidence_checked_through`: absolute ISO date (`YYYY-MM-DD`);
- `language`: `en`, `zh`, or a locale beginning with one of them;
- `aminer.used`: boolean.

Useful optional fields include `topic_slug`, `generated_at`, `search_notes`, and AMiner purpose/cost/skipped-reason fields. When supplied, `topic_slug` should be short ASCII lowercase hyphen-case; otherwise the builder derives one and uses `sota-leaderboard` when the topic has no ASCII words.

## `scopes[]`

Each scope needs a local `key`, `name`, `task`, and `metric`:

```json
{
  "key": "benchmark-standard-test-top1",
  "name": "Benchmark standard test",
  "task": "classification",
  "benchmark": "Benchmark X",
  "benchmark_version": "1.0",
  "dataset_or_subtask": "test",
  "split": "test",
  "metric": {
    "name": "accuracy",
    "variant": "top-1",
    "unit": "%",
    "direction": "higher"
  },
  "evaluation_protocol": "official server",
  "material_axes": [
    {"name": "external_data", "value": "not allowed"}
  ]
}
```

`metric.direction` must be `higher` or `lower`.

## `sources[]`

Each source needs a local `key`, `type`, `title`, `authority`, `accessed_date`, and `available` flag. `authority` should be one of:

- `official`;
- `primary`;
- `author`;
- `secondary`;
- `aggregator`.

Useful fields include `url`, `authors`, `published_date`, `version`, and `notes`.

## `claims[]`

Each claim needs:

- local `key`;
- `scope_key`;
- `section`: `main`, `reference`, or `unavailable`;
- `method`;
- `score_numeric` for main claims;
- `score_display` (generated from the numeric score when omitted);
- `evidence_source_keys`;
- `comparability_complete`;
- optional `variant`, `paper_title`, `year`, `setting`, `evidence_locators`, `method_summary`, and `notes`.

Example:

```json
{
  "key": "method-a-standard",
  "scope_key": "benchmark-standard-test-top1",
  "section": "main",
  "method": "Method A",
  "variant": "single model",
  "score_numeric": 91.2,
  "score_display": "91.2",
  "evidence_source_keys": ["method-a-paper"],
  "comparability_complete": true,
  "evidence_locators": [
    {"source_key": "method-a-paper", "location": "Table 2, row Method A"}
  ]
}
```

The builder rejects a main claim without complete comparability, a numeric score, or at least one `official`, `primary`, or `author` source. This is a check of the model's declared classification, not an attempt to judge the research automatically.

## `conflicts[]`

A conflict needs a local `key`, `scope_key`, `summary`, and `status` (`resolved`, `unresolved`, or `unavailable`). It may reference `claim_keys` and `source_keys`, and should include `resolution` when known.

## Stable IDs

Local keys should be concise English lowercase hyphen-case identifiers within the temporary input. The builder converts them to stable machine IDs:

- `scope-...`;
- `src-...`;
- `clm-...`;
- `conflict-...`;
- `run-...`.

IDs use normalized keys and deterministic collision suffixes rather than random or cryptographic identifiers. Final reports and workbook rows link back through `claim_id`.

## Final evidence JSON

The final file conforms to `schemas/evidence.schema.json` and contains:

- normalized `research_run`;
- ranked and linked scopes;
- claim-centered result records;
- a shared source registry;
- conflicts;
- coverage and gaps;
- validation warnings, when present.

Machine keys and enum values remain English even when visible reports are Chinese.
