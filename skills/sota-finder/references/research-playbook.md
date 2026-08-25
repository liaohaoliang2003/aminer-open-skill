# SOTA Finder Research Playbook

Use this reference for non-trivial discovery and comparison. It is guidance for model judgment, not a rigid workflow engine.

## 1. Start from the research question

Translate the request into provisional questions:

- What task or family of tasks is being compared?
- Is there an official benchmark, benchmark version, challenge, or dataset split?
- Which metrics are primary, and is higher or lower better?
- Which evaluation settings may make reported numbers materially non-comparable?
- What date must the evidence search cover through?

Do not force one leaderboard when the literature contains materially different settings.

## 2. Fast-first source discovery

Use several query families rather than one literal query:

- task + `state of the art`, `SOTA`, `leaderboard`, `benchmark`;
- benchmark/dataset + metric name;
- recent survey or benchmark paper + reported leaders;
- leading method + official repository or result table;
- challenge name + results, rules, evaluation protocol;
- known leading paper + later citations, follow-up work, or competing claims.

Prefer a broad first pass that identifies:

- likely scopes;
- official result pages;
- recent and historically strong candidates;
- metric and protocol differences;
- source conflicts and unavailable evidence.

Then verify only the claims that can affect the head of a scope, the latest claimed SOTA, or the interpretation of comparability.

## 3. Source roles

### Strong main-evidence candidates

- official benchmark or challenge leaderboard;
- benchmark documentation or evaluation server result;
- paper/preprint result table or surrounding evaluation text;
- author or official project repository containing the reported result;
- official model card or release record when it states the exact evaluation.

### Discovery and cross-check sources

- Papers with Code-style aggregators;
- survey tables;
- third-party blog posts;
- search snippets;
- citation indexes and metadata aggregators.

These sources are useful for candidate discovery and disagreement detection. They do not by themselves satisfy the main-evidence gate.

## 4. Scope formation

Retain fixed core comparison fields when available:

- task;
- benchmark/version;
- dataset/subtask;
- split;
- metric/variant/unit/direction;
- evaluation protocol.

Add only material axes. Common examples include:

- supervised, zero-shot, few-shot, or in-context evaluation;
- external training data or retrieval corpus;
- closed-book versus tool/retrieval access;
- single model versus ensemble;
- test-time augmentation or multi-pass inference;
- model-size or compute-restricted tracks;
- public test versus hidden/private test;
- official server versus locally reproduced evaluation.

Use the benchmark's own rules and the observed literature to decide whether an axis deserves a separate scope.

## 5. Claim capture

For each candidate result, capture:

- method and reported variant;
- numeric score and display form;
- paper/result title and date;
- scope and material settings;
- evidence source and precise locator, such as table/row/section/commit;
- whether the comparison record is complete;
- concise notes about caveats or normalization.

Avoid flattening distinct variants into one method name when the distinction changes the result.

## 6. Main, reference, and unavailable classification

A `main` claim should have:

- a complete enough scope assignment;
- the metric value and direction;
- an original, official, or author-controlled source;
- no unresolved material setting mismatch.

Use `reference` when the result is informative but lacks one of those conditions. Use `unavailable` when a relevant claim is known but its evidence cannot be accessed or reconstructed. Put contradictory reports in `conflicts` and record the resolution or unresolved state.

## 7. Conflict handling

Common conflicts include:

- paper table versus repository README;
- arXiv version versus later proceedings version;
- official leaderboard versus self-reported local evaluation;
- aggregate metric versus subtask metric;
- score unit or rounding differences;
- hidden changes in data, split, prompt, external data, or ensemble setting.

Prefer the source closest to the evaluation authority, but do not erase the disagreement. Keep the conflicting records and explain why one value was selected or why neither entered the main leaderboard.

## 8. Coverage and stopping

Stop when material scopes have credible source coverage, leader candidates converge, and additional discovery is unlikely to change the top results without resolving an already documented gap. Record:

- source types searched;
- query or search themes used;
- coverage limitations;
- unavailable pages or papers;
- unresolved benchmark/version ambiguity;
- the final stop reason.

Do not claim exhaustiveness merely because a search round returned few new papers.

## 9. Time handling

Always store an absolute `evidence_checked_through` date. When the user says “latest,” use the current date at execution time. Prioritize recent discovery, but compare against the historical pool so an older still-leading result is not discarded.

## 10. AMiner use

AMiner is an optional discovery/enrichment channel. Use the shortest useful API chain, preserve AMiner provenance separately from original evaluation evidence, and apply the cumulative paid-call confirmation guardrail described in `SKILL.md`.
