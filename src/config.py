"""Application configuration loading and validation."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic import Field, PositiveInt, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    """Runtime settings loaded from environment variables.

    All values are strongly typed and validated at process startup to fail fast
    on invalid configuration.
    """

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY", min_length=10)
    openai_model_vision: str = Field(default="gpt-4o", alias="OPENAI_MODEL_VISION")
    openai_model_text: str = Field(default="gpt-4o", alias="OPENAI_MODEL_TEXT")
    openai_temperature: float = Field(default=0.0, alias="OPENAI_TEMPERATURE", ge=0.0, le=1.0)
    openai_timeout_seconds: PositiveInt = Field(default=60, alias="OPENAI_TIMEOUT_SECONDS")
    openai_max_retries: PositiveInt = Field(default=3, alias="OPENAI_MAX_RETRIES")

    langfuse_enabled: bool = Field(default=False, alias="LANGFUSE_ENABLED")
    langfuse_public_key: str | None = Field(default=None, alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str | None = Field(default=None, alias="LANGFUSE_SECRET_KEY")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", alias="LANGFUSE_HOST")

    request_timeout_seconds: PositiveInt = Field(default=120, alias="REQUEST_TIMEOUT_SECONDS")
    parse_timeout_seconds: PositiveInt = Field(default=90, alias="PARSE_TIMEOUT_SECONDS")
    agent_timeout_seconds: PositiveInt = Field(default=60, alias="AGENT_TIMEOUT_SECONDS")
    json_repair_max_attempts: PositiveInt = Field(default=2, alias="JSON_REPAIR_MAX_ATTEMPTS")

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    @field_validator("langfuse_public_key", "langfuse_secret_key")
    @classmethod
    def _strip_optional_keys(cls, value: str | None) -> str | None:
        """Normalize optional secret values to stripped text or None."""
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("openai_api_key")
    @classmethod
    def _validate_openai_key(cls, value: str) -> str:
        """Ensure the OpenAI key is non-empty and normalized."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("OPENAI_API_KEY cannot be empty")
        return normalized


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache environment settings.

    Returns:
        Validated Settings instance.

    Raises:
        RuntimeError: If required settings are invalid or missing.
    """

    load_dotenv(override=False)
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
