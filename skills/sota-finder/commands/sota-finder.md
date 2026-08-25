---
description: Find evidence-backed SOTA and build a multi-scope leaderboard
argument-hint: "[research goal, task, or benchmark] [output: <dir>] [sources-only: yes|no] [aminer: auto|off|on]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
---

# `/sota-finder`

Use the `sota-finder` Skill for `$ARGUMENTS`.

1. Parse the research goal and optional output/source/AMiner preferences.
2. Prefer explicit files and URLs, then perform open-world discovery unless `sources-only: yes` or equivalent was explicitly requested.
3. Follow the fast-first, multi-scope, evidence-gated workflow in `SKILL.md`.
4. Keep AMiner optional and apply the cumulative paid-call guardrail.
5. Prepare the temporary research input described in `references/data-contract.md` and run `scripts/build_outputs.py`.
6. Return only the minimal leaderboard, essential notes, and direct links to `brief-report.md`, `full-report.html`, `leaderboards.xlsx`, and `evidence.json`.

Do not require another Skill or silently overwrite an earlier output bundle.
