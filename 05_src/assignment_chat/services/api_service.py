"""API service for CitySidekick.

Service 1 requirement: use public APIs as a backend and transform the output
into natural language rather than returning raw JSON.

Environment variables:
- OPENWEATHER_API_KEY
- TICKETMASTER_API_KEY
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

import requests


TORONTO_LAT = 43.6532
TORONTO_LON = -79.3832


def _get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_weather_summary(city: str = "Toronto") -> str:
    """Return a friendly weather summary for the next few days."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return (
            "Weather check is in demo mode because OPENWEATHER_API_KEY is not set. "
            "I can still plan activities, but live weather will be unavailable."
        )

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": f"{city},CA", "appid": api_key, "units": "metric"}

    try:
        data = _get_json(url, params)
    except Exception as exc:
        return f"I could not fetch live weather right now: {exc}"

    # Pick the next eight 3-hour forecast blocks, roughly the next 24 hours.
    forecasts = data.get("list", [])[:8]
    if not forecasts:
        return "I could not find a useful weather forecast."

    temps = [item.get("main", {}).get("temp") for item in forecasts if item.get("main")]
    descriptions = [
        item.get("weather", [{}])[0].get("description", "unknown conditions")
        for item in forecasts
    ]
    avg_temp = round(sum(temps) / len(temps), 1) if temps else "unknown"
    common_description = max(set(descriptions), key=descriptions.count)

    return (
        f"Live weather for {city}: around {avg_temp}°C with {common_description}. "
        f"Plan outdoor activities with a backup indoor option just in case."
    )


def get_event_summary(city: str = "Toronto", limit: int = 5) -> str:
    """Return a natural-language summary of upcoming Ticketmaster events."""
    api_key = os.getenv("TICKETMASTER_API_KEY")
    if not api_key:
        return (
            "Event search is in demo mode because TICKETMASTER_API_KEY is not set. "
            "Add the key to enable live Ticketmaster events."
        )

    now = datetime.now()
    end = now + timedelta(days=7)
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "city": city,
        "countryCode": "CA",
        "startDateTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "size": limit,
        "sort": "date,asc",
    }

    try:
        data = _get_json(url, params)
    except Exception as exc:
        return f"I could not fetch live events right now: {exc}"

    events = data.get("_embedded", {}).get("events", [])
    if not events:
        return f"I did not find Ticketmaster events for {city} this week."

    lines = []
    for event in events[:limit]:
        name = event.get("name", "Unnamed event")
        date = event.get("dates", {}).get("start", {}).get("localDate", "date TBA")
        venue = (
            event.get("_embedded", {})
            .get("venues", [{}])[0]
            .get("name", "venue TBA")
        )
        lines.append(f"{name} on {date} at {venue}")

    return "Here are some live events I found: " + "; ".join(lines) + "."


def get_weekend_live_summary(city: str = "Toronto") -> str:
    """Combine weather and event APIs into one transformed response."""
    weather = get_weather_summary(city)
    events = get_event_summary(city)
    return f"CitySidekick live scan for {city}:\n\n{weather}\n\n{events}"
