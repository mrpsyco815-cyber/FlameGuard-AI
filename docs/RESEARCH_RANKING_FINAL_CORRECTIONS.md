# Research Ranking Engine Final Corrections

## Scope

This correction pass addressed:

1. provenance normalization from existing nested source records;
2. duplicate metric accuracy for passage-level benchmark output;
3. cross-source validation using available local datasets and live NTRS
   metadata where available.

NASA, BASS-II, and historical benchmark files were read only and were not
modified.

## Task 1 — Provenance root cause and correction

### Root cause

The local research store records provenance under nested structures:

- `record["source"]["source_id"]`
- `record["source"]["citation_url"]`
- `record["source"]["pdf_page_number"]`
- `record["classification"]["evidence_role"]`
- `record["classification"]["review_status"]`
- `record["review"]["source_review_status"]`
- `record["provenance"]`

The local result builder passed a partial flattened source object to the
ranking contract. Consequently, the contract could see the excerpt and page
when explicitly copied, but could not consistently see NASA ID, evidence type,
or review status. Retrieval date and section name were not present in the
historical local records.

### Safe correction

`backend/services/ranking_contract.py` now reads existing nested aliases
without changing source records or inventing values. The local result builder
also adds the following normalized fields additively:

- `nasa_id`
- `source_url`
- `evidence_type`
- `source_type`

The contract now correctly recovers:

- NASA/source document ID;
- source URL;
- page number;
- evidence role/modality;
- review status.

It continues to report genuinely unavailable fields as missing:

- section name is absent from the historical passage records;
- retrieval date is absent from those records.

No dates, sections, identifiers, or URLs were fabricated.

### Before/after provenance metrics

Historical benchmark output contained 121 returned rows.

| Metric | Before correction | After correction |
|---|---:|---:|
| Returned benchmark rows with missing provenance | 121 | 121 |
| Unique returned records with missing provenance | Not measured | 29 |
| Unique returned records | Not measured | 29 |
| NASA/source ID available to contract | Not consistently available | 29/29 |
| Source URL available to contract | Not consistently available | 29/29 |
| Page number available to contract | 121 row appearances | 29/29 unique records |
| Evidence type available to contract | Missing in local contract input | 29/29 |
| Review status available to contract | Missing in local contract input | 29/29 |
| Genuinely missing section/retrieval date | Not separated | 29/29 records |

The row-level count remains 121 because the same records appear in multiple
queries. The corrected unique-record view shows that normalization fixed the
available provenance fields; the remaining missing fields are genuinely absent
from the historical store.

## Task 2 — Duplicate metric correction

The previous benchmark summary counted duplicate-marked rows and summed
per-query source positions. That overstated duplicate evidence because the
same passage can appear in several benchmark queries.

`backend/tests/run_scientific_search_benchmark.py` now:

- deduplicates benchmark output by `record_id` with a conservative fallback
  identity;
- counts returned rows separately from unique returned records;
- counts unique source documents;
- counts excess duplicate records beyond the first record in each source group;
- counts unique duplicate groups;
- counts independent source groups;
- counts documents with multiple distinct passages;
- reports source distribution, provenance gaps, and unknown conditions.

### Corrected historical benchmark metrics

The unmodified 30-query fixture was executed.

| Metric | Corrected value |
|---|---:|
| Query count | 30 |
| Total returned rows | 121 |
| Unique returned records | 29 |
| Unique source documents | 4 |
| Duplicate records beyond first per source | 25 |
| Unique duplicate groups | 4 |
| Independent evidence sources | 0 |
| Documents with multiple passages | 4 |
| Unique records with missing provenance | 29 |
| Unique records with unknown conditions | 20 |
| Runtime | 526.27 ms |
| Source distribution | 29 `local_nasa_passage` records |

The four source documents are represented by multiple distinct passages.
Those passages remain separate and retain their record IDs and page
references. They are not independent scientific corroboration.

## Task 3 — Cross-source validation

Available source paths were exercised without modifying datasets or fixtures.

| Source path | Probe result | Ranking source type |
|---|---:|---|
| Local NASA research passages | 5 results | `local_nasa_passage` |
| Extracted NASA document passages | 5 results | `nasa_extracted_passage` |
| Reviewed NASA evidence | 5 results | `reviewed_evidence` |
| BASS-II records | 5 results using available PMMA filter | `bass_ii` |
| NASA NTRS metadata/abstracts | 2 live results | `nasa_ntrs` |

The BASS-II search required an available material filter because its raw
records do not contain the benchmark's generic prose terms. This is a source
schema limitation, not a dataset modification.

All paths preserved their original score fields and attached the additive
ranking contract. NTRS results remained metadata/abstract-only and
scientifically unverified.

## Task 4 — Regression and scientific integrity

Verified:

- Original score fields and source-specific meanings remain unchanged.
- Existing API fields remain available.
- Search and fallback behavior remain unchanged.
- `missing`, `unknown`, and `not_applicable` remain distinct.
- No automatic scientific verification was added.
- No confidence percentages or accuracy claims were added.
- Metadata and abstracts remain separate from extracted passages and reviewed
  findings.
- Duplicate passages are not represented as independent corroboration.
- No source record is merged or deleted by normalization.

## Testing

Focused correction and integration tests:

```text
Ran 36 tests ... OK
```

Complete backend suite:

```text
Ran 139 tests ... OK
```

Backend `compileall`: passed.

`git diff --check`: passed. Git emitted only line-ending conversion warnings
for previously modified files; no whitespace errors were reported.

## Changed files

This correction pass changed:

- `backend/services/ranking_contract.py`
- `backend/services/research_summarizer.py`
- `backend/tests/run_scientific_search_benchmark.py`
- `backend/tests/test_ranking_contract.py`
- `docs/RESEARCH_RANKING_FINAL_CORRECTIONS.md`

No NASA/BASS-II dataset, historical benchmark fixture, frontend file, or
research record was modified.

## Limitations

- Historical local passage records still lack section names and retrieval
  dates; the correction reports these as missing rather than deriving them.
- The cross-source probe is coverage validation, not a relevance benchmark.
- NTRS validation depends on live availability and covers metadata/abstracts
  only.
- No independent expert relevance labels exist, so no Precision, Recall,
  MRR, NDCG, accuracy, or scientific-validity claim is made.
- Mission-intelligence integration is validated at compatible evidence-item
  level, not as a separate benchmark dataset.
- Source-specific scores remain incomparable and are not combined.

## Preservation checks

- NASA datasets preserved.
- BASS-II datasets preserved.
- Historical benchmark fixtures preserved.
- Existing stash preserved:
  `stash@{0}: On feature/research-backend: backup local mission intelligence changes`
- No dependencies installed.
- No reset, clean, rebase, merge, commit, push, or PR operation performed.
- No frontend or Research Insights work started.
