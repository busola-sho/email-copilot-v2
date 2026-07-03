# EmailCopilot Backend

A FastAPI backend for generating draft email replies with intent detection, confidence scoring, and human-review flags.

This is a rebuild of an earlier automatic email responder project I created in 2023. The original version combined a Flask backend, PostgreSQL database, React frontend, Celery workers, Outlook email integration, and an early GPT-2 fine-tuning attempt for email response generation.

That first version helped me explore full-stack ML application development, but the codebase reflected my skill level at the time: the ML component was difficult to integrate cleanly, the system design was tightly coupled, and the project lacked proper testing, evaluation, containerization, and deployment readiness.

EmailCopilot is a deliberate rebuild of that idea with stronger software engineering practices. The current backend starts with a rule-based baseline, then adds a configurable local LLM drafting engine using Ollama.

## Features

- `POST /draft-reply` endpoint
- Pydantic request/response validation
- Rule-based intent detection baseline
- Local Ollama-backed LLM drafting engine
- Configurable drafting engine via `.env`
- Confidence score
- Human-review flag
- Intent-specific tests
- Mocked LLM client and engine tests
- Synthetic evaluation dataset
- Evaluation report generation
- Docker and Docker Compose support

## Architecture

```text
email body
→ FastAPI endpoint
→ Pydantic validation
→ drafting engine
    → rule-based engine OR Ollama LLM engine
→ draft reply
→ confidence + review flag
→ JSON response
```

## Drafting engines

The backend currently supports two drafting engines:

`rule_based`

A deterministic baseline that detects simple email intents such as meeting, thanks, follow-up, and unknown.

`llm`

A local Ollama-backed drafting engine that generates replies using a local language model.

The active engine is controlled through `.env`.

## Environment setup

Create a local `.env` file in `v2/backend/`.

For the rule-based engine:

```env
DRAFTING_ENGINE=rule_based
```

For the Ollama LLM engine:

```env
DRAFTING_ENGINE=llm
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

Do not commit `.env`. Use `.env.example` for safe example configuration.

## Run locally with Python

From `v2/backend`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/
```

Example response:

```json
{
  "status": "ok",
  "drafting_engine": "rule_based"
}
```

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/draft-reply" \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Hi, can we reschedule our meeting to Friday afternoon?"}'
```

Example rule-based response:

```json
{
  "draft": "Hi, thanks for your message. That works for me. Please let me know what time suits you best.",
  "intent": "meeting",
  "confidence": 0.7,
  "needs_review": true
}
```

Example LLM response:

```json
{
  "draft": "Hi, thanks for your message. Friday afternoon works for me. What time did you have in mind?",
  "intent": "llm_generated",
  "confidence": 0.6,
  "needs_review": true
}
```

## Run with Docker Compose

From `v2/backend`:

```bash
docker compose up --build
```

Then call the endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/draft-reply" \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Hi, thank you so much!"}'
```

## Run with Ollama

Install Ollama and pull a local model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running locally, then set:

```env
DRAFTING_ENGINE=llm
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Call the drafting endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/draft-reply" \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Hi, can we reschedule our meeting to Friday afternoon? Also, do you like food?"}'
```

If the backend is running inside Docker while Ollama is running on your Mac, use this instead:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

## Run tests

Run tests locally:

```bash
pytest
```

Run tests inside Docker:

```bash
docker compose run --rm tests
```

The normal test suite does not call the real Ollama server. LLM-related tests mock the layer underneath so tests remain fast, stable, and independent of external services.

## Manual Ollama integration test

To test the real local Ollama integration:

```bash
python scripts/test_ollama_integration.py
```

This script calls the actual local Ollama model and prints the generated draft. It is intentionally separate from the normal pytest suite.

## Run evaluation

Run the intent evaluation script:

```bash
python scripts/evaluate_intents.py
```

This writes an evaluation report to:

```text
reports/intent_eval.json
```

The current evaluation is intentionally simple. It gives a baseline for checking intent detection behaviour and provides a foundation for comparing drafting engines later.

## Testing strategy

The project separates different kinds of tests:

```text
API tests
→ check endpoint behaviour and response schema

Rule-based tests
→ check deterministic intent detection paths

LLM engine tests
→ check that the LLM engine returns the expected response shape

LLM client tests
→ mock Ollama HTTP responses and check response parsing

Manual integration script
→ calls the real local Ollama model
```

This keeps normal tests reliable while still allowing real model behaviour to be tested manually.

## Current status

Backend v1 established a clean, tested, containerized rule-based API.

Backend v2 adds a configurable LLM drafting engine using local Ollama, while preserving the same API contract.

The project is currently focused on backend architecture, model-serving boundaries, testing, and local deployment. Future work may include a browser extension client, richer evaluation of draft quality, async processing, and cloud deployment.