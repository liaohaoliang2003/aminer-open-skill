# `sota-finder` Evaluation Plan

## 1. Purpose

This suite evaluates whether `sota-finder` can turn an underspecified or evidence-rich research request into a practical, source-aware SOTA analysis and leaderboard. It intentionally tests research judgment, comparability, evidence integrity, discovery breadth, graceful degradation, and artifact delivery rather than checking only whether a particular current paper appears at rank 1.

The suite contains **30 cases**, grouped into six capability categories and four execution modes. The synthetic fixtures are deterministic; live-web cases are time-sensitive and must be graded against the evidence available on the recorded cutoff date.

### Non-goals

- Do not treat one frozen list of method names or scores as the permanent truth for live-web cases.
- Do not require a ceremonial approval workflow when the task can be resolved safely by model judgment.
- Do not require AMiner access for baseline success.
- Do not reward exhaustive search that adds no material scope, candidate, or evidence improvement.

## 2. Execution modes

| Mode | Purpose | Network policy | Primary grading target |
|---|---|---|---|
| `offline_fixture` | Deterministic regression tests using supplied synthetic evidence | No network access beyond the named files | Scope construction, ranking, conflict handling, evidence links, artifact correctness |
| `behavioral` | Policy and decision tests that can be inspected without relying on a changing web result | Network optional unless the prompt says otherwise | Routing, autonomy, degradation behavior, AMiner guardrails, delivery behavior |
| `live_web` | Real research tests over papers, preprints, repositories, official boards, and aggregators | Broad web discovery allowed and expected | Search breadth, cutoff handling, source quality, explicit uncertainty, practical usefulness |
| `aminer_optional` | Optional AMiner enrichment tests | AMiner may be used only when configured and cost-safe | Optional enhancement, no-token fallback, cost accounting, no secret leakage |

Recommended order: run all `offline_fixture` and `behavioral` cases first, then `live_web`, then configured `aminer_optional` cases. A failed live source must not block deterministic regression coverage.

## 3. Case matrix

