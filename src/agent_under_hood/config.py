from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated at startup - a missing/invalid value fails fast with a
    clear error here, instead of failing confusingly mid-run."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    agent_model: str = Field(default="qwen3:1.7b", alias="AGENT_MODEL")
    max_iterations: int = Field(default=10, alias="AGENT_MAX_ITERATIONS")
    ollama_base_url: str = Field(
        default="http://localhost:11434", alias="OLLAMA_BASE_URL"
    )

    @field_validator("max_iterations")
    @classmethod
    def max_iterations_must_be_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("max_iterations must be at least 1")
        return value

    @field_validator("agent_model")
    @classmethod
    def agent_model_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("agent_model must not be blank")
        return value


settings = Settings()
