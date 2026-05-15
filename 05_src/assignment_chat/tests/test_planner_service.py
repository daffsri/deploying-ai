"""Tests for Service 3: function/tool-style weekend planner.

Run from 05_src/assignment_chat:
    uv run python -m unittest discover -s tests
"""

import unittest
from unittest.mock import patch

from services import planner_service


FAKE_MATCHES = [
    {
        "metadata": {
            "name": "High Park walk",
            "description": "Nature trails and green space",
            "cost": "free",
        }
    },
    {
        "metadata": {
            "name": "Distillery District",
            "description": "Art, cafes, and galleries",
            "cost": "$",
        }
    },
    {
        "metadata": {
            "name": "ROM visit",
            "description": "Explore history exhibits",
            "cost": "$$",
        }
    },
]


class TestPlannerService(unittest.TestCase):
    def test_plan_weekend_uses_weather_and_activity_search(self):
        with patch.object(planner_service, "get_weather_summary", return_value="Sunny and 20°C."):
            with patch.object(planner_service, "semantic_search", return_value=FAKE_MATCHES) as mock_search:
                result = planner_service.plan_weekend(
                    indoor=False, budget="free", group_size=2, city="Toronto"
                )

        mock_search.assert_called_once()
        query_used = mock_search.call_args.args[0]
        self.assertIn("free", query_used)
        self.assertIn("outdoor", query_used)

        self.assertIn("I’m CitySidekick", result)
        self.assertIn("Weather check", result)
        self.assertIn("Sunny and 20°C", result)
        self.assertIn("High Park walk", result)
        self.assertIn("Your Saturday plan", result)

    def test_plan_weekend_handles_no_matches(self):
        with patch.object(planner_service, "get_weather_summary", return_value="Rainy."):
            with patch.object(planner_service, "semantic_search", return_value=[]):
                result = planner_service.plan_weekend(indoor=True, budget="$", group_size=1)

        self.assertIn("could not find activities", result.lower())
        self.assertIn("weekend", result.lower())


if __name__ == "__main__":
    unittest.main()
