# FlameGuard AI Research Ranking Engine Audit

## Audit status

**READ-ONLY AUDIT COMPLETED.**

The audit inspected the existing ranking, retrieval, federation, NASA, BASS-II,
provenance, benchmark, and test implementations. Only this report was created.
No code, datasets, benchmark fixtures, existing records, user changes, or
stashes were modified.

This report assesses software behavior and scientific-integrity safeguards. It
does not provide scientific validation, expert relevance judgments, or
spacecraft fire-safety certification.

## Repository and preservation state

- Branch: `feature/research-backend`
- Branch status: behind configured remote by 33 commits.
- Existing worktree: dirty from prior authorized research/search and
  summarization work.
- Existing stash preserved:
  `stash@{0}: On feature/research-backend: backup local mission intelligence changes`
- Existing `data` diff: none observed.
- Existing benchmark fixtures were inspected but not modified.
- No reset, clean, rebase, merge, commit, push, dependency installation, or
  stash operation was performed.

## Inspected files

### Ranking and query understanding

- [query_understanding.py](../backend/services/query_understanding.py)
  - `parse_query()`
  - `score_text()`
  - scientific stopwords, synonym concepts, material aliases, condition and
    environment detection, numerical/unit extraction, contradiction checks.
- [research_summarizer.py](../backend/services/research_summarizer.py)
  - `build_evidence_brief()`
  - `_make_result()`
  - `_diversify_results()`
  - local primary/supplemental passage loading, eligibility filtering, scoring,
    source diversification, provenance output.
- [research_federation.py](../backend/services/research_federation.py)
  - `search_research_with_fallback()`
  - local sufficiency checks, NASA fallback, source merging and deduplication.
- [nasa_online.py](../backend/services/nasa_online.py)
  - `search_nasa_online()`
  - NASA NTRS normalization, metadata-only scope, online deduplication.
- [nasa_passage_search.py](../backend/services/nasa_passage_search.py)
  - passage-level NASA ranking and page/provenance output.
- [nasa_evidence_search.py](../backend/services/nasa_evidence_search.py)
  - reviewed-evidence token-overlap search.
- [bass2_dataset.py](../backend/services/bass2_dataset.py)
  - `search_bass2_records()`
  - schema validation, supported filters, query scoring, numeric filtering.
- [mission_intelligence.py](../backend/services/mission_intelligence.py)
  - scenario-term ranking for the existing mission-intelligence API.

### Tests, fixtures, and reports

- [test_query_understanding.py](../backend/tests/test_query_understanding.py)
- [test_research_summarizer.py](../backend/tests/test_research_summarizer.py)
- [test_research_federation.py](../backend/tests/test_research_federation.py)
- [test_nasa_online.py](../backend/tests/test_nasa_online.py)
- [test_research_benchmark.py](../backend/tests/test_research_benchmark.py)
- [test_research_benchmark_expanded.py](../backend/tests/test_research_benchmark_expanded.py)
- [run_scientific_search_benchmark.py](../backend/tests/run_scientific_search_benchmark.py)
- [scientific_search_benchmark.json](../backend/tests/fixtures/scientific_search_benchmark.json)
- [scientific_search_benchmark_after.json](../backend/tests/fixtures/scientific_search_benchmark_after.json)
- [FINAL_SEARCH_QUALITY_AUDIT.md](./FINAL_SEARCH_QUALITY_AUDIT.md)
- [SEARCH_TOPIC_RANKING.md](./SEARCH_TOPIC_RANKING.md)
- [SCIENTIFIC_SEARCH_QUALITY_REPORT.md](./SCIENTIFIC_SEARCH_QUALITY_REPORT.md)
- [FINAL_21_QUERY_SEARCH_VALIDATION.md](./FINAL_21_QUERY_SEARCH_VALIDATION.md)
- [SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv](./SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv)

## Capability summary

