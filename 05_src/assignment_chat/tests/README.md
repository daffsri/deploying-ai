# CitySidekick Tests

Run all tests from the assignment folder:

```bash
cd 05_src/assignment_chat
python -m unittest discover -s tests
```

What is covered:

- `test_api_service.py` checks Service 1 using mocked OpenWeather/Ticketmaster responses.
- `test_semantic_service.py` checks Service 2 dataset loading and local fallback search.
- `test_planner_service.py` checks Service 3 function-style weekend planning.
- `test_guardrails_and_memory.py` checks restricted-topic guardrails and sliding-window memory.

The tests avoid real network calls and do not require real API keys.
