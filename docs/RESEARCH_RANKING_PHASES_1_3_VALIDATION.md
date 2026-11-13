# Unified Scientific Research Ranking: Phases 1–3 Validation

## Scope

This implementation adds an additive, explainable ranking contract. It does
not replace existing ranking algorithms, alter fallback thresholds, or
calibrate scores from different sources onto a common scale.

## Implemented phases

### Phase 1: shared ranking contract

`backend/services/ranking_contract.py` provides
`build_ranking_contract()` and preserves each producer's original score and
score semantics. The contract exposes:

- contract version;
- original score;
- condition compatibility;
- evidence scope;
- provenance completeness;
- missing information;
- human-readable explanations;
- the existing scientific-verification state.

The contract is attached additively under `ranking_contract` to local research
results, NASA online results, NASA extracted passages, reviewed evidence,
BASS-II results, and compatible mission-intelligence evidence.

### Phase 2: condition-aware matching

`condition_match()` compares only conditions explicitly present in the query
and source text:

- material/fuel;
- gravity;
- oxygen concentration;
- pressure;
- temperature;
- flow condition;
- experimental setup.

Each requested field is classified as `exact`, `mismatch`, or `unknown`.
The aggregate is `exact`, `partial`, `mismatch`, or `unknown`. Missing source
conditions are never treated as matches. The implementation performs no unit
conversion and does not infer equivalence between materials or experimental
setups.

### Phase 3: evidence-aware representation

Evidence scope is preserved as descriptive metadata, including metadata,
abstract, experimental methods/setup/results, discussion, conclusion,
limitations, and independently reviewed evidence where explicitly supplied.
The contract does not assign arbitrary confidence percentages and does not
mark a finding scientifically verified merely because it was reviewed.

## Files changed

New:

- `backend/services/ranking_contract.py`
- `backend/tests/test_ranking_contract.py`
- `docs/RESEARCH_RANKING_PHASES_1_3_VALIDATION.md`

Additive integrations:

- `backend/services/research_summarizer.py`
- `backend/services/nasa_online.py`
- `backend/services/nasa_passage_search.py`
- `backend/services/nasa_evidence_search.py`
- `backend/services/bass2_dataset.py`
- `backend/services/mission_intelligence.py`

No datasets, historical benchmark fixtures, or search fallback rules were
modified by this phase.

## Validation results

Focused contract tests:

```text
Ran 4 tests ... OK
```

Ranking integration regressions:

```text
Ran 22 tests ... OK
```

Complete backend test suite:

```text
Ran 135 tests ... OK
```

Backend `compileall`: passed.

`git diff --check`: passed. Git emitted only existing-style CRLF conversion
warnings for several previously modified files; no whitespace errors were
reported.

## Known limitations

- Original scores remain source-specific and are not comparable across local,
  NASA, reviewed-evidence, and BASS-II producers.
- Condition extraction is conservative and text-based. It intentionally
  reports unknown when a value or unit is not explicit.
- Pressure, temperature, flow, and setup matching is limited by the
  heterogeneous fields and prose available in each source.
- Evidence scope is descriptive metadata, not a measure of scientific truth or
  independent validation.
- Provenance completeness reports missing fields; it does not repair or
  fabricate provenance.
- No human-reviewed relevance labels or externally validated ranking weights
  exist, so no new ranking weights or scientific performance claims were
  introduced.

## Preservation checks

- Existing ranking fields and score meanings remain present.
- Existing ranking order and fallback behavior were not intentionally changed.
- NASA online results remain metadata/abstract-only and are not persisted as
  verified findings.
- No dependency installation occurred.
- No commit, push, merge, rebase, reset, clean, dataset overwrite, or stash
  operation was performed.
