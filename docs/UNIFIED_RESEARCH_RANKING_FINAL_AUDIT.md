# Unified Research Ranking Engine Final Audit

## Audit scope

This audit covered the Phase 1–6 ranking contract, ranking integrations, API
surfaces, duplicate handling, historical benchmark fixtures, tests, compile
checks, Git state, and preservation requirements.

Inspected implementation and validation references:

- `backend/services/ranking_contract.py`
- `backend/services/research_summarizer.py`
- `backend/services/research_federation.py`
- `backend/services/nasa_online.py`
- `backend/services/nasa_passage_search.py`
- `backend/services/nasa_evidence_search.py`
- `backend/services/bass2_dataset.py`
- `backend/services/mission_intelligence.py`
- `backend/main.py`
- `backend/tests/test_ranking_contract.py`
- `backend/tests/test_research_summarizer.py`
- `backend/tests/test_research_federation.py`
- `backend/tests/test_nasa_online.py`
- `backend/tests/test_mission_intelligence.py`
- `backend/tests/test_research_remaining_work.py`
- Historical benchmark fixtures under `backend/tests/fixtures/`
- `docs/RESEARCH_RANKING_PHASES_1_3_VALIDATION.md`
- `docs/RESEARCH_RANKING_PHASES_4_6_VALIDATION.md`

## Final status

**PARTIALLY READY**

The engine is suitable for continued research-prototype use with explicit
limitations. It is not ready to claim complete cross-source provenance
normalization or scientifically validated ranking quality.

## Task 1 — Integration audit

| Integration | Contract present | Original score preserved | Source/evidence dimensions | Provenance behavior | Finding |
|---|---:|---:|---:|---:|---|
| Local NASA passages | Yes | Yes (`query_match_score`) | Yes | Additive, often incomplete | Integrated |
| NASA NTRS metadata/abstracts | Yes | Yes (`relevance_score`) | Yes | Correctly metadata/abstract scoped | Integrated |
| Extracted NASA passages | Yes | Yes (`relevance_score`) | Yes | Page and URL commonly present | Integrated |
| BASS-II records | Yes | Yes (`relevance_score`) | Yes | NASA/page/section marked not applicable | Integrated |
| Reviewed evidence | Yes | Yes (`relevance_score`) | Yes | Review state preserved | Integrated |
| Mission intelligence | Yes for compatible evidence items | Yes (`mission_relevance_score`) | Yes | Evidence-item level only | Partial |

Verified additive contract fields include:

- `contract_version`
- `original_score`
- `score_semantics`
- `source_type`
- `source_identity`
- `dimensions`
- `condition_match`
- `evidence_scope`
- `provenance`
- `duplicate_source`
- `missing_information`
- `explanations`
- `scientific_findings_verified`

### Integration inconsistencies found

1. Local NASA passage records commonly carry `source_id` but not a separate
   `nasa_id`. The contract therefore reports `source_document_id` as present
   and `nasa_id` as missing, even when the source ID is visibly a NASA
   citation identifier.
2. Local NASA passages in the historical store commonly lack normalized
   `evidence_type`, retrieval date, and review status. These remain explicitly
   missing, which is correct preservation behavior but prevents complete
   provenance.
3. Local NASA results are classified generically as `source_type: "nasa"`
   rather than a more specific local/extracted source type.
4. Mission intelligence attaches the contract to compatible evidence items;
   the surrounding mission response is not itself a normalized ranking result.
5. The federation layer correctly groups local and NTRS sources by NASA ID or
   URL, but its source counts are federation-level counts and do not expose
   the complete per-record duplicate metadata.

No existing score field was removed or repurposed.

## Task 2 — Duplicate validation

The stable-identity helper was tested against the required cases:

| Case | Observed behavior |
|---|---|
| Same NASA ID across records | Grouped as one duplicate source |
| Multiple passages from one paper | Records preserved separately; group marked non-independent |
| Same document with different URLs | NASA ID takes precedence and groups them |
| Same URL with URL formatting difference | Normalized URL groups them |
| Distinct papers with similar titles | Not grouped without a stable identifier |
| Missing identifiers | Remain ungrouped rather than guessed |
| Duplicate grouping | Annotates records without deleting or merging them |

For grouped records, `independent_evidence` is `false`. This prevents
duplicate passages from being represented as independent corroboration in the
ranking contract. The local research display also diversifies by stable source
group before filling the requested limit.

