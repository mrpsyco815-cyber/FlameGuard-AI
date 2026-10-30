# Data dictionary — FlameGuard AI v2 (2026-10-30)

## Files in this package
- `data/manifest.json` — package manifest, counts, status.
- `data/raw/` — original PDFs actually downloaded and opened. `bass_ii/` = BASS-II, `saffire_i/` = SAFFIRE, plus `spice/`, `sofie_gel/`, `same/`, `flex/` for the other verified core studies. Whole PSI datasets were NOT downloaded (PSI-25 255.77 GB, PSI-98 11.41 GB, PSI-107 6.47 GB).
- `data/processed/research_records.json` / `.csv` — VERIFIED CORE: 10 records extracted from opened PDFs, with evidence passages.
- `data/processed/extended_records.json` / `.csv` — EXTENDED SET: 176 headed entries from earlier summary-level harvests. These are preliminary, NOT verified, and NOT 176 unique studies (see validation_results.md).
- `data/evidence/evidence_passages.json` — 68 short verbatim passages (under 40 words each) from the verified core PDFs, with PDF page, section/table, source URL and file name.
- `data/documentation/source_register.csv` — assignment columns for the 11 core files plus 3 PSI investigation records.
- `data/documentation/data_quality_report.md`, `validation_results.md`, `backend_handover.md` — see those files.

## Fields in research_records.json (verified core)
- `study_id` — stable ID for this record, e.g. `saffire-vi-2024`. Unique in the core set.
- `title` — title as printed in the opened PDF, or the NASA/NTRS record title.
- `investigation` — BASS-II, SAFFIRE-IV/V, SAFFIRE-VI, SPICE, SoFIE-GEL, SAME, FLEX.
- `abstract` — null in v2. Full abstracts were not transcribed; the first evidence passage is a summary-level sentence, not a full abstract. Do not present it as the abstract.
- `plain_summary` — first evidence passage, for dashboard preview only.
- `experiment_conditions` — conditions ONLY as stated in the opened PDF, with conflicts kept as text (e.g. BASS-II flow 40 vs 0-55 cm/s). A condition not in the PDF is not in this object.
- `reported_findings` — the record's evidence passage texts, in order.
- `evidence_passages` — each with `text`, `page` (1-based PDF page), `section_or_table`, `experiment_context`.
- `source_url` — verbatim download URL of the opened PDF, or PSI landing page for PSI rows.
- `file_name`, `file_size` — real downloaded file, in bytes. PSI rows: file_size is the PSI total dataset size, not a downloaded file.
- `publication_details` — source file name only in v2; journal/date/DOI are in the source register where the file prints them.
- `license` — null unless the file itself prints a licence. NTRS "Public" distribution is NOT recorded as a licence. PSI rows carry CC0-1.0 as shown on the PSI record.
- `doi` — null unless printed in the file, except PSI rows where the DOI is from the PSI record.
- `missing_fields` — fields explicitly missing for this record.
- `verification_status` — `verified_from_opened_pdf` for all 10 core records; `psi_record_verified` for PSI rows; `preliminary` for all extended records.
- `moon_mars_rank` — 1 = most useful for Moon/Mars comparison in this core, 3 = context only. This is a comparison-usefulness rank, NOT a paper-quality score and NOT a safe/unsafe verdict.
- `moon_mars_rank_reason` — reason for the rank.
- `comparison_keys` — fuel/material, platform, gravity. Compare only records with matching platform/gravity/flow direction; never compare droplet/gas/emulator numbers with solid spread limits, and never compare a model or planned test with a flight measurement.
- `platform_type` — ISS flight (ISS or Cygnus) for all core records.

## Fields in source_register.csv
Assignment columns: study_id, title, investigation, source_url, file_name, file_format, file_size, publication_date, doi, license, access_status, extraction_status, verification_notes. Empty means the file/record does not state it; nothing was guessed.

## What the AI must NOT conclude from this data
- No safe/unsafe prediction for a real cabin, Moon habitat, or Mars habitat.
- No single "Saffire oxygen", "BASS-II flow limit", or "microgravity flammability limit" — values are per-test, per-geometry, per-duct, per-flow-direction.
- Ventilation-off does NOT mean fire out: BASS flames quenched when the fan stopped in some tests, but Saffire smolder, GEL pulsations, and still-air BRE-type persistence show post-flame persistence in other cases.
- Droplet LOI, gas-jet smoke points, and emulator results are NOT solid-material spread limits.
- Planned tests (FM2) and simulated-gravity tests (LUCI) in the extended set are NOT flight measurements.
