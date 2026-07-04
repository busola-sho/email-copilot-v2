from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import DraftReplyRequest, DraftReplyResponse
from app.services.drafting_engine import RuleBasedDraftingEngine, LLMDraftingEngine
from app.config import settings


app = FastAPI(title="EmailCopilot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # okay for MVP; restrict later if needed
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_drafting_engine():
    if settings.drafting_engine=="rule_based":
        return RuleBasedDraftingEngine()
    if settings.drafting_engine=="llm":
        return LLMDraftingEngine()
    raise ValueError(f"Unsupported drafting engine: {settings.drafting_engine}")

drafting_engine = get_drafting_engine()

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "drafting_engine":settings.drafting_engine
    }

@app.post("/draft-reply", response_model=DraftReplyResponse)
def draft_reply(request: DraftReplyRequest):
    return drafting_engine.generate(request.email_body)