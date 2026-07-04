import requests

from app.config import settings
from openai import OpenAI

SYSTEM_PROMPT = (
                "You are an email drafting assistant. "
                "Write a concise, polite draft reply. "
                "Answer all clear questions in the email, including casual ones, but keep the reply concise."
                "Do not invent extra plans, preferences, or details beyond what was asked."
                "Also do not add placeholders or any unnecessary information."
                "Return only the reply body. Do not include a subject line."
)

class LLMClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model_name = settings.model_name
        self.openai_api_key = settings.openai_api_key
        self.provider = settings.llm_provider

    def generate_ollama_reply(self, email_body:str)->str:
        #ollama call will be here
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content":SYSTEM_PROMPT,
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

    def generate_openai_reply(self, email_body:str)->str:
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")
        client = OpenAI(api_key=self.openai_api_key)

        response = client.responses.create(
            model=self.model_name,
            instructions=SYSTEM_PROMPT,
            input=f"Email to reply to:\n{email_body}",
        )

        return response.output_text.strip()

    def generate_llm_reply(self, email_body:str)->str:
        if self.provider=="ollama":
            return self.generate_ollama_reply(email_body)
        if self.provider=="openai":
            return self.generate_openai_reply(email_body)
        raise ValueError(f"Unsupported LLM provider: {self.provider}")