# EmailCopilot

EmailCopilot is a browser-based AI email drafting assistant. It lets a user select or paste email text, generate a draft reply through a FastAPI backend, and copy the response directly from a Chrome extension.

**Note:** Simply selecting the text gets it in EmailCopilot. All you then have to do is click "generate reply".

![EmailCopilot Chrome extension demo](docs/emailcopilot-demo.png)

This project is a rebuild of an automatic email responder I first created in 2023: [intelligent-email](https://github.com/Olubusolami-R/email-copilot-v1). The original version explored Flask, React, PostgreSQL, Celery, Outlook integration, and an early GPT-2 fine-tuning attempt for email response generation.

This version rebuilds the idea with cleaner software engineering practices: a tested FastAPI backend, Docker support, configurable LLM providers, local Ollama inference for development, hosted OpenAI inference for deployment, and a polished Chrome extension client.

## Live backend

The backend is deployed on Render:

```text
https://email-copilotv2.onrender.com
```

Example endpoint:

```text
POST https://email-copilotv2.onrender.com/draft-reply
```

## What it does

- Chrome extension UI for drafting email replies
- Auto-loads selected text from the browser into the extension
- Sends email text to a hosted FastAPI backend
- Supports rule-based, Ollama, and OpenAI drafting providers
- Returns a draft reply, intent, confidence score, and review flag
- Lets users copy the generated draft
- Includes Docker setup and automated tests
- Uses mocked LLM tests so the test suite does not depend on external model services

## Architecture

```text
Chrome Extension
→ Hosted FastAPI Backend on Render
→ Drafting Engine
    → Rule-based baseline
    → Ollama local LLM
    → OpenAI hosted LLM
→ Draft reply + confidence + review flag
```

## Tech stack

- Python
- FastAPI
- Pydantic
- Pytest
- Docker / Docker Compose
- Ollama
- OpenAI API
- Render
- Chrome Extension Manifest V3
- JavaScript, HTML, CSS

## Repository structure

```text
.
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── styles.css
└── v2/
    └── backend/
        ├── app/
        ├── data/
        ├── scripts/
        ├── tests/
        ├── Dockerfile
        ├── docker-compose.yml
        └── requirements.txt
```

## Run the backend locally

From `v2/backend`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The local backend runs at:

```text
http://127.0.0.1:8000
```

## Run with Docker

From `v2/backend`:

```bash
docker compose up --build
```

## Environment variables

Create a local `.env` file inside `v2/backend`.

For the rule-based baseline:

```env
DRAFTING_ENGINE=rule_based
```

For local Ollama inference:

```env
DRAFTING_ENGINE=llm
LLM_PROVIDER=ollama
MODEL_NAME=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

For hosted OpenAI inference:

```env
DRAFTING_ENGINE=llm
LLM_PROVIDER=openai
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env`.

## Run tests

From `v2/backend`:

```bash
pytest
```

Or inside Docker:

```bash
docker compose run --rm tests
```

## Run the Chrome extension

1. Open `chrome://extensions`
2. Turn on **Developer mode**
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Select email text on a webpage or paste text into the extension
6. Click **Generate reply**
7. Copy the generated draft

The extension currently calls the hosted Render backend. For local development, update `API_URL` in `extension/popup.js` to:

```js
const API_URL = "http://127.0.0.1:8000/draft-reply";
```

## Example request

```bash
curl -X POST "https://email-copilotv2.onrender.com/draft-reply" \
  -H "Content-Type: application/json" \
  -d '{"email_body": "Hi, can we reschedule our meeting to Friday afternoon?"}'
```

Example response:

```json
{
  "draft": "Sure, Friday afternoon works for me. What time do you have in mind?",
  "intent": "llm_generated",
  "confidence": 0.6,
  "needs_review": true
}
```

## Current status

EmailCopilot is a working MVP with a Chrome extension client, hosted FastAPI backend, Dockerized setup, rule-based baseline, local Ollama support, hosted OpenAI inference, and mocked LLM tests.

The Chrome extension is currently distributed as an unpacked developer extension from this repository.
