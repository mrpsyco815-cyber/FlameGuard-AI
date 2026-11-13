# FlameGuard AI — Scientific Search Quality Report

## Assessment status

**B. SEARCH QUALITY BASELINE ESTABLISHED — EXPERT REVIEW PENDING**

The benchmark was executed against the current local research database and
live NASA NTRS connector. It establishes an operational baseline, not
scientific ground truth. No domain expert reviewed the query/result pairs, so
all relevance assessments in this report are `provisional_unreviewed`.

## Benchmark methodology

Fixture: [scientific_search_benchmark.json](../backend/tests/fixtures/scientific_search_benchmark.json)

The fixture contains 30 queries in six categories:

| Category | Queries |
|---|---:|
| Microgravity combustion | 5 |
| Spacecraft fire safety | 5 |
| Oxygen and combustion | 5 |
| Materials and fuel | 5 |
| BASS-II research | 5 |
| Negative/adversarial | 5 |

Each query was executed with the existing local `build_evidence_brief`
implementation and a result limit of five. The benchmark fixture contains no
fabricated result records and no expert relevance labels. Actual returned
records were captured separately during execution.

Automatic search scores, provisional matching explanations, and any future
expert labels are separate concepts:

* `query_match_score` and `relevance_components`: automatic deterministic
  scorer output.
* `provisional_unreviewed`: this evaluation status; not a scientific label.
* Expert labels: **not available**.

## Actual execution results

The 30-query local benchmark produced:

* Queries executed: 30
* Errors: 0
* Total returned local passages: 126
* Empty local queries: 4
* Average local search time: 88.06 ms

### Representative local records

#### `flame spread in microgravity`

* Record ID: `NASA-PASSAGE-19960008387-0000`
* NASA source ID: `19960008387`
* Title: **Solid surface combustion experiment flame spread in a quiescent,
  microgravity environment implications of spread rate and flame structure**
* Automatic score: `0.75`
* Matched concepts: microgravity, flame spread
* Evidence type: extracted source text
* Review status: requires manual review
* Scientifically verified: false
* URL: <https://ntrs.nasa.gov/citations/19960008387>
* Excerpt begins: “Solid Surface Combustion Experiment — Flame Spread in a
  Quiescent, Microgravity Environment”

#### `material flammability in spacecraft`

* Record ID: local NASA passage from source `20000024924`
* Title: **Experimental Verification of Material Flammability in Space**
* Top automatic score: `0.30`
* Source diversity in top five: one NASA source
* Evidence type: extracted source text
* Review status: requires manual review
* Scientifically verified: false
* URL: <https://ntrs.nasa.gov/citations/20000024924>

#### `oxygen concentration effects on flame propagation`

* Top source: NASA `19960008387`
* Top automatic score: `0.48`
* Matched concepts: flame spread, oxygen concentration
* Evidence type: extracted source text
* Review status: requires manual review
* Scientifically verified: false
* Excerpt begins: “The experimental flame spread rates ... over the thin
  cellulosic fuel ... at three different ambient pressures”

#### `PMMA flame spread`

* Top source: NASA `20000024924`
* Top automatic score: `0.85`
* Evidence type: extracted source text
* Review status: requires manual review
* Scientifically verified: false
* URL: <https://ntrs.nasa.gov/citations/20000024924>

#### `BASS-II material flammability`

* Top source: NASA `20000024924`
* Top automatic score: `0.225`
* Evidence type: extracted source text
* Review status: requires manual review
* Scientifically verified: false
* The result is a NASA passage match; it is not a structured BASS-II record.

## Category retrieval results

| Category | Cases | Returned passages | Empty cases | Average unique sources/query |
|---|---:|---:|---:|---:|
| Microgravity combustion | 5 | 25 | 0 | 2.40 |
| Spacecraft fire safety | 5 | 22 | 0 | 1.60 |
| Oxygen and combustion | 5 | 25 | 0 | 2.00 |
| Materials and fuel | 5 | 25 | 0 | 1.60 |
| BASS-II research | 5 | 24 | 0 | 1.60 |
| Negative/adversarial | 5 | 5 | 4 | 0.20 |

## Relevance labels and metrics

### Expert labels

Not measured. No query-result pair was reviewed by an independent NASA,
combustion, fire-safety, or information-retrieval domain expert.

Therefore the following scientific metrics are **NOT MEASURED** against valid
ground truth:

* Precision@1
* Precision@3
* Precision@5
* Recall@5
* MRR
* NDCG@5
* Material mismatch rate
* Experimental-condition mismatch rate
* Irrelevant top-result rate

Empty-query false-positive rate and fallback-trigger accuracy were also
**NOT MEASURED** because this fixture contains no empty-query cases and no
independent expected fallback decisions.

Publishing these as validated scientific metrics would be misleading.

### Provisional operational diagnostics

These are retrieval diagnostics, not relevance metrics:

* Local result availability: 26/30 queries returned at least one result.
* Negative/adversarial empty-result rate: 4/5.
* Negative/adversarial non-empty rate: 1/5. The non-empty query was the
  intentionally contradictory `PMMA liquid fuel normal gravity microgravity
  contradiction`, whose top result came from NASA `20000024924` with score
  `0.5786`; this is a false-positive risk requiring expert review.
