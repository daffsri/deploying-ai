"""Tests for Service 2: semantic/local activity search.

These tests do not require OpenAI or ChromaDB. They verify the local dataset
and fallback retrieval path, which keeps the app usable during grading.

Run from 05_src/assignment_chat:
    uv runpython -m unittest discover -s tests
"""

import os
import unittest
from unittest.mock import patch

from services import semantic_service


class TestSemanticService(unittest.TestCase):
    def test_load_activities_has_required_columns(self):
        df = semantic_service.load_activities()
        required = {"name", "description", "indoor", "cost", "group", "tags"}
        self.assertTrue(required.issubset(set(df.columns)))
        self.assertGreaterEqual(len(df), 3)

    def test_activity_to_document_contains_searchable_fields(self):
        df = semantic_service.load_activities()
        document = semantic_service.activity_to_document(df.iloc[0])

        self.assertIn(str(df.iloc[0]["name"]), document)
        self.assertIn("Indoor:", document)
        self.assertIn("Cost:", document)
        self.assertIn("Tags:", document)

    def test_semantic_search_fallback_returns_ranked_matches(self):
        with patch.dict(os.environ, {}, clear=True):
            results = semantic_service.semantic_search(
                "cheap outdoors nature activity for two people", n_results=3
            )

        self.assertEqual(len(results), 3)
        self.assertIn("metadata", results[0])
        self.assertIn("document", results[0])
        self.assertIn("name", results[0]["metadata"])

    def test_format_activity_results_returns_natural_language(self):
        with patch.dict(os.environ, {}, clear=True):
            result = semantic_service.format_activity_results(
                "museum history indoor solo", n_results=2
            )

        self.assertIn("I found these local ideas", result)
        self.assertIn("-", result)
        self.assertNotIn("metadata", result.lower())


if __name__ == "__main__":
    unittest.main()
