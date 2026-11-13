"""Run the 30-query scientific search benchmark and emit JSON diagnostics."""

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.services.research_summarizer import build_evidence_brief
from backend.services.ranking_contract import annotate_duplicate_sources


FIXTURE = ROOT / "backend" / "tests" / "fixtures" / "scientific_search_benchmark.json"


def run_benchmark():
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))
    output = []
    for case in cases:
        started = time.perf_counter()
        brief = build_evidence_brief(query=case["query"], limit=5)
        elapsed_ms = (time.perf_counter() - started) * 1000
        results = brief["results"]
        annotated = annotate_duplicate_sources(results)
        source_groups = {
            item["duplicate_source"]["group_key"]
            for item in annotated
            if item["duplicate_source"]["group_key"]
        }
        output.append({
            "id": case["id"],
            "category": case["category"],
            "query": case["query"],
            "count": len(results),
            "elapsed_ms": round(elapsed_ms, 2),
            "unique_sources": len(source_groups),
            "source_groups": sorted(source_groups),
            "results": annotated,
        })
    return output


def benchmark_metrics(result):
    returned_results = [item for row in result for item in row["results"]]
    unique_records = {}
    for item in returned_results:
        identity = item.get("record_id") or (
            item.get("source_id"),
            item.get("pdf_page_number"),
            item.get("exact_source_excerpt"),
        )
        unique_records.setdefault(identity, item)
    all_results = list(unique_records.values())
    annotated = annotate_duplicate_sources(all_results)
    groups = {
        item["duplicate_source"]["group_key"]
        for item in annotated
        if item["duplicate_source"]["group_key"]
    }
    duplicate_groups = {
        item["duplicate_source"]["group_key"]
        for item in annotated
        if item["duplicate_source"]["is_duplicate"]
    }
    return {
        "query_count": len(result),
        "returned_records": len(returned_results),
        "unique_returned_records": len(all_results),
        "unique_source_documents": len(groups),
        "duplicate_records": sum(
            item["duplicate_source"]["group_size"] > 1
            and item["duplicate_source"]["occurrence"] > 1
            for item in annotated
        ),
        "unique_duplicate_groups": len(duplicate_groups),
        "independent_evidence_sources": "unknown",
        "independent_evidence_source_count": 0,
        "documents_with_multiple_passages": len(duplicate_groups),
        "missing_provenance_records": sum(
            bool(item.get("ranking_contract", {}).get("provenance", {}).get("missing_fields"))
            for item in annotated
        ),
        "unknown_condition_records": sum(
            item.get("ranking_contract", {}).get("condition_match", {}).get("overall")
            == "unknown"
            for item in annotated
        ),
        "source_distribution": dict(Counter(
            item.get("ranking_contract", {}).get("source_type", "unknown")
            for item in annotated
        )),
        "runtime_ms": round(sum(item["elapsed_ms"] for item in result), 2),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_benchmark()
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)

    print(json.dumps(benchmark_metrics(result)), file=sys.stderr)


if __name__ == "__main__":
    main()
