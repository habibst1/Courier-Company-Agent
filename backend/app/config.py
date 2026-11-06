"""Settings, read from environment variables and backend/.env (see .env.example)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    # LLM
    groq_api_key: SecretStr = SecretStr("")
    model: str = "groq:openai/gpt-oss-20b"
    sql_model: str | None = None
    temperature: float = 0.0

    # Database: two roles with very different powers (see db/sandbox.sql)
    agent_database_url: SecretStr
    app_database_url: SecretStr
    sql_timeout_seconds: float = Field(8.0, gt=0)
    sql_max_rows: int = Field(50, ge=1, le=500)

    # Logins and chat sessions
    session_secret: SecretStr
    session_max_age_hours: int = Field(24, ge=1)
    login_max_age_hours: int = Field(12, ge=1)

    # Conversation memory
    checkpointer: Literal["postgres", "memory"] = "postgres"
    summary_trigger_tokens: int = Field(4000, ge=500)
    summary_keep_messages: int = Field(20, ge=2)

    # HTTP
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    log_level: str = "INFO"

    @field_validator("session_secret")
    @classmethod
    def _long_secret(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 32:
            raise ValueError("SESSION_SECRET must be at least 32 characters")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
