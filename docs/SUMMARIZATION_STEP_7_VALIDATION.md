# Summarization Engine Step 7 Validation

## Status

**PASS for the scoped condition-aware mission-specific research brief
requirements.**

This step adds a separate research-support brief generator over Step 4
structured findings, Step 5 claims, and optional Step 6 synthesis output. It
does not generate operational recommendations, certify spacecraft safety, or
enable automatic PDF acquisition.

No live NASA downloads were performed.

## Exact files changed

### Implementation

- [mission_research_brief.py](../backend/services/mission_research_brief.py)
  - Adds `build_mission_research_brief()`.
  - Accepts explicit mission objective, question, material, gravity, oxygen,
    pressure, temperature, flow, and setup fields.
  - Preserves missing mission parameters as `unknown`.
  - Classifies each paper as:
    - `exact_match`
    - `partial_match`
    - `different_conditions`
    - `unknown_conditions`
  - Preserves claim and source provenance.
  - Includes optional Step 6 synthesis groups without altering them.
  - Explicitly avoids generating a recommendation field.

### Tests

- [test_mission_research_brief_step7.py](../backend/tests/test_mission_research_brief_step7.py)
  - Covers exact, partial, different, and unknown condition handling;
    missing research conditions; traceability; evidence gaps; recommendation
    safeguards; and invalid inputs.

### Documentation

- [SUMMARIZATION_STEP_7_VALIDATION.md](./SUMMARIZATION_STEP_7_VALIDATION.md)

No dataset, benchmark fixture, existing research record, search service, or
ranking implementation was modified.

## Brief structure

`build_mission_research_brief()` returns:

```text
schema_version
brief_type
research_question
research_objective
supplied_mission_conditions
relevant_nasa_research
comparable_studies
partially_comparable_studies
important_differences
unknown_condition_studies
scientific_observations
interpretations_and_conclusions
evidence_gaps
limitations_and_uncertainty
further_research_needed
source_references
synthesis_groups_used
scientific_findings_verified
```

Each included claim preserves:

```text
claim_id
source_document_id
nasa_id
source_url
claim_text
exact_supporting_excerpt
page_numbers
section_name
evidence_type
verification_status
uncertain
```

## Condition matching

- `exact_match`: every supported mission condition is explicitly supplied and
  matches the study's reported condition.
- `partial_match`: at least one supplied condition matches, while another
  mission condition is missing from the mission context or source.
- `different_conditions`: at least one supplied condition differs from the
  study condition.
- `unknown_conditions`: no sufficient condition comparison can be made.

Condition fields include material/fuel, gravity, oxygen concentration,
pressure, temperature, flow, and experimental setup. Values remain in their
reported wording and units. No unit conversion, material equivalence, or
condition inference is performed.

Different gravity, oxygen, material, or other experimental conditions are
reported as important differences and are never presented as direct validation
of a mission condition.

## Scientific safeguards

The brief:

- Does not include a `recommendation` field.
- Keeps observations separate from interpretations and conclusions.
- Keeps all extracted claims `not_scientifically_verified`.
- Does not generate thresholds, causal explanations, assurances, or
  operational instructions.
- Identifies itself as a research-support brief, not a certified spacecraft
  safety assessment.
- Emits:

```text
Insufficient verified evidence to support a mission-specific recommendation.
```

when no exact condition match exists.

## Actual test results

### Focused Step 7 and prior regressions

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_mission_research_brief_step7 `
  backend.tests.test_scientific_synthesis_step6 `
  backend.tests.test_claim_summarizer_step5 `
  backend.tests.test_structured_findings_step4 `
  backend.tests.test_section_extraction_step3 `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_nasa_ingestion
```

Result:

```text
Ran 54 tests in 0.370s
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
Ran 126 tests in 1.015s
OK
```

### Compile and diff validation

- Backend `compileall`: passed.
- `git diff --check`: passed.

## Sample behavior validated

- Exact PMMA/microgravity/oxygen/pressure/temperature/flow/setup matches are
  placed in `comparable_studies`.
- Missing mission parameters remain explicit unknown fields and produce a
  partial or unknown classification rather than an assumed match.
- Missing source conditions do not become differences or exact matches.
- Different gravity and oxygen conditions are placed in
  `important_differences`.
- Claim IDs, NASA IDs, URLs, excerpts, and page numbers are preserved.
- Unsupported mission-specific recommendations are rejected through the
  explicit evidence-gap statement.
- No recommendation is generated even when source claims are present.

## Remaining limitations

- Matching is intentionally strict and does not normalize units or material
  names.
- Experimental setup comparison depends on source-extracted methodological
  statements and does not establish apparatus equivalence.
- Research relevance is organized from supplied documents; this layer does
  not perform live search or automatic NASA retrieval.
- Claim and condition extraction remains dependent on Step 3–5 heuristics.
- All source claims remain unverified and require qualified scientific and
  engineering review.
- The brief is not a certified spacecraft safety assessment.
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
summarization steps. Step 7 changes are limited to the files listed above.

