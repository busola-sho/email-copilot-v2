# Email Copilot V2

A FastAPI backend for generating draft email replies with intent detection, confidence scoring, and human-review flags.

This is the backend foundation for an AI email drafting assistant. The current version uses a rule-based drafting service so the API, evaluation, tests, and deployment workflow are solid before adding an LLM.

## Some context

This is a rebuild of an earlier automatic email responder project I created in 2023. The original version combined a Flask backend, PostgreSQL database, React frontend, Celery workers, Outlook email integration, and an early GPT-2 fine-tuning attempt for email response generation.

That first version helped me explore full-stack ML application development, but the codebase reflected my skill level at the time: the ML component was difficult to integrate cleanly, the system design was tightly coupled, and the project lacked proper testing, evaluation, containerization, and deployment readiness.

This version is a deliberate rebuild of that idea with stronger software engineering practices. The current version starts with a simple rule-based drafting service so the API contract, validation, tests, evaluation workflow, and Docker setup are solid before replacing the drafting logic with an LLM or fine-tuned model.

## Features

- `POST /draft-reply` endpoint
- Pydantic request/response validation
- Rule-based intent detection
- Draft reply generation
- Confidence score
- Human-review flag
- Intent-specific tests
- Synthetic evaluation dataset
- Evaluation report generation
- Docker + Docker Compose support

## Architecture

```text
email body
→ FastAPI endpoint
→ Pydantic validation
→ intent detection
→ draft generation
→ confidence + review flag
→ JSON response
```

## Run locally with Python

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

then open:

```bash
http://127.0.0.1:8000/docs
```

## Run with Docker Compose

```bash
docker compose up --build
```

## Example Request
```bash
curl -X POST "http://127.0.0.1:8000/draft-reply" \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Hi, can we reschedule our meeting to Friday?"}'
```

## Example Response
```bash
{
  "draft": "Hi, thanks for your message. That works for me. Please let me know what time suits you best.",
  "confidence": 0.7,
  "intent": "meeting",
  "needs_review": true
}
```

## Run evaluations
Run this script which writes an evaluation report to `reports/intent_eval.json`.

```bash
python scripts/evaluate_intents.py
```
