from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    drafting_engine: str = "rule_based"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