The historical benchmark produced 111 duplicate-marked result records out of
121 returned result records. This is expected for a passage-level benchmark
where multiple passages originate from the same NASA documents; it is not a
claim that 111 independent papers were found.

## Task 3 — Scientific integrity audit

Verified:

- NASA NTRS records expose metadata/abstract scope and
  `scientific_findings_verified: false`.
- Abstract evidence remains distinguishable from extracted passage evidence.
- Discussion and conclusion evidence types remain descriptive and are not
  converted into measurements by the ranking contract.
- Missing conditions are classified as `unknown`.
- BASS-II fields that do not apply are reported as `not_applicable`, not as
  missing evidence.
- Review status does not automatically set scientific verification to true.
- No confidence percentages, accuracy claims, or calibrated cross-source
  weights were introduced.
- Duplicate source groups are not treated as independent corroboration.

The contract is an evidence-availability and ranking-transparency structure;
it is not a scientific validation system.

## Task 4 — API compatibility

The existing API response surfaces remain structurally compatible in the
validated tests:

- Existing result fields remain available.
- Existing score names and meanings remain unchanged.
- `ranking_contract` and duplicate metadata are additive.
- Empty result lists remain valid JSON responses.
- Missing provenance values serialize as explicit statuses rather than causing
  exceptions.
- Existing validation and error behavior remains intact.

API regression tests in `test_research_remaining_work.py` passed, including
BASS-II filters, invalid limits, empty query rejection, and unavailable NASA
online responses.

No API contract correction was required.

## Task 5 — Historical benchmark validation

The existing 30-query scientific search benchmark was executed without
modifying its fixtures.

| Metric | Observed value |
|---|---:|
| Query count | 30 |
| Returned result count | 121 |
| Unique-source positions across queries | 75 |
| Duplicate-marked result records | 111 |
| Missing-provenance result records | 121 |
| Unknown-condition result records | 85 |
| Total runtime | 470.21 ms |
| Mean query runtime | 15.67 ms |

### Source distribution

| Source type | Result records |
|---|---:|
| `nasa` local passage records | 121 |

This benchmark exercises the local NASA passage path only. It does not
provide a balanced cross-source benchmark for NTRS metadata, BASS-II, reviewed
evidence, or mission intelligence.

The benchmark contains no independent expert relevance labels. Therefore this
audit does not report Precision, Recall, MRR, NDCG, accuracy, or scientific
quality claims.

### Benchmark interpretation

The high duplicate count reflects passage-level records from repeated source
documents. The universal missing-provenance count reflects missing normalized
fields in the historical local store, especially NASA ID, evidence type,
retrieval date, and review status. These are provenance coverage findings, not
ranking-quality metrics.

## Task 6 — Test and validation results

Focused ranking and integration tests:

```text
Ran 35 tests ... OK
```

Complete backend test suite:

```text
Ran 138 tests ... OK
```

Backend `compileall`:

```text
Passed
```

`git diff --check`:

```text
Passed
```

Git emitted line-ending conversion warnings for previously modified files but
reported no whitespace errors.

## Remaining gaps

1. Normalize historical local NASA records with explicit `nasa_id`,
   `evidence_type`, retrieval date, and review status where those values are
   genuinely available.
2. Use a more specific source type for local NASA passages without changing
   existing API fields.
3. Add a read-only cross-source benchmark harness covering NASA online,
   extracted passages, BASS-II, reviewed evidence, and mission intelligence.
4. Expose duplicate-group counts directly in federation summary metadata if
   consumers need to distinguish source count from passage count.
5. Add explicit API contract tests for every ranking endpoint if future schema
   evolution requires stronger compatibility guarantees.
6. Obtain independent expert relevance labels before making any ranking
   quality or accuracy claims.

## Changed files

The only file created by this final audit was:

- `docs/UNIFIED_RESEARCH_RANKING_FINAL_AUDIT.md`

No implementation, dataset, benchmark fixture, frontend, or API source file
was modified for this audit.

## Preservation checks

- NASA datasets were not modified.
- BASS-II datasets were not modified.
- Historical benchmark fixtures were not modified.
- Existing research records were not overwritten.
- Existing search and fallback behavior was preserved.
- Existing user changes were preserved.
- Existing stash preserved:
  `stash@{0}: On feature/research-backend: backup local mission intelligence changes`
- No dependencies were installed.
- No reset, clean, rebase, merge, commit, push, pull, or PR operation was run.
- No frontend code was modified.
- Research Insights and new Mission Intelligence work were not started.
