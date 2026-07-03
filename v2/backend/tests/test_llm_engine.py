import os

os.environ["DRAFTING_ENGINE"] = "llm" # Making this file solely for llm

from app.services.drafting_engine import LLMDraftingEngine

def test_llm_engine_returns_valid_response():
    engine = LLMDraftingEngine()

    result=engine.generate("Hi, can we schedule a meeting soon?")

    assert "draft" in result
    assert "intent" in result
    assert "confidence" in result
    assert "needs_review" in result

    assert isinstance(result["draft"], str)
    assert isinstance(result["confidence"], float)
    assert isinstance(result["intent"], str)
    assert isinstance(result["needs_review"], bool)

    assert result["intent"] == "llm_generated"
    assert result["needs_review"] is True