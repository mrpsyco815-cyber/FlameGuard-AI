# Search Corrections Root-Cause Report

## Evidence inspected

The three real-world reports, final audit, scientific limitations/review guide, query parser, summarizer, federation, NASA connector, BASS-II loader, tests, and all 21-query baseline output were inspected. The baseline was executed individually before changes and stored at `C:\Users\User\AppData\Local\Temp\flameguard_21_query_baseline.json`.

## Findings

| Problem | Root cause | Status |
|---|---|---|
| Oxygen word matches without measurement context | `score_text` treated oxygen/concentration token overlap as sufficient and had no quantitative-measurement intent | Fixed partially: numeric oxygen context is now explicit; source passages without it receive a penalty and fallback can trigger |
| Generic spacecraft queries accepted as locally sufficient | Parser/fallback had no spacecraft/cabin environment intent or environment coverage check | Fixed partially: spacecraft/cabin environment intent and fallback coverage checks added |
| Fire detection/suppression/extinction intent was not explicit | Scientific concepts covered flame spread and oxygen but not these phenomena | Fixed: explainable phenomenon extraction added |
| Repeated source passages | Source-level diversification already existed; top-five data still contains repeats when fewer independent sources are available | Partially fixed before this task; unresolved as a data-availability limitation |
| Material mismatch | Existing material penalty was present and retained | Existing safeguard confirmed |
| Gravity mismatch | Existing contradiction handling covered microgravity/normal gravity; low/reduced gravity aliases were incomplete | Partially fixed: environment intent recognizes microgravity/reduced/low gravity; broader contradiction sets remain future work |
| NASA/local merging | Existing stable NASA-ID/URL merge was present and retained | Existing safeguard confirmed |
| Evidence scope confusion | Existing local review and NASA metadata flags were present and retained | Existing safeguard confirmed |
| BASS-II unsupported fields | Loader already validates the 17-column schema | No defect; no dataset change made |

## Corrections made

Only [query_understanding.py](../backend/services/query_understanding.py) and [research_federation.py](../backend/services/research_federation.py) were changed for this correction pass. The parser now exposes `phenomena`, `environments`, `measurement_required`, `environment_matches`, `phenomenon_matches`, and `quantitative_measurement_matches`. The federation requires requested environment and quantitative measurement coverage before considering local evidence sufficient.

## Important non-fixes

No embeddings, paid API, dataset edits, PDF downloads, or ranking rewrite were introduced. Existing source diversification, provenance, NASA evidence scope, BASS-II schema handling, and mission recommendation safeguards were preserved.