| Capability | Status | Assessment |
|---|---|---|
| Query normalization | **PASS** | Case/whitespace/punctuation normalization, stemming, units, numbers, and scientific tokens are handled deterministically. |
| Scientific stopwords | **PASS** | Generic stopwords are removed; the system rejects queries containing only stopwords. |
| Scientific synonyms | **PARTIAL** | Explainable aliases exist, but the vocabulary is narrow and some synonym groups are broad enough to create semantic false positives. |
| Query entity extraction | **PARTIAL** | Materials, concepts, phenomena, environments, units, numbers, and selected conditions are extracted; pressure, temperature, flow, setup, and uncertainty are not comprehensively represented in the ranking query model. |
| Relevance scoring | **PARTIAL** | Explainable weighted lexical/entity scoring exists, but it is not semantic, calibrated, or expert-validated. |
| Experimental-condition matching | **PARTIAL** | Material and environment mismatch penalties exist; condition matches are mostly additive and missing/contradictory condition handling is incomplete. |
| Evidence-strength classification | **PARTIAL** | Evidence roles and modalities filter eligible local records, but review quality and evidence scope are not fully incorporated into rank. |
| Source quality ranking | **MISSING** | Source quality/provenance is returned, but there is no principled source-quality score or ranking policy. |
| Provenance preservation | **PASS** | Local and NASA results preserve source IDs, URLs, excerpts, pages, evidence scope, review status, and verification flags where available. |
| Duplicate-source handling | **PARTIAL** | Exact record and NASA-ID deduplication plus source diversification exist; duplicate penalties and canonical identity handling are not universal. |
| Ranking explanations | **PASS** | Score components and human-readable matching reasons are returned for primary ranking paths. |
| Local research integration | **PASS** | Primary and supplemental NASA passage collections are searched with role filtering and provenance. |
| NASA NTRS integration | **PARTIAL** | NASA fallback and online ranking work, but results are metadata/abstract only and are not directly comparable to local passage scores. |
| BASS-II integration | **PARTIAL** | BASS-II supports schema-aware filtering and ranking, but remains a separate search surface and has different scoring/provenance semantics. |
| Fallback decision logic | **PASS** | Local-first sufficiency checks use passage count, source count, relevance threshold, concepts, materials, environments, conditions, and quantitative measurement intent. |
| Benchmark coverage | **PARTIAL** | Reproducible synthetic benchmarks exist, but human labels and real scientific relevance metrics are absent. |
| Scientific validity | **MISSING** | No ranking metric establishes scientific correctness or operational safety applicability. |

## 1. Existing implementation

### Query parsing

`parse_query()` normalizes text, removes scientific stopwords, stems plural
forms, extracts scientific concepts, material aliases, units, numbers,
conditions, phenomena, environments, and contradiction flags.

Examples of modeled concepts include:

- Microgravity/reduced gravity.
- Flame spread/propagation.
- Oxygen concentration.
- PMMA/polyethylene aliases.
- Flame extinction.
- Fire detection/suppression/hazard.

The parser returns a typed `ScientificQuery` object rather than an opaque
string, allowing ranking explanations to expose intermediate decisions.

### Local passage scoring

`score_text()` calculates:

```text
token overlap:                 0.45 weight
concept match:                 0.25
material match:                0.15
numeric match:                 0.10
condition match:               0.05
environment match:             0.10
phenomenon match:              0.10
quantitative oxygen context:   0.10
```

The weighted total is capped at `1.0`. Material, environment, and missing
quantitative oxygen context can multiply the score downward. Contradictory
queries return a score of `0.0`.

The score is explicitly described by the implementation as lexical overlap,
not scientific quality.

### Local evidence selection

`build_evidence_brief()`:

1. Loads primary research-intelligence records.
2. Loads supplemental NASA passages when present.
3. Keeps only configured eligible evidence roles.
4. Scores matching passage text.
5. Sorts by score, explanation count, source, page, and record ID.
6. Diversifies by source before repeating a source.
7. Returns exact excerpts and provenance.

Records classified as background or unrelated record types are excluded from
the local evidence brief.

### NASA online ranking

`search_nasa_online()` calls the NASA NTRS citation search endpoint, scores the
title plus abstract using the same query scorer, removes duplicate NASA IDs,
and returns metadata/abstract results.

NASA online results explicitly retain:

