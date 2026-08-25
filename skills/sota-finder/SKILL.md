---
name: sota-finder
description: >-
  Find evidence-backed state of the art results and build practical, multi-scope leaderboards for a research task or benchmark. Use when the user asks for the latest or historical SOTA, a benchmark leaderboard, cross-paper result comparison, official and open-world result discovery, or structured evidence deliverables from natural language, papers, URLs, repositories, tables, or existing result files. The skill separates comparable main results from reference results and conflicts, uses AMiner only as an optional enhancement, and produces concise chat output plus Markdown, self-contained HTML, XLSX, and evidence JSON artifacts.
license: MIT
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# SOTA Finder

Build a useful answer, not a ceremonial review pipeline. The host model makes research judgments; bundled scripts handle deterministic artifact mechanics.

## Core interpretation

- Define SOTA only inside a materially comparable scope.
- A topic may yield multiple scopes and multiple SOTA results.
- Use three user-visible result groups only: `Main Leaderboard`, `Reference Results`, and `Conflicts / Unavailable`.
- Admit a claim to the main leaderboard only when its comparison setting is sufficiently complete and at least one original, official, or author-controlled source supports it.
- Treat aggregators as discovery and cross-checking aids. Do not use an aggregator alone as sufficient main-leaderboard evidence.
- State an absolute cutoff such as `Evidence checked through August 25, 2026`.

## Inputs

The primary input is a natural-language goal such as:

- "Find the SOTA for this task."
- "Build the latest leaderboard for this benchmark."
- "Compare the results reported by recent papers."

Optional inputs include PDFs, paper or benchmark URLs, arXiv/DOI identifiers, official leaderboards, repositories, CSV/XLSX/Markdown/JSON files, pasted tables, prior leaderboards, and prior evidence records.

Prefer explicit inputs, then use open-world search to fill gaps. Disable outside search only when the user explicitly says to use only the supplied sources.

## Required workflow

### 1. Frame provisional scopes

Infer the task and likely comparison axes. Keep these core fields when applicable:

- task;
- benchmark and version;
- dataset or subtask;
- split;
- metric, variant, unit, and direction;
- evaluation protocol.

Add dynamic material axes only when they change comparability, for example training regime, external data, shot setting, tool access, ensemble, model scale, or retrieval conditions. Do not build a universal rules engine for them.

### 2. Run fast-first discovery

Read `references/research-playbook.md` for non-trivial searches.

Search broadly across:

1. official leaderboard and benchmark documentation;
2. papers and preprints;
3. author or official project repositories;
4. high-quality aggregators and result indexes.

Use a two-stage strategy:

- discover candidate scopes, leading methods, recent claims, and setting differences quickly;
- verify the leaders, recent SOTA claims, and conflicts against authoritative evidence.

When no year is requested, consider the full historical candidate pool. Prioritize discovery from the most recent two to three years, but retain an older method if it still leads a comparable scope.

### 3. Verify claims and classify results

For every result, capture the method, variant, score, source, evidence locator, setting, and comparability notes.

- `main`: comparable enough and supported by original/official/author evidence;
- `reference`: useful but incomplete, weakly evidenced, or materially non-comparable;
- `unavailable`: a relevant claim whose evidence or result could not be obtained;
- conflict records: contradictory values, settings, or source interpretations.

Explain conflicts rather than silently choosing a convenient value. Keep reference and unavailable material out of main rankings.

### 4. Decide when to stop

Do not use a fixed number of rounds. Stop when:

- material scopes have credible coverage;
- leading candidates have converged;
- newly found results no longer change the head of the scopes materially;
- unresolved gaps and conflicts are explicitly recorded.

Network or individual source failures should trigger best-effort degradation. Ask the user only when no meaningful result can be formed or a decision materially changes scope or risk.

### 5. Use AMiner only when valuable

AMiner is optional. Never require `AMINER_API_KEY` to start or finish the task.

When a token is available, AMiner may improve paper discovery, metadata, related-paper discovery, and citation expansion. Continue broad official, paper, repository, and web search even when AMiner is used.

Free or low-cost shortest-path calls may run automatically. Before an expected cumulative AMiner cost of about CNY 5, a clearly large batch, or an unbounded/uncertain paid plan, request one user confirmation. Do not split calls to evade the cumulative guardrail. Record usage, purpose, available cost information, and skipped enrichment in the research run.

### 6. Build the artifact bundle

Read `references/data-contract.md` before preparing the temporary research input. Read `references/output-contract.md` before final delivery.

The mechanical builder requires `openpyxl`:

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install -r "<skill-root>/requirements.txt"
python3 "<skill-root>/scripts/build_outputs.py" \
  --input "/path/to/research-input.json" \
  --output-root "outputs"
```

Use the actual loaded Skill directory for `<skill-root>`. Do not assume a personal absolute path. A host that exposes `${CLAUDE_PLUGIN_ROOT}` may use that variable.

The default output bundle is:

```text
outputs/<topic-slug>/
├── brief-report.md
├── full-report.html
├── leaderboards.xlsx
└── evidence.json
```

If that run directory already contains a default artifact, use `<topic-slug>-2`, `<topic-slug>-3`, and so on. Never silently overwrite a prior bundle.

The builder can check a prepared input without writing artifacts:

```bash
python3 "<skill-root>/scripts/build_outputs.py" \
  --input "/path/to/research-input.json" \
  --validate-only
```

If artifact generation fails, still provide the minimal chat result and state which files were not saved.

## Chat response contract

Keep the chat response extremely short:

1. show the main leaderboard content;
2. add only essential scope, cutoff, or exception notes;
3. provide direct links to the four generated files.

Do not paste the full research narrative into chat.

## Language and portability

Match the user's language for reports and visible labels. Keep JSON keys, IDs, schema values, and stable machine fields in English.

The Skill must remain self-contained. Do not require another Skill to be installed, do not use machine-specific absolute paths, and do not depend on a Codex-only artifact runtime. The host may use its native search/browser tools; the bundled Python script is only for local artifact mechanics.

## Non-goals

Do not create a rigid benchmark rule database, universal method alias registry, approval state machine, or fixed search-round protocol. Do not confuse weakly comparable open-world findings with the main leaderboard. Do not claim exhaustive coverage when gaps remain.
