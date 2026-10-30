import json
import unittest
from pathlib import Path
from collections import defaultdict, Counter


ROOT = Path(__file__).resolve().parents[2]

STORE_PATH = ROOT / "data/processed/research_intelligence_store.json"

SOURCE_PATHS = {
    "nasa": ROOT / "data/processed/nasa_combined_evidence.json",
    "reviewed": ROOT / "data/processed/nasa_reviewed_evidence.json",
    "bass2": ROOT / "data/raw/bass2/FlameGuard_BASSII_Experimental_Dataset.json",
    "audit": ROOT / "data/processed/nasa_v34_classification_audit.json",
}


def read_json(path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


class TestResearchIntelligenceStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store = read_json(STORE_PATH)

        cls.sources = {
            name: read_json(path)
            for name, path in SOURCE_PATHS.items()
        }

        cls.records = cls.store["records"]

        cls.by_id = {
            record["record_id"]: record
            for record in cls.records
        }

    def test_total_record_count(self):
        self.assertEqual(len(self.records), 2836)
        self.assertEqual(self.store["record_count"], 2836)

    def test_all_record_ids_are_unique(self):
        ids = [record["record_id"] for record in self.records]
        self.assertEqual(len(ids), len(set(ids)))

    def test_record_type_counts(self):
        counts = Counter(
            record["record_type"] for record in self.records
        )

        self.assertEqual(counts["nasa_passage"], 2687)
        self.assertEqual(counts["reviewed_nasa_evidence"], 20)
        self.assertEqual(counts["bass2_experimental_record"], 129)

    def test_all_nasa_passages_match_original_and_audit(self):
        audit = {
            (item["nasa_id"], item["record_index"]): item
            for item in self.sources["audit"]["records"]
        }

        checked = 0

        for document in self.sources["nasa"]["documents"]:
            nasa_id = document["nasa_id"]

            for index, passage in enumerate(document["passages"]):
                record_id = f"NASA-PASSAGE-{nasa_id}-{index:04d}"
                record = self.by_id[record_id]

                audit_item = audit[(nasa_id, index)]

                self.assertEqual(
                    record["content"]["text"],
                    passage["text"]
                )

                self.assertEqual(
                    record["classification"],
                    audit_item["classification"]
                )

                self.assertEqual(
                    record["source"]["source_id"],
                    nasa_id
                )

                self.assertEqual(
                    record["source"]["pdf_page_number"],
                    passage.get("pdf_page_number")
                )

                checked += 1

        self.assertEqual(checked, 2687)

    def test_reviewed_evidence_is_preserved(self):
        originals = {
            item["evidence_id"]: item
            for item in self.sources["reviewed"]["evidence"]
        }

        for evidence_id, original in originals.items():
            record = self.by_id[f"REVIEWED-{evidence_id}"]

            self.assertEqual(
                record["content"]["text"],
                original["finding"]
            )

            self.assertEqual(
                record["conditions"]["raw_values"],
                original.get("conditions") or {}
            )

            self.assertEqual(
                record["source"]["pdf_page_number"],
                original["pdf_page_number"]
            )

        self.assertEqual(len(originals), 20)

    def test_bass2_raw_records_are_identical(self):
        dataset = self.sources["bass2"]

        for original in dataset["records"]:
            pi = str(original["PI"])
            test_number = str(original["Test #"])

            record = self.by_id[
                f"BASS2-{pi}-{test_number}"
            ]

            self.assertEqual(
                record["content"]["raw_record"],
                original
            )

            self.assertTrue(
                record["conditions"]["raw_values_preserved"]
            )

            self.assertFalse(
                record["conditions"]["numeric_normalization_performed"]
            )

    def test_all_bass2_quality_flags_are_linked(self):
        dataset = self.sources["bass2"]

        grouped = defaultdict(list)

        for flag in dataset["quality_flags"]:
            key = (str(flag["PI"]), str(flag["Test #"]))
            grouped[key].append(flag)

        linked_flags = 0

        for original in dataset["records"]:
            key = (
                str(original["PI"]),
                str(original["Test #"])
            )

            record = self.by_id[
                f"BASS2-{key[0]}-{key[1]}"
            ]

            expected = grouped.get(key, [])

            self.assertEqual(
                record["quality"]["flags"],
                expected
            )

            linked_flags += record["quality"]["flag_count"]

        self.assertEqual(linked_flags, 172)

    def test_no_record_claims_scientific_verification(self):
        self.assertFalse(
            self.store["scientific_findings_verified"]
        )

        for record in self.records:
            self.assertIs(
                record["review"]["scientific_findings_verified"],
                False
            )

    def test_v34_audit_is_not_a_separate_record_set(self):
        self.assertEqual(
            len(self.sources["audit"]["records"]),
            2687
        )

        self.assertNotIn(
            "v34_audit",
            self.store["record_type_counts"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