```text
evidence_type = bibliographic_metadata_and_abstract
full_text_retrieved = false
scientific_findings_verified = false
review_status = not_scientifically_reviewed
```

### NASA passage ranking

`nasa_passage_search.py` applies the same scorer to extracted page passages,
preserves PDF page numbers, and provides snippets, classifications, review
status, and matching explanations.

### BASS-II ranking

`search_bass2_records()` validates the actual 17-column schema, applies
supported PI/material/oxygen/numeric filters, scores the concatenated record
fields, and sorts by relevance score followed by matched-term count.

The supported numeric fields are explicitly enumerated from the current
dataset schema. Unsupported numeric fields are rejected rather than silently
ignored.

### Federation and fallback

`search_research_with_fallback()` probes local results using a threshold-aware
limit and triggers NASA NTRS fallback when local evidence is insufficient by:

- passage count;
- distinct source count;
- minimum relevance score;
- required material coverage;
- required condition coverage;
- required environment coverage;
- quantitative measurement coverage; or
- missing scientific concepts.

Local and online sources are merged by NASA ID or canonical URL. Online
metadata is marked separately from local extracted passages.

## 2. Current scoring methodology

The ranking engine is primarily a deterministic lexical/entity ranker.

### Strengths

- Fully local and reproducible.
- No external LLM or embedding dependency.
- Visible score components.
- Human-readable match reasons.
- Scientific stopword handling.
- Material mismatch penalties.
- Environment mismatch penalties.
- Quantitative oxygen intent distinction.
- Contradictory-query rejection.
- Source-aware diversification.
- Stable tie-breakers.

### Weaknesses

- Token overlap remains the dominant signal.
- Scores are not calibrated against expert labels.
- No probability or confidence interpretation is justified.
- No passage proximity or section-weighting is used in the core scorer.
- A term can match in a context that does not establish the requested
  experimental relationship.
- `concept_matches`, `phenomenon_matches`, and `condition_matches` are mostly
  binary bonuses rather than condition-complete compatibility checks.
- A missing condition generally does not receive the same penalty as an
  explicit mismatch.
- The same scorer is reused across local passages, NASA abstracts, and
  concatenated BASS-II records despite their different evidence scopes.
- BASS-II and reviewed-evidence search use separate simpler scoring logic.

## 3. Evidence-strength classification

### Existing behavior

Local passage retrieval filters by configured evidence roles such as:

- Experimental quantitative result.
- Experimental observation.
- Experimental comparative result.
- Simulation result.
- Interpretation.
- Scientific limitation.

Results preserve evidence modality, role, review status, classification version,
source review status, and scientific verification flags.

### Assessment: PARTIAL

The role filter prevents some background content from entering the candidate
brief, but ranking does not consistently reward:

- extracted full text over metadata;
- experimental results over interpretations;
- reviewed evidence over pending review;
- exact page-linked evidence over abstract text;
- complete conditions over incomplete conditions;
- source identity quality;
- independent replication.

Unverified experimental-looking passages can therefore rank above or beside
reviewed evidence based primarily on lexical match.

This is acceptable for candidate retrieval but not for scientific evidence
strength estimation.

## 4. Source quality and provenance

### Assessment: PROVENANCE PASS; SOURCE-QUALITY RANKING MISSING

The implementation has strong provenance behavior:

- NASA IDs.
- Source IDs.
- Citation URLs.
- PDF page numbers.
- Exact source excerpts.
- Record origin.
- Evidence role and modality.
- Review status.
- Scientific verification flags.
- NASA metadata-only evidence scope.

The federation layer also merges local and online sources without inserting
online discoveries into the persistent store.

However, provenance is primarily returned as metadata. It is not a calibrated
ranking dimension. There is no source-quality policy that formally ranks:

- reviewed evidence over unreviewed evidence;
- extracted full text over abstract-only metadata;
- primary experiment over interpretation;
- complete provenance over incomplete provenance;
- independent sources over repeated passages from one document.

## 5. Experimental-condition matching

### Assessment: PARTIAL

Implemented:

