# Backend handover — FlameGuard AI v2 (2026-10-30)

## What to load first
Load `data/processed/research_records.json` — the verified core (10 records). This is the prototype dataset.
Load `data/processed/extended_records.json` only as a preliminary extended set, clearly labelled preliminary, never as verified studies.

## Schema (verified core record)
study_id (string, unique in core), title (string), investigation (string), abstract (null in v2), plain_summary (string or null), experiment_conditions (object, keys vary by record — read keys, do not assume a fixed set), reported_findings (array of passage texts), evidence_passages (array of {text, page, section_or_table, experiment_context}), source_url (string), file_name (string), file_size (integer bytes), publication_details (object), license (string or null), doi (string or null), missing_fields (array), verification_status (string), moon_mars_rank (1-3), moon_mars_rank_reason (string), comparison_keys {fuel_or_material, platform, gravity}, platform_type (string).

## Missing data
Represent null exactly as null, and display it honestly (e.g. "DOI not printed in this file"). Do not fill it from a summary or another study.

## Evidence display
For every answer, show at least one evidence passage with: study title, source URL, file name, PDF page, and experiment context. If a record has no passage for a claim, do not make that claim from that record.

## Search / rank / compare
- Search: title, investigation, fuel/material, platform.
- Rank: use moon_mars_rank only as comparison usefulness, and always show moon_mars_rank_reason beside it. Never display a rank as a safety score.
- Compare: only compare records with the same platform type and gravity, and never compare concurrent vs opposed flow, small duct vs large duct, droplet/gas vs solid, flight vs model/planned, without stating that difference.
- Demo: run `retrieve_demo.py` (in the zip root, outside data/) — it loads research_records.json, searches for "SAFFIRE", ranks the core, compares SAFFIRE-VI with SAFFIRE-IV/V, and prints evidence with page refs. Its output is saved as `demo_output.txt` in this package.

## What is NOT ready for backend finalisation
- Schema agreement with the backend developer (this file is a proposal, not an agreement).
- App retrieval test (local demo only).
- Extended-set unique-study mapping.
- SAME Table 1 and FLEX per-test tables.
