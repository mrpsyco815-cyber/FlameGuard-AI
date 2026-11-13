import unittest

from backend.services.evidence_extractor import extract_structured_findings


class TestStructuredFindingsStep4(unittest.TestCase):
    def document(self):
        return {
            "nasa_id": "123",
            "citation_url": "https://ntrs.nasa.gov/citations/123",
            "sections": [
                {
                    "section_name": "abstract",
                    "heading": "Abstract",
                    "text": "The study examined PMMA in microgravity.",
                    "page_numbers": [1],
                    "page_start": 1,
                    "page_end": 1,
                    "detection_uncertain": False,
                },
                {
                    "section_name": "experimental_setup",
                    "heading": "Experimental Setup",
                    "text": (
                        "PMMA samples were tested in reduced gravity at "
                        "21 percent oxygen, ambient pressure 100 kPa, "
                        "and temperature 300 K. "
                        "Forced flow velocity was 10 cm/s."
                    ),
                    "page_numbers": [2],
                    "page_start": 2,
                    "page_end": 2,
                    "detection_uncertain": False,
                },
                {
                    "section_name": "results",
                    "heading": "Results",
                    "text": (
                        "The flame spread rate was 0.3 mm/s. "
                        "The observed flame became shorter."
                    ),
                    "page_numbers": [3, 4],
                    "page_start": 3,
                    "page_end": 4,
                    "detection_uncertain": False,
                },
                {
                    "section_name": "discussion",
                    "heading": "Discussion",
                    "text": "These results may indicate a flow effect.",
                    "page_numbers": [5],
                    "page_start": 5,
                    "page_end": 5,
                    "detection_uncertain": False,
                },
                {
                    "section_name": "limitations",
                    "heading": "Limitations",
                    "text": "The measurement uncertainty was not reported.",
                    "page_numbers": [6],
                    "page_start": 6,
                    "page_end": 6,
                    "detection_uncertain": False,
                },
            ],
            "unclassified_text": [],
        }

    def test_extracts_material_conditions_and_original_units(self):
        result = extract_structured_findings(
            self.document(),
            document_id="NASA-123",
        )

        self.assertEqual(result["fields"]["material_fuel"]["status"], "reported")
        self.assertEqual(
            result["fields"]["gravity_condition"]["status"], "reported"
        )
        oxygen = result["fields"]["oxygen_concentration"]["values"][0]
        self.assertEqual(oxygen["value"], "21")
        self.assertEqual(oxygen["unit"], "percent")
        self.assertEqual(
            result["fields"]["pressure"]["values"][0]["unit"], "kPa"
        )
        self.assertEqual(
            result["fields"]["temperature"]["values"][0]["unit"], "K"
        )
        self.assertEqual(
            result["fields"]["flow_condition"]["values"][0]["unit"], "cm/s"
        )

    def test_measurement_provenance_is_exact_and_page_linked(self):
        result = extract_structured_findings(
            self.document(),
            document_id="NASA-123",
        )

        measurement = next(
            item for item in result["measurements"]
            if item["field"] == "flow_condition"
        )
        self.assertEqual(measurement["source_document_id"], "NASA-123")
        self.assertEqual(measurement["nasa_id"], "123")
        self.assertEqual(
            measurement["source_url"],
            "https://ntrs.nasa.gov/citations/123",
        )
        self.assertEqual(measurement["page_numbers"], [2])
        self.assertIn("10 cm/s", measurement["exact_supporting_text"])
        self.assertEqual(
            measurement["verification_status"],
            "not_scientifically_verified",
        )

    def test_results_and_discussion_are_separate_evidence_categories(self):
        result = extract_structured_findings(self.document())

        self.assertTrue(result["scientific_observations"])
        self.assertEqual(
            result["scientific_observations"][0]["evidence_type"],
            "experimental_results",
        )
        self.assertTrue(result["scientific_findings"])
        self.assertEqual(
            result["scientific_findings"][0]["evidence_type"],
            "discussion_interpretation",
        )
        self.assertTrue(
            all(
                item["section_name"] != "abstract"
                for item in result["scientific_findings"]
            )
        )

    def test_limitations_are_extracted_separately(self):
        result = extract_structured_findings(self.document())
        self.assertEqual(len(result["limitations"]), 1)
        self.assertEqual(
            result["limitations"][0]["evidence_type"],
            "limitation_statement",
        )
        self.assertIn("uncertainty", result["limitations"][0]["value"].lower())

    def test_missing_fields_are_explicitly_not_reported(self):
        result = extract_structured_findings({
            "sections": [{
                "section_name": "introduction",
                "text": "A general introduction without measurements.",
                "page_numbers": [1],
                "page_start": 1,
                "page_end": 1,
            }],
            "unclassified_text": [],
        })

        self.assertEqual(
            result["fields"]["pressure"]["status"], "not_reported"
        )
        self.assertEqual(result["fields"]["pressure"]["values"], [])
        self.assertFalse(result["measurements"])

    def test_abstract_is_not_experimental_result(self):
        result = extract_structured_findings({
            "sections": [{
                "section_name": "abstract",
                "text": "The measured oxygen concentration was 21 percent.",
                "page_numbers": [1],
                "page_start": 1,
                "page_end": 1,
            }],
            "unclassified_text": [],
        })

        oxygen = result["fields"]["oxygen_concentration"]["values"][0]
        self.assertEqual(oxygen["evidence_type"], "abstract_statement")
        self.assertFalse(result["scientific_observations"])

    def test_unclassified_text_generates_uncertainty_not_a_finding(self):
        result = extract_structured_findings({
            "sections": [],
            "unclassified_text": [{
                "text": "Flame spread increased at 21 percent oxygen.",
                "page_start": 2,
                "page_end": 2,
                "reason": "Unknown heading.",
            }],
        })

        self.assertEqual(result["uncertainty"]["status"], "present")
        self.assertFalse(result["scientific_observations"])
        self.assertFalse(result["scientific_findings"])

    def test_ambiguous_section_marks_extracted_values_uncertain(self):
        result = extract_structured_findings({
            "sections": [{
                "section_name": "results_and_discussion",
                "text": "Pressure was 100 kPa.",
                "page_numbers": [4],
                "page_start": 4,
                "page_end": 4,
                "detection_uncertain": True,
                "uncertainty_reason": "Combined heading.",
            }],
            "unclassified_text": [],
        })

        value = result["fields"]["pressure"]["values"][0]
        self.assertTrue(value["uncertain"])
        self.assertEqual(
            value["evidence_type"], "results_and_discussion_statement"
        )

    def test_no_unsupported_finding_is_generated_from_intro_keywords(self):
        result = extract_structured_findings({
            "sections": [{
                "section_name": "introduction",
                "text": (
                    "Flame spread may increase with oxygen. "
                    "This paper investigates combustion."
                ),
                "page_numbers": [1],
                "page_start": 1,
                "page_end": 1,
            }],
            "unclassified_text": [],
        })

        self.assertFalse(result["scientific_observations"])
        self.assertFalse(result["scientific_findings"])
        self.assertFalse(result["evidence"])

    def test_multi_page_section_provenance_is_preserved(self):
        result = extract_structured_findings({
            "sections": [{
                "section_name": "results",
                "text": "The spread rate was 0.3 mm/s.",
                "page_numbers": [7, 8],
                "page_start": 7,
                "page_end": 8,
            }],
            "unclassified_text": [],
        }, nasa_id="999")

        value = result["fields"]["flow_condition"]["status"]
        self.assertEqual(value, "not_reported")
        observations = result["scientific_observations"]
        self.assertEqual(observations[0]["page_numbers"], [7, 8])
        self.assertEqual(observations[0]["nasa_id"], "999")
