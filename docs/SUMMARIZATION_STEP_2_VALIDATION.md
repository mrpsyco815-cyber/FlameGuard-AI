# Summarization Engine Step 2 Validation

## Status

**PASS for the scoped Step 2 extraction and acquisition hardening.**

This step improved explicit NASA PDF import diagnostics and page-level
extraction only. It did **not** implement section-aware extraction,
scientific-finding extraction, claim-level summarization, or multi-paper
synthesis. No live NASA download was performed.

The existing local-first search behavior remains unchanged, and ordinary
search/summarization does not automatically download NASA PDFs.

## Exact files changed

### Implementation

- [document_parser.py](../backend/services/document_parser.py)
  - Added structured extraction statuses.
  - Added optional local PDF/output paths for controlled testing while keeping
    the existing NASA-ID default behavior.
  - Preserved page order, page numbers, text, counts, source URL, and metadata.
  - Distinguished complete, partial, valid-but-empty, missing, and malformed
    extraction outcomes.
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
  - Propagated extraction diagnostics into explicit import responses.
  - Reported download/import and identity-validation failures distinctly.
  - Preserved existing append-only behavior and manual-review status.

### Tests

- [test_document_processing_step2.py](../backend/tests/test_document_processing_step2.py)
  - Added controlled local synthetic-PDF tests.
  - Added abstract-only NASA response scope test.

### Not changed

- [nasa_documents.py](../backend/services/nasa_documents.py) was inspected but
  did not require a code change for this step. Its explicit download path
  already validates NASA-hosted URLs, limits size, checks content type and PDF
  signature, rejects HTML, and cleans temporary files.
- NASA and BASS-II datasets.
- Existing benchmark fixtures.
- Existing primary research records.
- Search ranking and ordinary summarization behavior.

## Implemented extraction statuses

### `success`

Returned when the PDF opens successfully and every page contains extracted
text.

Example diagnostic fields:

```text
success: true
extraction_status: success
pdf_page_count: 3
pages_with_extracted_text: 3
pages_without_extracted_text: 0
```

### `partial_extraction`

Returned when the PDF opens successfully but at least one page has no
extractable text. The document remains valid, and every page is retained in
order with its `pdf_page_number` and
`text_extraction_status`.

The implementation does not infer why a page is empty. It reports:

```text
extraction_message: One or more PDF pages contained no extractable text.
```

### `no_extractable_text`

Returned when the PDF opens successfully and has pages, but no page contains
extractable text. The implementation does not claim OCR was performed:

```text
extraction_message: OCR required or text extraction unavailable.
```

### `invalid_pdf`

Returned for an invalid NASA ID, missing PDF, zero-page PDF, encrypted PDF, or
malformed/corrupt PDF extraction failure. The error field preserves the
specific failure message.

### Import-level diagnostics

The explicit import path retains its established `status` values and adds an
`extraction_status` diagnostic:

- `pdf_unavailable` with `extraction_status=download_or_import_failed` when
  official PDF acquisition is unavailable or fails;
- `pdf_identity_audit_failed` with
  `extraction_status=identity_validation_failed` when the identity audit cannot
  complete;
- `pdf_identity_requires_manual_review` when the PDF does not confirm the
  NASA catalogue title, with `extraction_status=identity_validation_failed`;
- `pdf_text_extraction_failed` when extraction fails after identity validation;
- `no_extractable_text` when a valid PDF contains no usable text; and
- `imported_pending_review` when passages are appended successfully.

Existing response fields and the previous manual-review safeguards remain
available for compatibility.

## Behavior implemented

### PDF acquisition remains explicit

`download_nasa_pdf()` is still called only by the explicit
`/research/import/{nasa_id}` flow. Ordinary endpoints such as
`/research/search`, `/research/online-search`, and
`/research/combined-search` do not download PDFs.

No live NASA requests or downloads were made during this task. Tests use
mocked HTTP responses or locally generated PDFs.

### Page preservation

For every successfully opened PDF:

- PDF page count is recorded.
- Pages are processed in document order.
- Page numbers are one-based and preserved.
- Extracted text, character count, and word count are retained.
- Empty pages remain represented rather than being silently dropped.
- The NASA citation URL is preserved on the document and each page.
- `scientific_findings_verified` remains `false`.

### Identity validation

The existing import flow continues to:

1. Validate the NASA ID.
2. Retrieve NASA citation metadata.
3. Reject citation ID mismatches.
4. Download only an official validated NASA PDF.
5. Compare the PDF first-page title with the NASA catalogue title.
6. Stop before passage ingestion when identity confirmation fails.

