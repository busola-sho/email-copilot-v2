# EmailCopilot

EmailCopilot is a browser-based AI email drafting assistant. It lets a user select or paste email text, generate a draft reply through a FastAPI backend, and copy the response directly from a Chrome extension.

This project is a rebuild of an automatic email responder I first created in 2023. The original version explored Flask, React, PostgreSQL, Celery, Outlook integration, and GPT-2 fine-tuning. This version rebuilds the idea with cleaner software engineering practices, a tested backend, Docker support, and a local LLM-powered drafting engine.

## What it does

- Chrome extension UI for drafting email replies
- Auto-loads selected text from the browser into the extension
- Sends email text to a FastAPI backend
- Supports both rule-based and Ollama-backed LLM drafting engines
- Returns draft reply, intent, confidence, and review flag
- Lets users copy the generated draft
- Includes tests, Docker setup, and mocked LLM integration tests

## Architecture

```text
Chrome Extension
→ FastAPI Backend
→ Drafting Engine
    → Rule-based baseline
    → Ollama local LLM
→ Draft reply + confidence + review flag
```

## Tech stack

- Python
- FastAPI
- Pydantic
- Pytest
- Docker / Docker Compose
- Ollama
- Chrome Extension Manifest V3
- JavaScript, HTML, CSS

## Run the backend

From `v2/backend`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker compose up --build
```

## Use Ollama

Pull a local model:

```bash
ollama pull llama3.2:3b
```

Create a local `.env` file in `v2/backend`:

```env
DRAFTING_ENGINE=llm
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

## Run tests

```bash
pytest
```

Or inside Docker:

```bash
docker compose run --rm tests
```

## Run the extension

1. Open `chrome://extensions`
2. Turn on Developer mode
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Start the backend
6. Select email text on a webpage or paste text into the extension
7. Click **Generate reply**

## Current status

EmailCopilot currently supports a polished local MVP: Chrome extension client, FastAPI backend, Dockerized setup, rule-based baseline, Ollama LLM drafting, and mocked tests for reliable development.

Next steps include cloud deployment, better evaluation of draft quality, and richer browser/email-client integration.