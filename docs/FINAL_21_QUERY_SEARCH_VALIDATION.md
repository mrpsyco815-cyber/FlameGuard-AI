# Final 21-Query Search Validation

## Status

**PARTIAL PASS ? corrections implemented and individually validated; scientific expert review remains required.**

## Execution

All 21 fixed queries from the three completed topic tests were run individually before and after the correction. Each run called local search, combined local-first/NASA fallback, and BASS-II search with limit 5. Actual outputs are in the temporary baseline/final JSON artifacts and summarized in [INDIVIDUAL_QUERY_BEFORE_AFTER_RESULTS.md](./INDIVIDUAL_QUERY_BEFORE_AFTER_RESULTS.md).

## Aggregate metrics

| Metric | Baseline | Final |
|---|---:|---:|
| Queries | 21 | 21 |
| Local result records | 96 | 96 |
| NASA records | 44 | 39 |
| BASS-II records | 11 | 11 |
| Local/NASA combined records | 140 | 135 |
| Accumulated unique sources | 114 | 109 |
| Accumulated duplicate source records | 26 | 26 |
| NASA fallback calls | 11 | 11 |
| Mean local latency | 41.09 ms | 35.17 ms |
| Mean combined latency | 1624.37 ms | 1558.03 ms |
| Mean BASS-II latency | 25.54 ms | 24.63 ms |

The aggregate source diversity and duplicate counts were unchanged. This is reported as unresolved, not as an improvement. Combined latency is live NASA-dependent and variable.

## Query-level correction outcomes

- Spacecraft-specific context is now part of query intent and can trigger fallback when local results lack environment coverage.
- Oxygen concentration/extinction queries now distinguish oxygen text from quantitative oxygen measurement context.
- Phenomena such as detection, suppression, extinction, and flame spread are explicitly exposed in explanations.
- Material mismatch penalties and existing source-level diversification remain active.
- NASA metadata, abstracts, full-text passages, and verified findings remain separate.

## Automated verification

The corrected suite ran with `./.venv/Scripts/python.exe -m unittest discover -s backend\tests -p "test_*.py"`: **77 tests passed**. `compileall` passed. Final `git diff --check` was run.

## Unresolved limitations

No expert qrels exist. Lexical/entity scoring remains deterministic rather than semantic. Some top-five results repeat a source because few independent local sources are available. Live NASA latency can be seconds and may fail or vary. No scientific threshold, extinction limit, or safety recommendation is inferred.
