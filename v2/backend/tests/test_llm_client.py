from unittest.mock import Mock, patch

from app.services.llm_client import LLMClient

#the rule: to test a layer, mocj the layer underneath, requests.post in this case

def test_llm_client_returns_message_content_from_ollama_response():
    fake_response = Mock()
    fake_response.json.return_value = {
        "message": {
            "content": "Hi, Friday afternoon works for me. What time did you have in mind?"
        }
    }

    with patch("app.services.llm_client.requests.post", return_value=fake_response):
        client = LLMClient()
        result = client.generate_llm_reply(
            "Hi, can we reschedule our meeting to Friday afternoon?"
        )

    assert result == "Hi, Friday afternoon works for me. What time did you have in mind?"
    fake_response.raise_for_status.assert_called_once()