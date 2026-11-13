# Summarization Engine Step 5 Validation

## Status

**PASS for the scoped claim-level evidence-linked summarization requirements.**

This step adds a deterministic, extractive claim layer over the page-preserving
and section-aware document structures from Steps 2 and 3 and the structured
evidence from Step 4. It does not perform scientific verification, multi-paper
synthesis, mission recommendations, or automatic PDF acquisition.

No live NASA downloads were performed.

## Exact files changed

### Implementation

- [claim_summarizer.py](../backend/services/claim_summarizer.py)
  - Adds `extract_claims()`.
  - Adds `build_paper_summary()`.
  - Preserves exact excerpts and source/page/section provenance.
  - Rejects content from introduction, background, references, and unsupported
    sections as claim evidence.
  - Keeps abstract, methods, results, discussion, conclusion, and limitation
    evidence categories separate.
  - Supports additional source-linked excerpts for an existing claim.
- [document_parser.py](../backend/services/document_parser.py)
  - Adds `claim_summary` to the existing extracted-document result.
  - Does not change page, section, or structured-finding fields.
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
  - Preserves `claim_summary` in imported document metadata.
  - Does not alter primary datasets or existing records.

### Tests

- [test_claim_summarizer_step5.py](../backend/tests/test_claim_summarizer_step5.py)
  - Covers supported claims, rejected unsupported content, exact excerpts,
    provenance, abstract distinction, result/discussion/conclusion separation,
    multiple supporting excerpts, uncertainty, summary traceability, and empty
    evidence.

### Documentation

- [SUMMARIZATION_STEP_5_VALIDATION.md](./SUMMARIZATION_STEP_5_VALIDATION.md)

## Claim schema

Each extracted claim contains:

```text
claim_id                 # assigned in the paper summary
claim_text
claim_type
source_document_id
nasa_id
source_url
exact_supporting_excerpt
page_numbers
section_name
evidence_type
extraction_method
verification_status
uncertain
supporting_evidence
scientific_findings_verified
```

Supported claim types are:

- `experimental_observation`
- `experimental_result`
- `methodological_statement`
- `discussion_interpretation`
- `conclusion`
- `limitation`
- `abstract_statement`

The additional `abstract_statement` type is intentional. It prevents abstract
content from being mislabeled as independently verified experimental evidence.

Every claim remains:

```text
verification_status = not_scientifically_verified
scientific_findings_verified = false
```

## Classification behavior

| Source section | Claim classification |
|---|---|
| Abstract | `abstract_statement` |
| Methodology / Methods | `methodological_statement` |
| Experimental Setup | `methodological_statement` |
| Results | `experimental_result` or `experimental_observation` |
| Results and Discussion | `experimental_result` with uncertainty |
| Discussion | `discussion_interpretation` |
| Conclusion | `conclusion` |
| Limitations | `limitation` |
| Introduction / Background / References | Rejected as claim evidence |

Results sentences containing measurement or observation language are classified
as experimental results; other Results sentences are retained as experimental
observations. Discussion and Conclusion claims are never converted into direct
experimental results.

## Summary behavior

`build_paper_summary()` returns:

- Research objective.
- Experimental context.
- Materials and conditions.
- Main reported observations.
- Main interpretations.
- Limitations.
- Evidence gaps.

Every populated summary statement contains one or more `claim_ids`, and every
claim contains at least one exact supporting excerpt. Empty summary categories
produce the explicit statement:

```text
Insufficient verified evidence to support this statement.
```

The summary is extractive and source-linked. It does not create unsupported
numbers, units, thresholds, causal relationships, recommendations, or verified
scientific findings.

Multiple source excerpts can be attached to one claim through the
`additional_evidence` argument of `extract_claims()`. Each excerpt retains its
own page and provenance fields.

## Actual test results

### Focused Step 5 and regression tests

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_claim_summarizer_step5 `
  backend.tests.test_structured_findings_step4 `
  backend.tests.test_section_extraction_step3 `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_nasa_ingestion
```

Result:

```text
Ran 38 tests in 0.385s
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
Ran 110 tests in 1.390s
OK
```

### Compile and diff validation

- Backend `compileall`: passed.
- `git diff --check`: passed.

## Before and after behavior

Before Step 5:

- The parser exposed page text, sections, and structured candidate findings.
- The research summarizer provided retrieval-oriented evidence briefs.
- No claim-level object linked each source statement to an exact excerpt and
  summary statement.

After Step 5:

- Parsed documents additionally expose `claim_summary`.
- Imported document metadata preserves the claim summary.
- Claims are source-preserving, section-classified, page-linked, and explicitly
  unverified.
- Summary statements reference claim IDs.
- Unsupported sections and empty candidates do not create scientific claims.

Existing page extraction, section extraction, structured findings, ingestion
status values, search, ranking, and API contracts remain unchanged.

## Remaining limitations

- Extraction is deterministic and sentence-based; it does not understand
  tables, figures, equations, or complex multi-column reading order.
- It does not independently verify source claims or assess experimental quality.
- It does not resolve contradictions across papers.
- It does not infer causality, thresholds, uncertainty magnitudes, or
  engineering recommendations.
- Claim classification is heuristic and requires scientific review.
- Abstract statements remain source statements, not independently verified
  findings.
- OCR is not performed for scanned PDFs.
- Multi-paper synthesis and mission-specific recommendations remain out of
  scope.

## Preservation checks

- No NASA or BASS-II datasets were modified.
- No benchmark fixtures were modified.
- No existing research records were overwritten.
- No dependencies were installed.
- No live NASA downloads occurred.
- Existing user changes and stash were preserved.
- No reset, clean, rebase, merge, commit, push, or stash operation occurred.

The worktree contains pre-existing changes from the earlier research/search and
summarization steps. Step 5 changes are limited to the files listed above.

