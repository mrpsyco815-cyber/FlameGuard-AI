# Summarization Engine Step 6 Validation

## Status

**PASS for the scoped condition-aware multi-paper synthesis requirements.**

This step adds a separate, deterministic synthesis layer over Step 4
structured findings and Step 5 evidence-linked claims. It compares only
documents with explicitly reported and matching condition values. It does not
perform scientific verification, causal inference, mission recommendations, or
automatic PDF acquisition.

No live NASA downloads were performed.

## Exact files changed

### Implementation

- [scientific_synthesis.py](../backend/services/scientific_synthesis.py)
  - Adds `synthesize_documents()`.
  - Builds strict condition signatures from:
    - Material/fuel.
    - Gravity condition.
    - Oxygen concentration.
    - Pressure.
    - Temperature.
    - Flow condition.
    - Experimental setup.
  - Separates comparable study groups from different experimental conditions.
  - Preserves source claims, excerpts, pages, sections, evidence types,
    conditions, verification status, and uncertainty.
  - Reports potential disagreements only for comparable studies with matching
    fields and units but different reported measurement values.
  - Emits explicit evidence gaps when cross-study comparison is unsupported.

### Tests

- [test_scientific_synthesis_step6.py](../backend/tests/test_scientific_synthesis_step6.py)
  - Covers comparable conditions, differing oxygen/gravity/material,
    missing conditions, unit and provenance preservation, disagreement gating,
    unsupported synthesis rejection, and invalid input.

### Documentation

- [SUMMARIZATION_STEP_6_VALIDATION.md](./SUMMARIZATION_STEP_6_VALIDATION.md)

No dataset, benchmark fixture, existing research record, search service, or
ranking implementation was modified.

## Synthesis output

`synthesize_documents()` returns:

```text
schema_version
research_topic
papers_included
comparable_study_groups
shared_observations
differences
potential_disagreements
evidence_gaps
limitations
scientific_findings_verified
```

Every shared observation and potential disagreement includes supporting
provenance with:

```text
claim_id
source_document_id
nasa_id
source_url
exact_supporting_excerpt
page_numbers
section_name
evidence_type
experimental_conditions
verification_status
uncertain
```

## Comparability rules

Two documents are placed in the same comparable group only when all supported
condition fields are explicitly present and their source values, units, and
reported wording match:

- Material/fuel.
- Gravity condition.
- Oxygen concentration.
- Pressure.
- Temperature.
- Flow condition.
- Experimental setup.

Missing conditions are never treated as equal. Different oxygen
concentrations, gravity conditions, materials, pressures, temperatures, flow
conditions, or setups produce a `different_experimental_conditions` entry
instead of a scientific contradiction.

No unit conversion or material equivalence is performed.

## Conflict handling

Potential disagreement detection requires:

1. A comparable study group.
2. The same measurement field.
3. Matching reported units.
4. At least two source documents.
5. Different reported values.

Such output is labeled `potential_disagreement`, not a verified contradiction.
Differences between non-comparable studies are never reported as conflicts.

Discussion interpretations and conclusions are not used as direct
experimental measurements. Shared observations are limited to Step 5
experimental observation/result claims.

## Insufficient evidence behavior

When no comparable study group exists, the synthesis includes:

```text
Insufficient verified evidence to support a cross-study conclusion.
```

The corresponding evidence-gap entry has no claim IDs, preventing an
unsupported cross-study conclusion from appearing evidence-linked.

## Actual test results

### Focused Step 6 and prior regressions

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_scientific_synthesis_step6 `
  backend.tests.test_claim_summarizer_step5 `
  backend.tests.test_structured_findings_step4 `
  backend.tests.test_section_extraction_step3 `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_nasa_ingestion
```

Result:

```text
Ran 47 tests in 0.328s
OK
```

### Complete backend suite

Command:

```text
.\.venv\Scripts\python.exe -m unittest discover `
  -s backend\tests -p "test_*.py"
```

Result:

```text
Ran 119 tests in 0.998s
OK
```

### Compile and diff validation

- Backend `compileall`: passed.
- `git diff --check`: passed.

## Sample behavior validated

- Identical PMMA, microgravity, oxygen, pressure, temperature, flow, and
  setup conditions formed one comparable group.
- Different oxygen concentration produced a non-comparable condition entry.
- Different gravity condition produced a non-comparable condition entry.
- Different materials produced a non-comparable condition entry.
- Missing pressure or other conditions prevented comparability.
- Original `mm/s` measurement units remained unchanged.
- NASA IDs, source URLs, excerpts, and page numbers were preserved.
- Different flame-spread measurements under otherwise matching conditions
  produced a potential disagreement.
- Different measurements under nonmatching oxygen conditions did not produce a
  potential disagreement.
- A single paper produced an explicit insufficient-evidence gap.

## Remaining limitations

- Comparability is intentionally strict and may separate studies whose
  conditions are scientifically comparable but expressed differently.
- No safe unit conversion or material ontology has been added.
- Experimental setup comparison uses exact source-linked methodological
  statements and does not infer apparatus equivalence.
- Sentence and pattern extraction remains dependent on Steps 3–5 heuristics.
- Potential disagreements are not expert-reviewed contradictions.
- The service does not synthesize causal mechanisms, thresholds, or safety
  recommendations.
- Multi-paper claims remain explicitly unverified.
- OCR, tables, figures, equations, and complex reading-order reconstruction
  remain outside scope.

## Preservation checks

- No NASA or BASS-II datasets were modified.
- No benchmark fixtures were modified.
- No existing research records were overwritten.
- No search or ranking behavior was changed.
- Automatic PDF downloads remain disabled.
- No dependencies were installed.
- Existing user changes and stash were preserved.
- No reset, clean, rebase, merge, commit, push, or stash operation occurred.

The worktree contains pre-existing changes from earlier research/search and
summarization steps. Step 6 changes are limited to the files listed above.

