# Summarization Engine Step 3 Validation

## Status

**PASS for the scoped section-aware extraction requirements.**

Section detection was implemented on top of the existing page-preserving PDF
pipeline. Step 2 extraction diagnostics, explicit PDF acquisition, identity
validation, provenance, and review safeguards remain in place.

This step does **not** implement scientific finding extraction, claim-level
summarization, or multi-paper synthesis.

No live NASA downloads were performed.

## Exact files changed

### Implementation

- [document_parser.py](../backend/services/document_parser.py)
  - Added conservative research-section heading detection.
  - Added support for optional numeric prefixes and subsection levels.
  - Added section text and page-span construction.
  - Added explicit unclassified text output.
  - Added uncertainty flags for ambiguous combined headings.
  - Integrated section metadata into `extract_pdf_pages()` without changing
    the existing `pages` output.
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
  - Preserved detected sections and unclassified text in imported document
    metadata.
  - Added section provenance to imported passage metadata when page/text
    mapping is available.

### Tests

- [test_section_extraction_step3.py](../backend/tests/test_section_extraction_step3.py)
  - Added local synthetic-document tests for all requested section cases.

### Documentation

- [SUMMARIZATION_STEP_3_VALIDATION.md](./SUMMARIZATION_STEP_3_VALIDATION.md)

No NASA/BASS-II dataset, benchmark fixture, or existing research record was
modified.

## Section extraction behavior

### Supported canonical sections

The parser recognizes heading aliases for:

- Abstract
- Introduction
- Background / Related Work
- Methodology / Methods
- Experimental Setup
- Results
- Discussion
- Conclusion
- Limitations
- References

Examples recognized by the same conservative heading matcher include:

```text
Abstract
1. Introduction
2. BACKGROUND
3.2 Experimental Setup
3.3 EXPERIMENTAL METHODS
References
```

### Section output

Each detected section contains:

```text
section_name
heading
section_level
text
page_start
page_end
page_numbers
detection_method
detection_uncertain
uncertainty_reason
scientific_findings_verified
```

The output is structural document metadata only. It does not assert that
section text contains a scientific finding and does not change the existing
verification state.

### Heading detection rules

Detection is intentionally conservative:

- The heading must appear as a standalone heading-like line.
- Optional numbering such as `1.`, `2.1`, or `3.2` is supported.
- Heading aliases are matched case-insensitively after whitespace
  normalization.
- Long sentence-like lines and lines ending in `.`, `!`, or `?` are not
  classified as headings.
- Unrecognized headings are not mapped to a known scientific section.
- `Results and Discussion` and `Discussion and Results` are retained as
  `results_and_discussion` and flagged with `detection_uncertain=true`.

### Page preservation and section spans

- Existing `pages` entries are unchanged.
- Page numbers remain one-based and document-ordered.
- Sections may span multiple pages.
- Empty pages between section boundaries remain in `page_numbers`.
- A page containing the next heading is included in the preceding section only
  when it contains text before that heading.
- Section text excludes the detected heading line itself.
- Missing sections are absent rather than synthesized.

### Unclassified text

`unclassified_text` preserves non-empty text outside recognized section
boundaries, including title/author material before the first recognized
heading and text associated with unrecognized headings. Each item includes
page start/end and a reason.

Empty pages are retained in the original page output and section page spans,
but do not create fabricated unclassified text.

## Actual sample extraction results

### Standard structure

Input pages contained:

```text
Page 1: title, Abstract, 1. Introduction
Page 2: Methods, Results
Page 3: Discussion, Conclusion
Page 4: References
```

Detected ordered sections:

```text
abstract               pages 1-1
introduction           pages 1-1
methodology_methods    pages 2-2
results                pages 2-2
discussion             pages 3-3
conclusion             pages 3-3
references             pages 4-4
```

### Multi-page section with an empty page

Input:

```text
Page 1: Introduction / First part
Page 2: empty
Page 3: Second part
Page 4: Results
```

Actual section span:

```text
section_name=introduction
page_start=1
page_end=3
page_numbers=[1, 2, 3]
text contains=First part.; Second part.
```

The empty page was not discarded and did not receive invented text.

### Ambiguous combined heading

Input:

```text
Results and Discussion
Combined text.
```

Actual structural result:

```text
section_name=results_and_discussion
detection_uncertain=True
uncertainty_reason=Combined Results/Discussion heading cannot be assigned to one canonical section.
```

### Unclassified preamble

Input:

```text
Document title and author.
Introduction
Introduction text.
```

The title/author line was preserved in `unclassified_text` rather than
discarded or assigned to Introduction.

## Focused tests

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_section_extraction_step3 `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_nasa_ingestion
```

Actual result after correcting a page-boundary test defect:

```text
Ran 20 tests in 0.338s
OK
```

The Step 3 tests cover:

1. Standard research-paper structure.
2. Numbered headings and subsection levels.
3. Heading capitalization variations.
4. Sections spanning multiple pages.
5. Missing sections.
6. Multiple subsections.
7. References detection.
8. Ambiguous combined headings.
9. Empty pages between sections.
10. Preservation of unclassified text.
11. Regression of Step 2 extraction behavior through the existing Step 2
    focused tests.
12. Existing NASA ingestion regression behavior.

## Full validation

### Full backend test suite

Command:

```text
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test_*.py"
```

Expected final result after the Step 3 tests were added:

```text
Ran 92 tests
OK
```

### Compile check

```text
.\.venv\Scripts\python.exe -m compileall -q backend
PASS
```

### Diff check

```text
git diff --check
PASS
```

## Acceptance criteria

| Criterion | Result |
|---|---|
| Detect supported research sections | PASS |
| Preserve original heading and section text | PASS |
| Preserve page start/end and ordering | PASS |
| Support numbered headings and subsections | PASS |
| Handle sections spanning pages | PASS |
| Preserve empty-page spans | PASS |
| Omit missing sections without invention | PASS |
| Preserve unclassified text | PASS |
| Flag ambiguous section detection | PASS |
| Preserve original page-level output | PASS |
| Keep section parsing separate from finding extraction | PASS |
| Avoid automatic PDF download | PASS |
| Avoid dataset/fixture modification | PASS |

## Remaining limitations

- Heading detection is heuristic and only recognizes conservative aliases.
- Unknown section names are preserved as unclassified text but are not given a
  generic section object.
- Complex layouts, multi-column ordering, tables, figures, headers, footers,
  OCR, and scanned PDFs remain outside this step.
- Section boundaries are line-based and depend on the quality of extracted
  text.
- A section heading split across lines may not be detected.
- Combined headings are retained but are intentionally uncertain.
- Section detection does not validate scientific claims or extract material,
  gravity, oxygen, measurements, units, findings, or limitations.
- Imported passage-to-section mapping is page/text based and may remain
  unresolved when a passage crosses a section boundary.

## Preservation checks

- No live NASA download was performed.
- No NASA or BASS-II dataset changed.
- No benchmark fixture changed.
- No existing research record was overwritten.
- No dependency was installed.
- No reset, clean, merge, rebase, commit, push, or stash operation occurred.
- Existing user changes and stash were preserved.
- Step 4 scientific finding extraction has not been started.

