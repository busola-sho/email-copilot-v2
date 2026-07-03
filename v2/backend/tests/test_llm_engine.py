from unittest.mock import patch

from app.services.drafting_engine import LLMDraftingEngine

#the rule: to test a layer, mocj the layer underneath, generate_llm_reply in this case

def test_llm_engine_returns_valid_response():
    with patch(
        "app.services.drafting_engine.LLMClient.generate_llm_reply",
        return_value="Hi, yes, happy to schedule a meeting soon."
    ):
        engine = LLMDraftingEngine()
        result = engine.generate("Hi, can we schedule a meeting soon?")

    assert result["draft"] == "Hi, yes, happy to schedule a meeting soon."
    assert result["intent"] == "llm_generated"
    assert isinstance(result["confidence"], float)
    assert result["needs_review"] is True