- Material aliases and mismatch penalty.
- Environment detection and mismatch penalty.
- Numeric and unit extraction.
- Oxygen quantitative-measurement intent.
- Contradictory query rejection for selected combinations.
- Federation fallback checks for required materials, conditions, environments,
  and quantitative measurement coverage.

Missing or weak:

- No unified condition object is used by the core ranking engine.
- Pressure, temperature, flow, setup, and gravity are not comprehensively
  modeled in `ScientificQuery`.
- Explicit condition mismatch is not uniformly penalized.
- Missing conditions are not consistently separated from matching conditions.
- A passage can receive additive condition credit without demonstrating that
  all requested conditions apply to the same experiment.
- BASS-II condition filters are schema-specific and not mapped to NASA/local
  condition fields.
- Unit equivalence is not normalized.
- Material equivalence is intentionally narrow and not ontology-backed.

The later Step 6/7 synthesis and mission-brief services apply stricter
condition comparison than the search ranker. This creates a semantic gap:
retrieval may rank a candidate highly even though synthesis correctly treats it
as non-comparable.

## 6. Duplicate-source handling

### Assessment: PARTIAL

Implemented:

- NASA online deduplication by NASA ID, URL, or fallback record key.
- Federation merging by NASA ID or canonical citation URL.
- Local duplicate record-ID suppression.
- Local source diversification before repeated passages.
- Benchmark reporting of repeated-source queries and unique-source positions.

Limitations:

- `_diversify_results()` is a display diversification strategy, not a score
  penalty.
- Multiple passages from one source can still occupy the remaining result
  slots.
- Canonical URL normalization is limited.
- BASS-II search does not apply the same source diversification approach.
- Reviewed-evidence search does not expose a common duplicate policy.
- Duplicate document identity and duplicate experimental result identity are not
  the same concept, but the engine does not model that distinction explicitly.

## 7. Ranking explanations and transparency

### Assessment: PASS for explainability

Primary ranking paths expose:

- raw score;
- matched terms;
- concept matches;
- material matches;
- numeric matches;
- condition matches;
- phenomenon matches;
- environment matches;
- quantitative measurement matches;
- measurement intent;
- human-readable matching reasons.

The API and reports explicitly warn that lexical scores are not scientific
quality scores.

Remaining transparency limitations:

- Weight rationale is not empirically calibrated.
- There is no explanation of why a result outranked another result beyond the
  component values.
- Evidence-strength and source-quality effects are absent from the score.
- Different search surfaces expose different score schemas.

## 8. Integration assessment

| Source | Integration | Ranking behavior | Audit result |
|---|---|---|---|
| Local NASA passage store | Direct | Scientific lexical/entity score, eligible-role filter | **PASS/PARTIAL** |
| Supplemental NASA passages | Direct | Same local scorer, origin retained | **PASS/PARTIAL** |
| NASA NTRS online | Fallback and direct endpoint | Same scorer on title + abstract; metadata-only | **PARTIAL** |
| Extracted NASA page passages | Direct endpoint | Same scorer plus page/classification output | **PARTIAL** |
| Reviewed NASA evidence | Separate endpoint | Basic token overlap fraction | **PARTIAL** |
| BASS-II | Separate endpoint | Same query scorer over concatenated fields plus filters | **PARTIAL** |
| Mission intelligence | Separate scenario-term ranker | Mission-term overlap | **PARTIAL** |
| Step 6/7 synthesis and briefs | Downstream service use | Strict condition comparison after retrieval | **PARTIAL integration** |

The central missing integration is a shared ranking contract across all source
types. Local passage scoring, NASA abstract scoring, reviewed-evidence scoring,
BASS-II scoring, and mission-term scoring produce values with different
semantics. Their scores must not be compared as if they were calibrated on one
scale.

## 9. Existing tests and benchmark results

### Automated test coverage

The existing backend suite was executed with:

```text
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test_*.py"
```

Result:

```text
Ran 131 tests in 1.103s
OK
```

Backend compilation also passed:

```text
.\.venv\Scripts\python.exe -m compileall -q backend
PASS
```

### What tests cover well

