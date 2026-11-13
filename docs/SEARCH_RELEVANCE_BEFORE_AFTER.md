# Search Relevance Before/After Comparison

## Scope and reproducibility

The same 30-query fixture was executed against the local search service with a
result limit of five:

```powershell
.\.venv\Scripts\python.exe backend\tests\run_scientific_search_benchmark.py `
  --output backend\tests\fixtures\scientific_search_benchmark_after.json
```

The pre-change output is the captured baseline
`C:\Users\User\AppData\Local\Temp\flameguard_scientific_benchmark.json`.
The post-change run used the same fixture and current code. No source dataset
was modified. The comparison measures retrieval behavior, not scientific
relevance ground truth.

## Changes evaluated

1. Prefer one high-ranked passage per source before filling the requested
   result limit with additional passages.
2. Reject scoring for explicitly contradictory query conditions:
   PMMA with liquid fuel, and microgravity with normal gravity.

Multiple passages from one source remain available when the result limit
requires them; diversification changes display order/selection only.

## Aggregate results

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Queries | 30 | 30 | Same fixture |
| Returned passages | 126 | 121 | Five fewer because the contradictory query is rejected |
| Empty-result queries | 4 | 5 | The contradictory query now returns zero |
| Accumulated unique-source positions | 47 | 75 | More independent source coverage |
| Average unique sources/query | 1.57 | 2.50 | Improved diversity |
| Queries with repeated source IDs | 26/30 (86.7%) | 25/30 (83.3%) | Slightly lower source repetition |
| Average latency | 88.06 ms | 392.55 ms | Repeated store parsing caused the measured regression |
| Benchmark errors | 0 | 0 | No execution failures |

The latency comparison is not a controlled performance experiment: the
baseline was captured in an earlier run and filesystem/runtime conditions may
differ. The result is reported rather than normalized away.

## Query-level outcome

All 25 positive/category queries retained their previous result counts except
for no count reductions caused by diversification. The five negative/adversarial
queries behaved as follows:

* Marine biology: empty before and after.
* Computer networking: empty before and after.
* Random nonsense: empty before and after.
* Random numerical identifier: empty before and after.
* Contradictory PMMA/liquid-fuel/gravity query: five results before, zero
  after.

## Scientific quality status

Precision@1, Precision@3, Precision@5, Recall@5, MRR, and NDCG@5 remain
**not calculable as human-reviewed scientific metrics**. The human-review
queue leaves reviewer labels blank. Machine scores and proposed categories are
not ground truth.

## Conclusion

**Partial improvement with a documented tradeoff.** Source diversity and
contradiction rejection improved, while the displayed result total decreased
for the intentionally contradictory query. An in-process cache keyed by file
metadata was then added; the final runner reported 24.09 ms average, with
controlled warm-pass mean 29.55 ms and p95 48.17 ms. The change still requires
expert qrels review and does not establish scientific relevance validation.
