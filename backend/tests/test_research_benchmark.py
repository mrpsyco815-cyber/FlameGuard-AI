import json
import unittest
from pathlib import Path

from backend.services.query_understanding import parse_query, score_text


class TestResearchBenchmark(unittest.TestCase):
    def test_material_condition_precision(self):
        fixture = Path(__file__).parent / "fixtures" / "research_benchmark" / "records.json"
        records = json.loads(fixture.read_text(encoding="utf-8"))
        query = parse_query("PMMA flame spread microgravity 21% oxygen")
        ranked = sorted(
            ((score_text(query, item["text"])["score"], item) for item in records),
            key=lambda pair: pair[0],
            reverse=True,
        )
        top = [item for _, item in ranked[:2]]
        self.assertEqual(top[0]["id"], "pmma-microgravity")
        self.assertEqual(sum(item["relevant"] for item in top), 1)