| ID | Must pass | Case | Category | Mode | Difficulty | Fixture(s) |
|---:|:---:|---|---|---|---|---|
| 01 | yes | Official live leaderboard | `routing-input` | `live_web` | basic | <live / none> |
| 02 | yes | No unified benchmark | `routing-input` | `live_web` | adversarial | <live / none> |
| 03 | yes | Closed supplied sources only | `routing-input` | `offline_fixture` | intermediate | evals/fixtures/closed_source_dossier.md |
| 04 | no | Prior leaderboard plus open-world update | `routing-input` | `offline_fixture` | intermediate | evals/fixtures/prior_leaderboard.csv |
| 05 | no | Negative routing — simple metadata lookup | `routing-input` | `behavioral` | basic | <live / none> |
| 06 | yes | Split mismatch | `scope-comparability` | `offline_fixture` | basic | evals/fixtures/prior_leaderboard.csv |
| 07 | no | Benchmark version mismatch | `scope-comparability` | `offline_fixture` | intermediate | evals/fixtures/prior_leaderboard.csv |
| 08 | yes | Tool access and external data | `scope-comparability` | `offline_fixture` | adversarial | evals/fixtures/closed_source_dossier.md |
| 09 | yes | Higher/lower metric directions | `scope-comparability` | `offline_fixture` | basic | evals/fixtures/mixed_scope_results.json |
| 10 | no | Single model versus ensemble | `scope-comparability` | `behavioral` | intermediate | <live / none> |
| 11 | yes | Aggregator-only leading claim | `evidence-integrity` | `behavioral` | basic | <live / none> |
| 12 | yes | Official versus paper conflict | `evidence-integrity` | `offline_fixture` | adversarial | evals/fixtures/conflicting_sources.md |
| 13 | no | Preprint versus proceedings revision | `evidence-integrity` | `offline_fixture` | intermediate | evals/fixtures/conflicting_sources.md |
| 14 | no | Unavailable authoritative source | `evidence-integrity` | `live_web` | intermediate | <live / none> |
| 15 | yes | Evidence locator and source registry | `evidence-integrity` | `offline_fixture` | basic | evals/fixtures/mixed_scope_results.json |
| 16 | yes | Latest cutoff and historical pool | `discovery-coverage` | `live_web` | intermediate | <live / none> |
| 17 | no | Fast-first convergence | `discovery-coverage` | `live_web` | adversarial | <live / none> |
| 18 | no | Partial network failure | `discovery-coverage` | `behavioral` | intermediate | <live / none> |
| 19 | no | Multilingual source discovery | `discovery-coverage` | `live_web` | intermediate | <live / none> |
| 20 | no | Ambiguous but inferable goal | `discovery-coverage` | `behavioral` | basic | <live / none> |
| 21 | yes | No AMiner token | `robustness-aminer` | `behavioral` | basic | <live / none> |
| 22 | no | Low-cost AMiner enhancement | `robustness-aminer` | `aminer_optional` | intermediate | <live / none> |
| 23 | yes | High-cost AMiner guardrail | `robustness-aminer` | `aminer_optional` | adversarial | <live / none> |
| 24 | no | AMiner metadata versus result evidence | `robustness-aminer` | `aminer_optional` | intermediate | <live / none> |
| 25 | yes | Minimal chat and four links | `artifact-delivery` | `behavioral` | basic | <live / none> |
| 26 | no | Non-overwrite repeated run | `artifact-delivery` | `offline_fixture` | basic | evals/fixtures/mixed_scope_results.json |
| 27 | no | Multi-scope workbook | `artifact-delivery` | `offline_fixture` | intermediate | evals/fixtures/mixed_scope_results.json |
| 28 | no | Chinese visible labels, English machine keys | `artifact-delivery` | `offline_fixture` | intermediate | evals/fixtures/mixed_scope_results.json |
| 29 | no | Offline self-contained HTML | `artifact-delivery` | `offline_fixture` | basic | evals/fixtures/mixed_scope_results.json |
| 30 | yes | Cross-file claim alignment | `artifact-delivery` | `offline_fixture` | adversarial | evals/fixtures/mixed_scope_results.json |

The canonical prompts, expected behaviors, expectation lists, failure conditions, tags, and fixture paths live in [`evals.json`](./evals.json). This plan explains how to run and score them; it does not duplicate the full rubric text.

## 4. Capability categories

### `routing-input`

Checks positive and negative triggering, closed-source boundaries, prior-leaderboard updates, open-world discovery, and tolerance for natural-language inputs. A good run starts useful work without forcing the user through a long questionnaire, but does not hijack simple metadata lookups.

### `scope-comparability`

Checks whether the model separates materially different benchmark versions, splits, metrics, directions, access conditions, and method settings. Scope construction remains a model judgment: the evaluator should penalize misleading comparisons, not harmless differences in table layout or wording.

### `evidence-integrity`

Checks source authority, evidence locators, conflicts, inaccessible evidence, source registries, and cross-file identifiers. Aggregators are useful for discovery and reference pools but cannot by themselves establish a verified main SOTA claim.

### `discovery-coverage`

Checks broad discovery across official sources, papers, preprints, repositories, and aggregators; multilingual query expansion; historical candidate pools; absolute cutoff dates; fast-first convergence; and graceful handling of partial network failure.

### `robustness-aminer`

Checks that AMiner is an optional enhancement, never a prerequisite. No-token execution must remain complete. When AMiner is configured, low-cost calls may enrich discovery, while estimated cumulative cost around CNY 5, clearly large batches, or unbounded paid plans require one user confirmation.

### `artifact-delivery`

Checks the user-visible contract: minimal leaderboard-first chat output, four saved artifacts, non-overwrite behavior, multiple workbook sheets for multiple scopes, self-contained HTML, Chinese-visible reporting with stable English machine identifiers, and cross-artifact `claim_id` / `source_id` consistency.

## 5. Scoring

### 5.1 Expectation scoring

For each expectation in a case:

- `1.0`: clearly satisfied with observable evidence.
- `0.5`: partially satisfied, materially incomplete, or only implicit.
- `0.0`: absent or contradicted.

