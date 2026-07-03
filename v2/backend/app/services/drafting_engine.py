from abc import ABC, abstractmethod

from app.services.draft_service import generate_draft_reply
from app.services.llm_client import LLMClient

class DraftingEngine(ABC):
    @abstractmethod
    def generate(self, email_body: str) -> dict:
        pass


class RuleBasedDraftingEngine(DraftingEngine):
    def generate(self, email_body: str) -> dict:
        return generate_draft_reply(email_body)

class LLMDraftingEngine(DraftingEngine):
    def __init__(self):
        self.client=LLMClient()

    def generate(self, email_body: str) -> dict:
        draft=self.client.generate_llm_reply(email_body)
        return{
            "draft": draft,
            "confidence": 0.6,
            "intent": "llm_generated",
            "needs_review": True
        }