* Queries with repeated source IDs in the top five: 26/30.
* Query-level repeated-source rate: 86.7% (26/30).
* Total top-five passage slots: 126.
* Sum of unique source counts across queries: 47.
* Mean unique source count per query: 1.57.

The high repeated-source count confirms that passage count must not be used as
independent evidence count.

### Metric definitions for future reviewed qrels

After expert qrels exist, the benchmark will calculate:

* Precision@K = relevant retrieved results in the first K positions divided by
  K; missing positions count as non-relevant.
* Recall@5 = relevant retrieved results in the first five divided by the total
  known relevant documents for the query.
* MRR = reciprocal rank of the first relevant result, averaged across queries.
* NDCG@5 = graded discounted cumulative gain normalized by the ideal ranking,
  using labels 0–3.
* Binary relevance for precision/recall: labels 2 and 3.
* Graded relevance for NDCG: labels 0, 1, 2, and 3.

## Source diversity

The benchmark counted passages and unique source IDs separately.

Observed behavior:

* 126 passages were returned.
* Only 47 unique-source positions were accumulated across queries.
* 26 of 30 queries repeated at least one source ID within the top five.
* Several top results were different pages/passages from the same NASA report.

This is useful for context retrieval but must not be described as 126
independent research sources.

## Adversarial scientific testing

The following queries were executed against the local scorer and live NASA
connector:

* `PMMA flame spread in microgravity`
* `liquid fuel combustion in reduced gravity`
* `oxygen concentration and flame extinction`
* `fire suppression using water mist in microgravity`
* `polyethylene insulation flammability in spacecraft`
* `high oxygen concentration and solid material ignition`
* `marine biology`
* `networking protocols`
* `qwertyzz flameguard 918273645`
* `PMMA liquid fuel normal gravity microgravity contradiction`

Observed findings:

* NASA live search returned real catalogue records for the combustion and
  fire-safety queries.
* `marine biology`, networking, and random nonsense produced no local
  benchmark results.
* The contradictory PMMA/liquid-fuel/gravity query did produce local matches,
  showing that incompatible-condition rejection is incomplete.
* Random exact tokens can receive a lexical score when a candidate contains
  the same token, even though no scientific concept is present.
* NASA results consistently exposed metadata/abstract scope and
  `scientific_findings_verified: false`.

Example live NASA result:

* Query: `PMMA flame spread in microgravity`
* NASA ID: `20200000557`
* Title: **Buoyancy Effects on Concurrent Flame Spread Over Thick PMMA**
* Automatic score: `0.9`
* URL: <https://ntrs.nasa.gov/citations/20200000557>
* Abstract begins: “The flammability of combustible materials in a spacecraft
  is important for fire safety applications...”
* Evidence type: bibliographic metadata and abstract
* Scientific verification: false

## Explainability assessment

The current result objects expose:

* Matched query terms
* Scientific concept matches
* Material matches
* Numeric matches
* Condition matches
* Matching reasons
* Source ID and title
* Page number where available
* Citation URL
* Evidence type
* Review status
* Scientific verification state

This is sufficient to explain what the deterministic scorer matched. It is
not sufficient to prove that a passage supports a scientific conclusion.

## Limitations

1. No independent expert-reviewed qrels exist.
2. Scientific precision, recall, MRR, and NDCG are therefore unavailable.
3. The current benchmark uses local passages; live NASA retrieval was tested
   for adversarial examples but was not used as expert-labelled ground truth.
4. Source diversity is low in many top-five result sets.
5. Contradictory conditions can still produce matches.
6. Lexical scores do not establish semantic or scientific relevance.
7. NASA catalogue metadata and abstracts are not verified findings.

## Overall assessment

**PARTIAL PASS — operational baseline executed successfully.**

The benchmark is reproducible and exposed meaningful quality risks,
especially source concentration, contradictory-condition matches, and the lack
of independent relevance labels. The system is ready for expert qrels review,
not for a claim of scientifically validated search quality.

## Post-baseline implementation rerun

After the source-aware display diversification and explicit contradiction
rejection changes, the same fixture produced 121 passages, 5 empty queries,
75 accumulated unique-source positions, 25/30 queries with repeated source
IDs, and 392.55 ms average latency in the reproducible rerun. The recorded
baseline was 126 passages, 4 empty queries, 47 unique-source positions,
26/30 repeated-source queries, and 88.06 ms average latency. This is a mixed
operational result: source diversity improved and the contradictory query was
rejected, but the displayed result total decreased and observed latency was
higher before the subsequent metadata-keyed store cache optimization. The
final runner reported 24.09 ms average, with controlled warm-pass mean 29.55 ms
and p95 48.17 ms. Human relevance metrics remain unavailable.

## Test execution evidence

Validation completed after restoring the environment's existing test
dependencies (`pymupdf` and `httpx2`):

```text
python -m unittest discover -s backend/tests -p "test*.py"
Ran 60 tests in 0.637s
OK

python -m compileall -q backend
PASS

python -m json.tool backend/tests/fixtures/scientific_search_benchmark.json
PASS

git diff --check
PASS
```

The test run validates the implementation and regression suite; it does not
convert provisional benchmark observations into expert-reviewed relevance
judgments.
