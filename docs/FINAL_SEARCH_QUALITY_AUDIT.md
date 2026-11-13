# Final Search Quality Audit

## Status

**A. SEARCH AND MISSION VALIDATION COMPLETED — HUMAN SCIENTIFIC REVIEW STILL
REQUIRED.**

Software implementation and audit verification are complete. Scientific
expert validation is not complete because no qualified reviewer has supplied
relevance judgments.

## 1. Human-review synchronization

Source of truth:
[scientific_search_benchmark_after.json](../backend/tests/fixtures/scientific_search_benchmark_after.json)

The review queue
[SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv](./SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv) was
regenerated directly from that output.

| Check | Result |
|---|---:|
| Benchmark queries | 30 |
| Final benchmark result records | 121 |
| Human-review rows | 121 |
| Exact `(query_id, result_rank)` pair match | PASS |
| Duplicate review pairs | 0 |
| Human labels populated | 0 |
| Empty-result queries represented as result rows | 0, correctly |
| Machine proposed labels | Present separately |

Five queries have no result rows because the final benchmark returned no
results: `F01`, `F02`, `F03`, `F04`, and `F05`. They remain represented in the
benchmark output and are not fabricated into review rows.

The CSV preserves source IDs, titles, URLs, evidence type, exact excerpt,
category, retrieval timestamp, search method, and blank human-review fields.

## 2. Latency methodology

The benchmark times only the call to `build_evidence_brief(query, limit=5)`;
fixture loading, process startup, JSON output writing, and summary printing
are outside the per-query timer.

Controlled timing used the same 30 queries in one Python process for six
sequential passes. The first pass is reported as cold-ish because it includes
the initial file read/JSON parse. Later passes are warm and use the in-process
store cache. Per-query distributions use 30 samples for the first pass and
150 samples across warm passes.

| Measurement | Mean | Median | P95 | Min | Max |
|---|---:|---:|---:|---:|---:|
| Cold-ish pass 1 | 23.88 ms | 14.69 ms | 29.97 ms | 8.34 ms | 235.43 ms |
| Warm passes 2–6 | 29.55 ms | 29.39 ms | 48.17 ms | 9.35 ms | 75.02 ms |

The reproducible benchmark runner's final single-pass summary was 24.09 ms
average. Timing varies by OS scheduling and filesystem state; the multi-pass
distribution is the more informative result.

Slowest warm queries included `C04` (75.02 ms), `C01` (59.29 ms), `C05`
(58.89 ms), `F03` (58.82 ms), and `A03` (56.15 ms). These were not associated
with extra result counts or a separate I/O path.

## 3. Bottleneck investigation and optimization

Before optimization, profiling showed that each query reparsed the
approximately 5.5 MB `research_intelligence_store.json`. In a three-call
profile, `load_store` consumed approximately 0.30 seconds of 0.37 seconds;
JSON decoding and file reads dominated. Scoring and result construction were
secondary, and source diversification was not a material cost.

The smallest safe optimization was added in
[research_summarizer.py](../backend/services/research_summarizer.py):

* Cache parsed store data by resolved path, modification timestamp, and file
  size.
* Automatically invalidate the cache when the file changes.
* Preserve the existing search and ranking behavior.
* Avoid caching stale data across file edits.

No ranking logic or evidence selection was removed. Source diversification and
contradiction rejection remain unchanged.

## 4. Final benchmark comparison

| Metric | Original baseline | Before cache optimization | Final after optimization |
|---|---:|---:|---:|
| Queries | 30 | 30 | 30 |
| Results | 126 | 121 | 121 |
| Empty queries | 4 | 5 | 5 |
| Unique-source positions | 47 | 75 | 75 |
| Repeated-source queries | 26/30 | 25/30 | 25/30 |
| Average latency | 88.06 ms | 392.55 ms | 24.09 ms runner summary |

The final result and diversity counts are unchanged by caching. The
contradictory query remains rejected, and source-aware diversification remains
in effect. The apparent latency regression was caused by repeated store
loading/parsing and is no longer present in the controlled final measurements.

## 5. Automated verification

Executed with `.\.venv\Scripts\python.exe`:

```text
python -m unittest discover -s backend\tests -p "test_*.py"
Ran 73 tests
OK

python -m compileall -q backend
PASS

git diff --check
PASS
```

Additional audit checks:

* Benchmark output contains exactly 30 queries.
* Final benchmark output contains 121 result records.
* Review CSV contains exactly 121 rows.
* Query/rank pairs match exactly.
* Duplicate review pairs: 0.
* Human labels populated: 0.

## 6. Scientific limitations and human review status

The machine-generated proposed relevance category is not a scientific
judgment. Precision@1, Precision@3, Precision@5, Recall@5, MRR, and NDCG@5
remain unavailable as human-reviewed metrics. NASA metadata and abstracts
remain non-verified evidence, and lexical/entity scoring does not establish
scientific support.

The system is research support, not a certified spacecraft fire-safety
authority. Qualified engineering review is required before any operational
decision.

## 7. Preservation

The work remained on `feature/research-backend`. The existing stash remained
present, `git diff --name-only -- data` remained empty, and no original
research datasets were changed or deleted. No Git history or stash operation
was performed.
