import unittest

from backend.services.query_understanding import parse_query, score_text


class TestQueryUnderstanding(unittest.TestCase):
    def test_stopwords_do_not_create_tokens(self):
        with self.assertRaises(ValueError):
            parse_query("the and of with")

    def test_synonyms_and_materials_are_explainable(self):
        query = parse_query("PMMA flame propagation at 21% oxygen")
        score = score_text(query, "polymethyl methacrylate flame spread at 21 percent oxygen")
        self.assertIn("flame spread", query.concepts)
        self.assertIn("polymethyl methacrylate", query.materials)
        self.assertTrue(score["material_matches"])
        self.assertTrue(score["matching_reasons"])

    def test_wrong_material_is_penalized(self):
        query = parse_query("polyethylene flame spread")
        right = score_text(query, "polyethylene flame spread experiment")
        wrong = score_text(query, "PMMA flame spread experiment")
        self.assertGreater(right["score"], wrong["score"])
        self.assertIn("material mismatch penalty", wrong["matching_reasons"])

    def test_incompatible_conditions_are_rejected(self):
        query = parse_query(
            "PMMA liquid fuel normal gravity microgravity contradiction"
        )
        result = score_text(query, "PMMA flame spread in microgravity.")
        self.assertEqual(result["score"], 0.0)
        self.assertTrue(
            any("query contradiction" in reason for reason in result["matching_reasons"])
        )

    def test_extracts_spacecraft_and_measurement_intent(self):
        query = parse_query(
            "limiting oxygen concentration for flame extinction in spacecraft"
        )
        self.assertIn("spacecraft", query.environments)
        self.assertIn("flame extinction", query.phenomena)
        self.assertTrue(query.measurement_required)

    def test_quantitative_oxygen_context_is_distinguished(self):
        query = parse_query("oxygen concentration and flame spread")
        quantified = score_text(query, "Flame spread at 21 percent oxygen.")
        textual = score_text(query, "Flame spread depends on oxygen concentration.")
        self.assertTrue(quantified["quantitative_measurement_matches"])
        self.assertFalse(textual["quantitative_measurement_matches"])
        self.assertIn(
            "quantitative measurement context missing",
            textual["matching_reasons"],
        )

    def test_spacecraft_environment_mismatch_is_explained(self):
        query = parse_query("flame spread in spacecraft cabin")
        result = score_text(query, "Flame spread in a terrestrial laboratory.")
        self.assertIn("environment mismatch penalty", result["matching_reasons"])

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_query("and or the")
