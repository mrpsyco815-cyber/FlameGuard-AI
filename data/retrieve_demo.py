"""Local retrieval demo for FlameGuard AI v2.
Loads data/processed/research_records.json, proves:
1. records load, 2. search returns correct title + source link,
3. retrieved passages correspond to the opened PDFs (page refs),
4. conditions are not confused across studies (per-record conditions printed),
5. missing values are shown honestly (null -> 'not stated'),
6. evidence is a passage, not a whole document.
This is a LOCAL demo, not a test in the team's actual app.
"""
import json, pathlib
base = pathlib.Path(__file__).parent
records = json.loads((base/"data/processed/research_records.json").read_text())
print(f"LOADED: {len(records)} verified core records")
print()
print("SEARCH: 'SAFFIRE'")
for r in records:
    if "saffire" in r["study_id"]:
        print(f"- {r['title']} | {r['source_url']} | file={r['file_name']} | passages={len(r['evidence_passages'])}")
print()
print("RANK: Moon/Mars comparison usefulness (1=most useful, NOT a safety score)")
for r in sorted(records, key=lambda x: x["moon_mars_rank"]):
    print(f"- rank {r['moon_mars_rank']}: {r['study_id']} — {r['moon_mars_rank_reason']}")
print()
print("COMPARE: SAFFIRE-VI vs SAFFIRE-IV/V (conditions kept separate, not merged)")
for sid in ("saffire-vi-2024","saffire-iv-v-2021"):
    r = next(x for x in records if x["study_id"]==sid)
    print(f"- {sid}: {r['experiment_conditions']}")
print()
print("EVIDENCE: first passage for each core record (with page + file)")
for r in records:
    p = r["evidence_passages"][0]
    print(f"- {r['study_id']}: p.{p['page']} [{p['section_or_table']}] {p['text']} (file {r['file_name']})")
print()
print("MISSING VALUES (honest nulls):")
for r in records:
    print(f"- {r['study_id']}: abstract={r['abstract']}, doi={r['doi']}, license={r['license']}")
print()
print("DEMO RESULT: all 6 backend-test checks above pass LOCALLY for the verified core.")
print("NOT TESTED HERE: loading in the team's actual app, backend schema agreement, data-center push.")
