# Output Contract

## Chat

Return only:

1. the minimal main leaderboard content;
2. essential scope, evidence-cutoff, conflict, or gap notes;
3. direct links to the four files.

Do not paste the full report into chat.

## Output directory

Default:

```text
outputs/<topic-slug>/
```

If the target already contains any default artifact, allocate `<topic-slug>-2`, `<topic-slug>-3`, and so on. Do not overwrite silently.

## `brief-report.md`

An expanded version of the chat result:

- evidence cutoff;
- more complete scope leaderboards;
- reference results and essential exceptions;
- short descriptions of SOTA methods;
- concise conflicts and gaps.

## `full-report.html`

A self-contained offline report with no CDN dependency:

- table of contents;
- scope definitions and material axes;
- complete main/reference/unavailable tables;
- method summaries;
- source registry and evidence links;
- coverage, conflicts, and gaps;
- modest filtering, sorting, sticky headers, and collapsible sections.

## `leaderboards.xlsx`

- `Index` sheet plus one sheet per scope;
- main, reference, and unavailable rows clearly labeled;
- filters, frozen header row, practical column widths;
- stable `claim_id` and evidence-source columns;
- no macros;
- compatible with Excel/WPS through ordinary `.xlsx` features.

Do not create extra CSV files.

## `evidence.json`

A single hierarchical JSON file, not JSONL. It is claim-centered, uses a shared source registry, and stores stable scope/claim/source/conflict IDs. It also records the research run, queries or search themes, coverage, gaps, AMiner use, and conflict handling.

## Partial failure

If one artifact cannot be written, do not suppress the research answer. Return the minimal chat leaderboard and state exactly which files failed. Never fabricate a successful file link.
