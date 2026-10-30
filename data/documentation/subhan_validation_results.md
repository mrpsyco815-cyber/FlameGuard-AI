# Validation results — FlameGuard AI v2 (2026-10-30)

## Counts actually counted from the built files
- Verified core records: 10
- Verified core evidence passages: 68 (BASS-II 8, SAFFIRE-VI 8, SAFFIRE-IV/V 6, SPICE Dotson 8, SPICE summary 5, GEL manuscript 8, GEL Task Book 5, SAME 7, FLEX methanol 6, FLEX detailed 7)
- Core files: 11 PDFs in data/raw/, 63,289,402 bytes total
- Extended records: 176 headed entries (preliminary, summary-level)
- Source register rows: 14 (11 core files + 3 PSI investigations)
- Records with a DOI: core PDFs 1 (SPICE Dotson); PSI rows 3; all other core PDFs null
- Records with a licence: PSI rows 3 (CC0-1.0); all core PDFs null
- Records with a source URL: 10/10 core, 14/14 register rows
- Records with evidence: 10/10 core, 0/176 extended

## Duplicate check
- Core: 10 unique study_ids, no duplicates.
- Extended: title+investigation exact-match check found 0 duplicates, but this does NOT prove 176 unique studies, because the standards harvest re-covers BASS/SAFFIRE/GEL/SAME/FLEX/SPICE/SLICE/ACME under different entry titles. Manual unique-study mapping is still required before the extended set is used as a study count. Do not report "176 studies".

## Source check
- Every core passage was checked as contiguous text on its stated PDF page (pdftotext extraction; PyMuPDF was not installed, pip blocked by system policy).
- PSI-25, PSI-98, PSI-107, PSI-99, PSI-100 verified by live PSI check 2026-10-30 (10-second wait for details to load).
- Journal papers listed as not opened were not quoted.

## Extraction review
- Two candidate passages in the SAME/FLEX pass failed exact-match verification and were dropped/replaced.
- GEL margin line numbers and PDF ligatures were normalised only for the check; passages quote the printed words.
- SAME NASA fact sheet was downloaded but no passages were taken from it; the NIST final report is the primary SAME source in v2.
- FLEX cool-flame journal papers were not downloaded (paywall route not attempted as a free PDF).

## Still not validated in v2
- Backend schema agreement with the team's backend developer: NOT done (handover notes prepared, demo script included, but no agreement recorded).
- Retrieval test in the team's actual app: NOT done. A local demo script (retrieve_demo.py, outside data/) proves loading/search/rank/compare/evidence display from the JSON, but it is not the team's app.
- Push to the project data center: NOT done (no data center link/name provided).
- SAME Table 1 full transcription, FLEX per-test LOI tables, SAFFIRE I/III journal tables: NOT done.
