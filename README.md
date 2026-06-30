# intelligent-email-copilot-v2

# EmailCopilot v2 Backend

A minimal FastAPI backend for generating draft email replies.

## Current scope

This first version exposes one endpoint:

`POST /draft-reply`

It accepts an email body and returns:

- a generated draft reply
- a confidence score
- whether the draft needs human review

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload