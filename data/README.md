# FlameGuard AI — v2 complete core (2026-10-30)

This zip follows the team assignment Task 3 `data/` tree, with extra raw folders and an extended set, all documented in `data/documentation/`.

## What is complete in v2
- Verified core: 10 records from 11 PDFs actually downloaded and opened, 68 evidence passages with PDF page refs.
- PSI investigations verified live: PSI-25 (BASS-II, DOI 10.60555/4qc4-de67, CC0-1.0), PSI-98 (SAFFIRE-I, DOI 10.60555/0t15-1z43, CC0-1.0), PSI-107 (SPICE, DOI 10.60555/9kbh-e962, CC0-1.0), plus PSI-99/PSI-100 found by search. Whole PSI datasets were NOT downloaded (255.77 GB / 11.41 GB / 6.47 GB).
- Conflicts resolved from primary PDFs: SAFFIRE per-test O2/pressure, SAFFIRE-VI 981 s detection lag, FLEX report number 2015-216046, SPICE counts kept separate.
- Local retrieval demo: `retrieve_demo.py` + `demo_output.txt` — load, search, rank, compare, evidence, honest nulls.

## What is still NOT complete, stated plainly
- Extended set (176 headed entries) is preliminary, not verified, and not 176 unique studies.
- Backend schema agreement with the team's backend developer: not done.
- Retrieval test in the team's actual app: not done (local demo only).
- Push to the project data center: not done (no link/name provided).
- Some conflicts still open: BASS-II flow 40 vs 55 cm/s, SAFFIRE duct 46 vs 50 cm for I-III, SAME 1.7x vs 1.9x, SAFFIRE I/III journal tables (paywalled), current NASA-STD-6001 revision.
- This zip is about 63 MB, mostly the 41 MB FLEX detailed report. The team lead should decide whether that PDF belongs in version control; the JSON/CSV alone is enough for backend loading.

## Structure
```
data/
├── manifest.json
├── raw/bass_ii/, raw/saffire_i/, raw/spice/, raw/sofie_gel/, raw/same/, raw/flex/
├── processed/research_records.json + .csv  (verified core, 10)
├── processed/extended_records.json + .csv  (preliminary, 176)
├── evidence/evidence_passages.json  (68 passages)
└── documentation/data_dictionary.md, source_register.csv, data_quality_report.md, backend_handover.md, validation_results.md
retrieve_demo.py
demo_output.txt
README.md
```
