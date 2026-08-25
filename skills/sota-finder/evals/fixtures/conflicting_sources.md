# Synthetic Conflicting Result Sources

## Official leaderboard snapshot

- Benchmark: ConflictBench v2
- Split: hidden test
- Metric: macro F1, higher is better
- Method K: 84.6
- Locator: official leaderboard row Method K

## ArXiv preprint v1

- Benchmark label: ConflictBench
- Split: development
- Metric: macro F1
- Method K: 85.1
- Locator: Table 4, "development results"

## Proceedings paper

- Benchmark: ConflictBench v2.1 (corrected labels)
- Split: hidden test
- Metric: macro F1
- Method K: 84.4
- Locator: Table 5, corrected test set

## Author repository

- Benchmark: ConflictBench v2
- Split: hidden test
- Method K: 84.6
- Locator: README commit `synthetic-k84`

## Expected interpretation

The values are not a single flat contradiction: 85.1 is a development score, 84.6 belongs to v2 hidden test, and 84.4 belongs to corrected v2.1. Preserve all records, create separate scopes for materially different version/split combinations, and explain the apparent conflict.
