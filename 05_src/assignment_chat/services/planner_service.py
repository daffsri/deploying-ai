"""Planner service for CitySidekick.

Service 3 requirement: function/tool-style weekend planning.
The function can be called directly by the app or selected by the model.
"""

from __future__ import annotations

from services.api_service import get_weather_summary
from services.semantic_service import semantic_search


def plan_weekend(indoor: bool, budget: str, group_size: int, city: str = "Toronto") -> str:
    """Build a simple weekend plan using weather and semantic activity search."""
    preference = "indoor" if indoor else "outdoor"
    group_label = "solo" if group_size <= 1 else f"for {group_size} people"
    query = f"{budget} {preference} activity {group_label} Toronto weekend"

    matches = semantic_search(query, n_results=3)
    weather = get_weather_summary(city)

    if not matches:
        return "I could not find activities for that plan, but I refuse to let your weekend be boring."

    first = matches[0]["metadata"]
    second = matches[1]["metadata"] if len(matches) > 1 else first
    third = matches[2]["metadata"] if len(matches) > 2 else first

    return f"""I’m CitySidekick — I fight boring weekends.

Weather check:
{weather}

Your Saturday plan:
10:30 AM — Start with {first['name']}.
Why: {first['description']} Cost: {first['cost']}.

1:00 PM — Food/coffee break nearby. Keep it low-stress and flexible.

2:30 PM — Continue with {second['name']}.
Why: {second['description']} Cost: {second['cost']}.

5:00 PM — Backup option: {third['name']}.
Why: {third['description']} Cost: {third['cost']}.

Sidekick verdict: this is a solid {preference}, {budget}-budget plan {group_label}."""