Identity mismatch remains a manual-review rejection, not a successful import.

### Evidence-scope distinction

NASA online results remain:

```text
evidence_type: bibliographic_metadata_and_abstract
full_text_retrieved: false
scientific_findings_verified: false
```

Successful PDF extraction is represented separately through extracted page
text and page provenance. Extraction itself does not establish scientific
verification.

## Focused tests added and results

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_nasa_ingestion `
  backend.tests.test_nasa_online
```

Actual result:

```text
Ran 14 tests in 0.412s
OK
```

The new tests cover:

1. Valid text-based PDF.
2. Multi-page PDF and page ordering.
3. PDF containing an empty page.
4. Malformed/corrupted PDF.
5. Valid PDF with no extractable text.
6. NASA identity mismatch through existing ingestion tests.
7. Missing PDF.
8. Existing abstract-only record behavior.
9. NASA ID, citation URL, page number, and page-text provenance.
10. Existing NASA ingestion regression behavior.

The existing ingestion tests also verify that:

- imported passages preserve source IDs and pages;
- identity mismatch prevents extraction and collection creation;
- duplicate documents are not reimported;
- primary-dataset documents are not reimported; and
- imported records remain pending manual review and unverified.

## Actual sample diagnostic outputs

### Valid three-page text PDF

```text
success=True
extraction_status=success
pdf_page_count=3
pages_with_extracted_text=3
pages_without_extracted_text=0
page_numbers=[1, 2, 3]
page_texts=['first page', 'second page', 'third page']
```

### Three-page PDF with one empty page

```text
success=True
extraction_status=partial_extraction
pdf_page_count=3
pages_with_extracted_text=2
pages_without_extracted_text=1
empty_page_number=2
empty_page_status=no_text_extracted
```

### Valid two-page PDF with no text

```text
success=True
extraction_status=no_extractable_text
extraction_message=OCR required or text extraction unavailable.
pages_with_extracted_text=0
```

### Corrupt PDF

```text
success=False
extraction_status=invalid_pdf
error=<PyMuPDF PDF parsing error>
```

### Abstract-only NASA record

```text
evidence_type=bibliographic_metadata_and_abstract
full_text_retrieved=False
scientific_findings_verified=False
```

## Before/after behavior

| Behavior | Before Step 2 | After Step 2 |
|---|---|---|
| Complete text PDF | Returned page data with no document-level extraction status | Returns `success` with page/count diagnostics |
| PDF with empty pages | Returned `success` and empty-page counts | Returns `partial_extraction` and preserves empty-page status |
| Valid PDF with no text | Returned `success` with zero text pages | Returns `no_extractable_text` and explicitly reports `OCR required or text extraction unavailable` |
| Corrupt/missing PDF | Returned generic failure or missing-file error | Returns `invalid_pdf` plus explicit error |
| Identity mismatch | Existing manual-review rejection preserved | Same rejection, with `identity_validation_failed` diagnostic |
| Abstract-only result | Metadata/abstract flags already preserved | Unchanged; still not full text or verified |
| Ordinary search | Did not download PDFs | Still does not download PDFs |
| Existing imported records | Append-only collection behavior | Preserved; no overwrite or reimport |

## Full validation

### Complete backend test suite

Command:

```text
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test_*.py"
```

Result:

```text
Ran 83 tests
OK
```

The suite increased from 77 to 83 tests because six focused Step 2 tests were
added.

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

## Remaining limitations

- No OCR capability was added. Scanned/image-only documents are reported as
  `no_extractable_text`; OCR is not claimed or performed.
- PDF layout reconstruction for tables, figures, columns, headers, and
  footnotes remains out of scope.
- Section-aware extraction remains Step 3.
- Scientific finding extraction remains a later step.
- Successful text extraction does not establish scientific verification.
- The extraction status does not classify the specific cause of every empty
  page beyond the explicit no-text/OCR-required message.
- Download URL availability is discovered from NASA's manifest, but the
  normalized online search result does not itself expose concrete download
  links.
- No live NASA availability or latency claim was made in this validation.

## Preservation checks

- Branch remained `feature/research-backend`.
- No reset, clean, merge, rebase, commit, push, or stash operation occurred.
- Existing stash remained:
  `stash@{0}: On feature/research-backend: backup local mission intelligence changes`
- No files under `data` changed.
- No files under `backend/tests/fixtures` changed.
- No NASA or BASS-II dataset was modified.
- No dependency was installed.
- Existing user changes were preserved.

Step 3 section-aware extraction has not been started. Approval is required
before proceeding.
