from pydantic import BaseModel, Field


class DraftReplyRequest(BaseModel):
    email_body: str = Field(..., min_length=1)


class DraftReplyResponse(BaseModel):
    draft: str
    intent: str
    confidence: float
    needs_review: bool