- Stopword-only query rejection.
- Scientific aliases and material matching.
- Material mismatch penalty.
- Contradiction rejection.
- Quantitative oxygen context.
- Environment mismatch explanation.
- Local evidence role filtering.
- Simulation/experiment separation.
- Exact excerpt and citation preservation.
- Source diversification.
- NASA metadata normalization.
- NASA duplicate removal.
- NASA HTTP failure handling.
- Local sufficiency and NASA fallback.
- NASA/local deduplication by NASA ID.
- Metadata-only online evidence labeling.
- BASS-II schema and supported numeric filters.
- Synthetic ranking benchmark reproducibility.

### Benchmark limitations

The expanded benchmark uses synthetic candidate cases and asserts:

- top-1 hit count;
- fixed top-five relevant count;
- recall over known synthetic candidates.

The benchmark is useful for regression detection, but it does not establish
scientific ranking quality because:

- labels are synthetic and repository-authored;
- there is no independent expert annotation;
- no real-paper graded relevance set is available;
- no calibrated human-reviewed Precision@K, Recall@K, MRR, or NDCG is
  established;
- the benchmark tests `score_text()` directly rather than every federated
  source surface.

Historical reports record 21-query and 30-query search validation, but those
reports explicitly identify machine-proposed relevance and the absence of
independent human labels.

## 10. Scientific-integrity risks

1. **Lexical match can be mistaken for scientific relevance.** A passage may
   contain all query terms without reporting the requested experiment.
2. **Metadata/abstract ranking can appear comparable to full-text ranking.**
   The evidence scope is preserved, but the common score field can encourage
   misuse.
3. **Condition incompleteness can be under-penalized.** Missing pressure,
   temperature, gravity, flow, or setup should not be read as a match.
4. **Evidence role is not evidence verification.** Experimental-looking
   classifications remain heuristic unless independently reviewed.
5. **Repeated source passages can inflate apparent support.** Diversification
   reduces display concentration but does not measure independent evidence.
6. **BASS-II values and NASA passage scores are not directly comparable.**
7. **Source quality is not a ranking dimension.** A low-quality or
   unreviewed source can rank highly if lexical overlap is strong.
8. **Benchmark success is not scientific validation.** Synthetic labels and
   deterministic tests establish software reproducibility only.
9. **Mission applicability is downstream of retrieval.** A high search score
   does not establish condition equivalence for a mission brief.

## 11. Recommended implementation sequence

Only the next step is recommended; implementation was not performed in this
audit.

### Next implementation step: establish a shared, condition-aware ranking contract

Scope:

1. Define a typed ranking result schema shared by local passages, NASA online
   records, extracted NASA passages, reviewed evidence, and BASS-II results.
2. Separate:
   - lexical relevance;
   - condition compatibility;
   - evidence scope/strength;
   - provenance completeness;
   - source diversity.
3. Keep the existing raw score and explanations backward compatible while
   adding explicit sub-scores and an applicability status:
   - exact;
   - partial;
   - different;
   - unknown.
4. Prevent scores from different source surfaces from being interpreted as
   directly calibrated values.
5. Add tests for missing, contradictory, and cross-source condition fields.
6. Add a human-review benchmark format before changing ranking weights.

Acceptance criteria for that next step should include:

- no search/ranking regression in the current 131-test suite;
- unchanged provenance and evidence-scope fields;
- explicit separation of metadata-only and extracted-full-text evidence;
- no fabricated condition values;
- duplicate-source handling visible in output;
- deterministic explanations for each sub-score;
- no claim of scientific validity without independent labels.

Do not tune weights or claim improved ranking quality until an independent
human-reviewed relevance set exists.

## Final conclusion

The Research Ranking Engine is **implemented and operational as a deterministic
candidate retrieval ranker**, with good explainability, provenance retention,
local-first federation, and regression coverage.

It is **PARTIAL** as a scientific information-retrieval ranking system because
condition compatibility, evidence strength, source quality, duplicate
independence, and cross-source score semantics are not unified.

It is **not scientifically validated** and must not be used to make certified
spacecraft fire-safety or operational decisions.

