from fastapi import FastAPI

from app.schemas import DraftReplyRequest, DraftReplyResponse
from app.services.drafting_engine import RuleBasedDraftingEngine
from app.config import settings


app = FastAPI(title="EmailCopilot API")

def get_drafting_engine():
    if settings.drafting_engine=="rule_based":
        return RuleBasedDraftingEngine()
    raise ValueError(f"Unsupported drafting engine: {settings.drafting_engine}")

drafting_engine = get_drafting_engine()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/draft-reply", response_model=DraftReplyResponse)
def draft_reply(request: DraftReplyRequest):
    return drafting_engine.generate(request.email_body)