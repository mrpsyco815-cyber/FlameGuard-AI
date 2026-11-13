# Unified Scientific Research Ranking: Phases 4–6 Validation

## Scope

Phases 4–6 extend the existing ranking contract additively. Existing source
scores, ranking algorithms, API fields, local-first fallback behavior, and
research records remain unchanged.

## Phase 4: provenance quality

`backend/services/ranking_contract.py` now reports provenance for:

- source/document ID;
- NASA ID;
- source URL;
- exact supporting excerpt;
- page number or page range;
- section name;
- evidence type;
- retrieval date/timestamp;
- review or verification status.

Each field has an explicit status: `present`, `missing`, or
`not_applicable`. Missing values are not filled from guesses. Metadata-only
NASA results mark page and section information as not applicable where
appropriate. BASS-II records mark NASA ID, page, and section fields as not
applicable. Original source fields remain untouched.

The contract retains the earlier `present_fields`, `missing_fields`, and
`complete` compatibility fields and adds detailed `fields`,
`not_applicable_fields`, and explanations.

## Phase 5: duplicate source intelligence

Stable source identity is derived only from:

1. NASA ID;
2. source/document ID;
3. document ID;
4. normalized source URL.

Titles are never used as duplicate keys. `annotate_duplicate_sources()`
preserves every record and adds:

- duplicate group key;
- group size;
- occurrence number;
- duplicate status;
- independent-evidence indicator;
- explanation for the grouping decision.

Separate passages from one NASA paper remain separate records and retain their
page/snippet provenance. Local research, NASA extracted passages, NASA online
results, and reviewed evidence expose duplicate metadata. Local result
diversification uses stable source groups, preventing repeated passages from
crowding out distinct sources without deleting relevant evidence.

## Phase 6: cross-source ranking contract

The additive `ranking_contract` is integrated with:

- local NASA passages;
- NASA NTRS metadata and abstracts;
- extracted NASA passages;
- reviewed evidence;
- BASS-II records;
- mission-intelligence evidence.

The contract now consistently exposes:

- source type;
- original score;
- source-specific score semantics;
- evidence scope;
- condition compatibility;
- provenance details;
- stable source identity;
- duplicate-source metadata;
- ranking explanations;
- scientific verification state.

Scores from different producers are not arithmetically combined or presented
as calibrated cross-source values. Metadata and abstracts remain distinct from
full-text findings, and reviewed evidence does not automatically become
scientifically verified.

## Changed files

New:

- `docs/RESEARCH_RANKING_PHASES_4_6_VALIDATION.md`

Updated:

- `backend/services/ranking_contract.py`
- `backend/services/research_summarizer.py`
- `backend/services/nasa_online.py`
- `backend/services/nasa_passage_search.py`
- `backend/services/nasa_evidence_search.py`
- `backend/services/bass2_dataset.py`
- `backend/services/mission_intelligence.py`
- `backend/tests/test_ranking_contract.py`

## Tests and validation

Focused Phase 4–6 contract tests:

```text
Ran 7 tests ... OK
```

Ranking integration regressions:

```text
Ran 28 tests ... OK
```

Complete backend suite after the final duplicate-output wiring:

```text
Ran 138 tests ... OK
```

Backend `compileall`: passed.

`git diff --check`: passed. Git reported only line-ending conversion
warnings for previously modified files; no whitespace errors were reported.

The final duplicate-output wiring is additive and was included in the final
focused and complete validation runs.

## Limitations

- Duplicate grouping is intentionally conservative and requires a stable
  identifier or normalized URL.
- Records without stable identifiers are explicitly ungrouped rather than
  merged by title or text similarity.
- A duplicate group indicates shared source identity, not that passages have
  identical content.
- Source-specific scores remain incomparable across producers.
- Provenance completeness describes availability and applicability; it does not
  establish scientific validity.
- Evidence scope is descriptive and does not create confidence percentages or
  independent verification.
- Cross-source result federation still preserves producer-specific records and
  does not claim that duplicate passages are independent corroboration.

## Preservation checks

- NASA and BASS-II datasets were not modified.
- Historical benchmark fixtures were not modified.
- Existing score fields, response structures, ranking order, and fallback
  behavior were preserved.
- No research records were overwritten.
- No dependencies were installed.
- Existing stash was preserved.
- No reset, clean, rebase, merge, commit, push, or pull operation was run.
