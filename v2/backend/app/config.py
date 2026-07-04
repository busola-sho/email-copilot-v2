from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    drafting_engine: str = "rule_based"
    llm_provider: str = "ollama"
    model_name: str = "llama3.2:3b"
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: str | None = None
    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()

