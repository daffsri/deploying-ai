# CitySidekick — Your Weekend Activity Planner

CitySidekick is a chat-based weekend planning assistant for Toronto. Its personality is casual and funny: **"I fight boring weekends."** The assistant helps users discover live events, check weather, search a local activity dataset, and generate a simple weekend schedule.

## How to Run

From the repository root:

```bash
cd 05_src/assignment_chat
uv run python embeddings.py
uv run python app.py
```

Then open the Gradio link shown in the terminal.

## Environment Variables

The app is designed to run in demo mode even if API keys are missing, but full functionality uses:

```bash
export OPENAI_API_KEY="your_openai_key"
export OPENWEATHER_API_KEY="your_openweather_key"
export TICKETMASTER_API_KEY="your_ticketmaster_key"
```

Optional:

```bash
export OPENAI_MODEL="gpt-4o-mini"
```

## Folder Structure

```text
05_src/assignment_chat/
├── app.py
├── services/
│   ├── api_service.py
│   ├── semantic_service.py
│   └── planner_service.py
├── chroma_db/
├── data/activities.csv
├── embeddings.py
└── readme.md
```

## Service 1 — API Calls: Live Events and Weather

Files:

- `services/api_service.py`

This service uses two public APIs:

1. OpenWeather forecast API
2. Ticketmaster Discovery API

Example user request:

> What's happening in Toronto this weekend?

The app calls both APIs and transforms the returned data into a short natural-language summary. It does not return the raw JSON response.

If API keys are missing, the app returns a clear demo-mode message instead of crashing.

## Service 2 — Semantic Search with ChromaDB

Files:

- `data/activities.csv`
- `services/semantic_service.py`
- `embeddings.py`
- `chroma_db/`

The local dataset contains Toronto activity ideas with columns:

- `name`
- `description`
- `indoor`
- `cost`
- `group`
- `tags`

The embedding script reads `activities.csv`, converts each row into a text document, embeds the documents with OpenAI embeddings, and stores them in a persistent ChromaDB collection.

Example user request:

> I want something cheap, outdoors, good for 2 people.

The app embeds the query, searches ChromaDB, and returns matching activity suggestions in natural language.

If ChromaDB or OpenAI embeddings are unavailable during grading, the app uses a simple keyword fallback so the interface remains testable.

## Service 3 — Function Calling: Weekend Planner

Files:

- `services/planner_service.py`
- `app.py`

The main planning function is:

```python
def plan_weekend(indoor: bool, budget: str, group_size: int):
```

When the user asks for a plan, the model can call this function. The function combines:

1. Weather information from the API service
2. Activity recommendations from semantic search
3. User preferences such as indoor/outdoor, budget, and group size

Example user request:

> Plan my Saturday, cheap and outdoors for 2 people.

The function returns a simple schedule with a morning activity, break, afternoon activity, and backup option.

## Gradio Chat Interface

File:

- `app.py`

The UI is implemented with Gradio. It includes:

- A chat window
- A text input
- A clear-chat button
- A distinct assistant personality

## Conversation Memory

CitySidekick stores chat history in Gradio state. To prevent long conversations from growing too large, the app uses a sliding window and keeps only the most recent messages:

```python
MAX_HISTORY_MESSAGES = 12
```

This demonstrates short-term memory while keeping the context manageable.

## Guardrails

CitySidekick blocks requests about restricted topics required by the assignment:

- Cats
- Dogs
- Horoscopes
- Zodiac signs
- Taylor Swift

It also blocks attempts to reveal or modify the system prompt, including phrases such as:

- "system prompt"
- "ignore previous instructions"
- "reveal your instructions"
- "modify your prompt"

When a blocked request is detected, the assistant refuses and redirects the user back to weekend planning.

## Design Decisions

The project intentionally keeps the architecture simple:

```text
Gradio Chat UI
    ↓
Conversation Memory + Guardrails
    ↓
Router / Function Calling
    ├── API Service
    ├── Semantic Search Service
    └── Planner Function
```

This satisfies the assignment requirements without overengineering the app. The app can run in partial demo mode without API keys, which makes it easier to test in different environments.
