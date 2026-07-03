import requests

from app.config import settings


class LLMClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model_name = settings.model_name

    def generate_llm_reply(self, email_body:str)->str:
        #llm call will be here
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an email drafting assistant. "
                            "Write a concise, polite draft reply. "
                            "Answer all clear questions in the email, including casual ones, but keep the reply concise."
                            "Do not invent extra plans, preferences, or details beyond what was asked."
                            "Also do not add placeholders or any unnecessary information."
                            "Return only the reply body. Do not include a subject line."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Email to reply to:\n{email_body}",
                    },
                ],
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]
