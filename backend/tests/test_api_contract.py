import unittest

from backend.main import app


class TestBackendAPIContract(unittest.TestCase):
    def test_mission_research_route_is_registered(self):
        schema = app.openapi()
        self.assertIn("/research/mission-search", schema["paths"])
        operation = schema["paths"]["/research/mission-search"]["get"]
        parameters = {item["name"] for item in operation["parameters"]}
        self.assertTrue({"q", "limit", "fuel", "mission"}.issubset(parameters))

    def test_nasa_import_route_is_registered(self):
        schema = app.openapi()
        self.assertIn("/research/import/{nasa_id}", schema["paths"])
        self.assertIn(
            "post",
            schema["paths"]["/research/import/{nasa_id}"],
        )

    def test_bass2_search_route_remains_available(self):
        schema = app.openapi()
        self.assertIn("/bass2/search", schema["paths"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
