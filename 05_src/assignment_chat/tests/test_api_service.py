"""Tests for Service 1: live API service.

Run from 05_src/assignment_chat:
    uv run python -m unittest discover -s tests
"""

import os
import unittest
from unittest.mock import patch

from services import api_service


class TestApiService(unittest.TestCase):
    def test_weather_summary_transforms_openweather_json(self):
        fake_weather = {
            "list": [
                {"main": {"temp": 10}, "weather": [{"description": "light rain"}]},
                {"main": {"temp": 12}, "weather": [{"description": "light rain"}]},
                {"main": {"temp": 14}, "weather": [{"description": "cloudy"}]},
            ]
        }

        with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "fake-key"}):
            with patch("services.api_service._get_json", return_value=fake_weather):
                result = api_service.get_weather_summary("Toronto")

        self.assertIn("Live weather for Toronto", result)
        self.assertIn("12.0°C", result)
        self.assertIn("light rain", result)
        self.assertNotIn("{'list':", result)  # confirms it is not raw JSON

    def test_event_summary_transforms_ticketmaster_json(self):
        fake_events = {
            "_embedded": {
                "events": [
                    {
                        "name": "Jazz Night",
                        "dates": {"start": {"localDate": "2026-05-16"}},
                        "_embedded": {"venues": [{"name": "Massey Hall"}]},
                    },
                    {
                        "name": "Food Festival",
                        "dates": {"start": {"localDate": "2026-05-17"}},
                        "_embedded": {"venues": [{"name": "Harbourfront Centre"}]},
                    },
                ]
            }
        }

        with patch.dict(os.environ, {"TICKETMASTER_API_KEY": "fake-key"}):
            with patch("services.api_service._get_json", return_value=fake_events):
                result = api_service.get_event_summary("Toronto", limit=2)

        self.assertIn("Here are some live events", result)
        self.assertIn("Jazz Night", result)
        self.assertIn("Massey Hall", result)
        self.assertIn("Food Festival", result)
        self.assertNotIn("_embedded", result)  # confirms it is summarized, not raw JSON

    def test_api_service_demo_mode_without_keys(self):
        with patch.dict(os.environ, {}, clear=True):
            weather = api_service.get_weather_summary("Toronto")
            events = api_service.get_event_summary("Toronto")

        self.assertIn("demo mode", weather.lower())
        self.assertIn("demo mode", events.lower())


if __name__ == "__main__":
    unittest.main()