`case_score = sum(expectation_scores) / expectation_count * 100`.

This rubric supports model judgment. Evaluators should assess the substance of the outcome rather than exact prose, heading names, or search order.

### 5.2 Failure conditions and hard failures

Every listed `failure_condition` is checked independently. A normal failure condition caps that Case at 60. A hard failure sets that Case to 0 and must be recorded with evidence.

Treat the following as suite-level hard failures when applicable:

1. Fabricating a score, paper, source, quotation, or evidence locator.
2. Presenting materially incomparable results as one verified main ranking without qualification.
3. Promoting an aggregator-only claim to verified main SOTA.
4. Violating a closed-source prompt by searching beyond the supplied fixture.
5. Requiring an AMiner token to start or finish the task, or exposing/requesting secret material.
6. Silently overwriting an existing artifact bundle.
7. Claiming that required artifacts exist when they were not created.
8. Producing dangling or contradictory `claim_id` / `source_id` references across artifacts.

### 5.3 Aggregate result

Report both micro and macro results:

- **Micro score:** expectation-weighted average across all executed cases.
- **Category macro score:** average of the six category scores so the six-case artifact category does not dominate the four-case AMiner category.
- **Must-pass status:** all IDs in `must_pass_ids` must score at least 80 and contain no hard failure.
- **Coverage status:** list skipped cases and why; do not silently remove unavailable live or AMiner cases from the denominator.

Suggested release gate for a usable prototype:

- all must-pass cases pass;
- no suite-level hard failure;
- category macro score at least 80;
- every category score at least 70;
- deterministic (`offline_fixture` + `behavioral`) cases are reproducible on a second run, allowing benign wording variation.

These thresholds are defaults for regression evaluation, not immutable product policy.

## 6. Live-web drift policy

Live-web cases must record an absolute `evidence_checked_through` date, run date, model/tool configuration, and any inaccessible sources. Grade the method and evidentiary support against what was discoverable on that date.

Do not fail a later run merely because the leading method changed. Instead check whether the run:

- searched the expected source classes;
- found plausible current and historical candidates;
- separated incompatible scopes;
- supported main claims with authoritative or primary evidence;
- preserved unresolved or aggregator-only candidates as clearly marked reference results;
- stopped after additional search no longer materially changed the answer.

For comparative model evaluation, run live cases within the same time window and preserve the source registry so adjudicators can distinguish model quality from web drift.

## 7. Fixture policy

Fixtures under `evals/fixtures/` are synthetic and intentionally contain traps:

- `closed_source_dossier.md`: primary closed-book evidence plus aggregator-only and tool-assisted incompatible candidates.
- `prior_leaderboard.csv`: mixed benchmark versions, splits, and evidence quality.
- `conflicting_sources.md`: official, preprint, proceedings, and repository values that require authority/version reasoning.
- `mixed_scope_results.json`: higher-is-better and lower-is-better scopes, ties, reference-only claims, unavailable evidence, and stable IDs.

Offline runs must use only the files named by the Case. The expected result is a defensible scope-aware leaderboard and evidence package, not extraction of every number into one table.

## 8. Run record

For each evaluated Case, retain at least:

- suite version and Case ID;
- exact prompt and supplied files;
- execution mode, date, model, and enabled tools;
- network and AMiner availability;
- output text and artifact directory;
- expectation-level scores with short evidence notes;
- triggered failure conditions and adjudicator notes;
- live-web cutoff date and unavailable sources, when relevant.

A compact machine-readable record may use JSONL with one record per Case. Human adjudication is expected for research quality; scripts should validate structure, files, identifiers, and deterministic artifact behavior.

## 9. Maintenance

When modifying the Skill:

1. Keep stable regression cases unless the product contract intentionally changes.
2. Add a Case when a real failure reveals a materially new behavior, not merely another paraphrase.
3. Update `suite_version` when prompts, expectations, failure conditions, fixtures, or must-pass membership change.
4. Keep live-web grading behavior-based and date-aware.
5. Run `tests/test_eval_suite.py` before accepting changes to this directory.
