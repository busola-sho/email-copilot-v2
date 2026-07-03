from fastapi import FastAPI

from app.schemas import DraftReplyRequest, DraftReplyResponse
from app.services.draft_service import generate_draft_reply


app = FastAPI(title="EmailCopilot API")


@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/draft-reply", response_model=DraftReplyResponse)
def draft_reply(request: DraftReplyRequest):
    return generate_draft_reply(request.email_body)
