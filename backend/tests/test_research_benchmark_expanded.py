import json
import unittest
from pathlib import Path

from backend.services.query_understanding import parse_query, score_text


class TestExpandedResearchBenchmark(unittest.TestCase):
    def test_thirty_synthetic_cases_are_reproducible(self):
        path = Path(__file__).parent / "fixtures" / "research_benchmark" / "cases.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 30)
        top1_hits = 0
        precision_at_5_numerator = 0
        recall_at_10_hits = 0
        known_relevant = 0
        for case in cases:
            query = parse_query(case["query"])
            ranked = sorted(
                case["candidates"],
                key=lambda item: score_text(query, item[0])["score"],
                reverse=True,
            )
            top1_hits += int(ranked[0][1])
            precision_at_5_numerator += sum(
                int(item[1]) for item in ranked[:5]
            )
            known_relevant += sum(int(item[1]) for item in ranked)
            recall_at_10_hits += sum(int(item[1]) for item in ranked[:10])
        self.assertEqual(top1_hits, len(cases))
        self.assertEqual(precision_at_5_numerator, len(cases))
        self.assertEqual(recall_at_10_hits, known_relevant)
        self.assertEqual(
            top1_hits / len(cases),
            1.0,
        )
        # Precision@K uses K as the denominator; unavailable result slots
        # count as non-relevant rather than inflating the metric.
        self.assertEqual(
            precision_at_5_numerator / (len(cases) * 5),
            0.2,
        )
