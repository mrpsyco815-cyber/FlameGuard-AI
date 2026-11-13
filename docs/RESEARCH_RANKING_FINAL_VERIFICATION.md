# Research Ranking Engine Final Verification

## Final status

**PARTIALLY READY**

The provenance implementation is functioning for all recoverable fields, and
the four benchmark source identities are consistent. The benchmark does not
contain enough metadata to establish independent experiments, so independence
is correctly reported as `unknown`. The engine should not be marked
scientifically validated or frozen as a source-independence system until
experiment-level identifiers or expert review are available.

## Task 1 — Field-level provenance investigation

The 29 unique benchmark records were traced to their original records in
`data/processed/research_intelligence_store.json`. Every record is a
`nasa_passage` record whose source data uses nested fields.

Representative original record:

```text
record_id: NASA-PASSAGE-19960008387-0000
source.source_id: 19960008387
source.citation_url: https://ntrs.nasa.gov/citations/19960008387
source.pdf_page_number: 1
classification.evidence_role: experiment
classification.review_status: requires_manual_review
review.source_review_status: requires_manual_review
provenance: {record_index: 0, audit_version: "3.4", source_text_preserved: true}
```

The excerpt is stored in `content.text` and is preserved as the normalized
result's `exact_source_excerpt`.

### Findings for all 29 unique records

| Field | Status across 29 records | Root-cause classification | Evidence |
|---|---:|---|---|
| Source/document ID | 29 present | Available under nested field | `source.source_id` |
| NASA ID | 29 present after safe normalization | Available under alternative field name | NASA NTRS `source.source_id` and citation URL |
| Source URL | 29 present | Available in nested metadata | `source.citation_url` |
| Exact supporting excerpt | 29 present | Available in content and preserved during transformation | `content.text` → `exact_source_excerpt` |
| Page number/range | 29 present as page number | Available in nested metadata | `source.pdf_page_number` |
| Section name | 29 missing | Genuinely absent from original passage records | No section field in record/source/classification |
| Evidence type | 29 present after normalization | Available under alternative nested fields | `classification.evidence_role` / `evidence_modality` |
| Retrieval date | 29 missing | Genuinely absent from original data | `provenance` has index/audit metadata only |
| Review status | 29 present after normalization | Available in nested metadata | `classification.review_status` / `review.source_review_status` |

Therefore, the statement that all 29 records have “missing provenance” is
technically true only under the aggregate rule “any provenance field is
missing.” It does **not** mean that all provenance is absent. The recoverable
identity, URL, excerpt, page, evidence, and review fields are present for all
29 records. Only section name and retrieval date are genuinely unavailable.

No values were inferred from titles or generated from benchmark query text.

## Task 2 — Four-document source identity verification

The local store and `nasa_combined_evidence.json` both contain four NASA
documents represented in the benchmark:

| NASA ID | Citation URL | Local passage records | Identity finding |
|---|---|---:|---|
| `19960008387` | `https://ntrs.nasa.gov/citations/19960008387` | 175 | One consistent URL and source ID |
| `20000024924` | `https://ntrs.nasa.gov/citations/20000024924` | 1,439 | One consistent URL and source ID |
| `20210017787` | `https://ntrs.nasa.gov/citations/20210017787` | 613 | One consistent URL and source ID |
| `20220012861` | `https://ntrs.nasa.gov/citations/20220012861` | 480 | One consistent URL and source ID |

For each document:

- all local records use the same NASA/source ID;
- all local records use exactly one citation URL;
- the URL path contains the same NASA ID;
- record IDs are passage-specific and remain distinct;
- no source identity collision was found;
- no title-only merge was used.

The records are therefore four distinct source documents. Multiple records
within each group are passages from the same document, not four separate
experiments.

## Task 3 — Independent-evidence audit

The benchmark contains passage records, not experiment-level records.
Consequently:

- repeated passages with the same NASA ID are confirmed same-document
  records;
- they are not independent corroboration;
- the four different NASA IDs are distinct papers/documents;
- the passage metadata does not establish whether the papers contain
  independent experiments, reused experiments, follow-up experiments, or
  related analyses;
- no experiment identifier or study-family identifier is available in the
  benchmark records.

The previous numeric result `independent_evidence_sources: 0` was therefore
too strong: it could be read as proof that no independent evidence exists.
The benchmark now reports:

```text
independent_evidence_sources: "unknown"
independent_evidence_source_count: 0
```

The zero is retained only as a count of **confirmed** independent source
groups. It is not a claim that independent evidence is absent.

Duplicate-source grouping remains justified at the document level because it
uses stable NASA IDs and URLs. Independence remains `unknown` at the
experiment level.

## Task 4 — Minimal corrections

The following minimal correction was made:

- Added `independence_status: "unknown"` to duplicate metadata.
- Changed the benchmark report from a definitive independent-source count to
  an explicit unknown status plus a confirmed-count field.
- Preserved the existing duplicate grouping, record IDs, source fields, score
  semantics, and API response fields.

No NASA/BASS-II dataset or benchmark fixture was modified.

The prior safe provenance normalization remains in place and was verified
against all 29 records. It reads nested source, classification, review, and
provenance fields without fabricating missing section names or dates.

## Before/after benchmark metrics

The same unmodified 30-query benchmark was used.

| Metric | Before verification | After verification |
|---|---:|---:|
| Query count | 30 | 30 |
| Returned rows | 121 | 121 |
| Unique returned records | 29 | 29 |
| Unique source documents | 4 | 4 |
| Duplicate records beyond first source passage | 25 | 25 |
| Unique duplicate groups | 4 | 4 |
| Documents with multiple passages | 4 | 4 |
| Aggregate rows with any missing provenance | 121 | 121 |
| Unique records with any missing provenance | 29 | 29 |
| Field-level recoverable provenance | Not separated | 7 of 9 fields present for all records |
| Genuinely missing fields | Not separated | Section and retrieval date only |
| Independent evidence classification | `0` | `unknown` |
| Source distribution | Local NASA passages | Local NASA passages |

The aggregate missing-provenance count did not decrease because every unique
record still lacks two genuinely absent fields. The field-level audit shows
that source identity, NASA ID, URL, excerpt, page, evidence type, and review
status are present for all records.

## Task 5 — Validation

Focused ranking and integration tests:

```text
Ran 36 tests ... OK
```

Complete backend test suite:

```text
Ran 139 tests ... OK
```

Backend `compileall`: passed.

`git diff --check`: passed. Only line-ending conversion warnings for
previously modified files were emitted; no whitespace errors were reported.

## Changed files

This verification changed:

- `backend/services/ranking_contract.py`
- `backend/tests/run_scientific_search_benchmark.py`
- `backend/tests/test_ranking_contract.py`
- `docs/RESEARCH_RANKING_FINAL_VERIFICATION.md`

No frontend files were modified.

## Limitations

- Section names are unavailable in the historical local passage records.
- Retrieval dates are unavailable in the historical local passage records.
- Experiment-level independence cannot be established from passage records.
- Distinct NASA documents do not automatically prove independent experiments.
- Cross-source ranking scores remain source-specific and uncalibrated.
- No expert relevance labels or scientific validation labels exist.

## Preservation checks

- NASA datasets preserved.
- BASS-II datasets preserved.
- Historical benchmark fixtures preserved.
- Existing research records preserved.
- Existing search and NASA fallback behavior preserved.
- Existing API fields and score semantics preserved.
- Existing stash preserved:
  `stash@{0}: On feature/research-backend: backup local mission intelligence changes`
- No dependencies installed.
- No reset, clean, rebase, merge, commit, push, or PR operation performed.
- Research Insights and frontend development were not started.
