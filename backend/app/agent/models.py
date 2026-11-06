"""Chat model construction. Any init_chat_model id works; Groq keys come from settings."""

from __future__ import annotations

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from ..config import Settings

# A wrong key, missing permission or unknown model won't fix itself on retry.
_PERMANENT_STATUS_CODES = {401, 403, 404}


def make_chat_model(model_id: str, settings: Settings) -> BaseChatModel:
    kwargs: dict = {"temperature": settings.temperature}
    if model_id.startswith("groq:"):
        key = settings.groq_api_key.get_secret_value()
        if not key:
            raise RuntimeError("GROQ_API_KEY is empty. Add your Groq API key to backend/.env.")
        kwargs |= {"api_key": key, "max_retries": 2}
    return init_chat_model(model_id, **kwargs)


def is_retryable(exc: BaseException) -> bool:
    """Retry rate limits, timeouts and malformed tool calls, but not configuration errors."""
    return (
        isinstance(exc, Exception)
        and getattr(exc, "status_code", None) not in _PERMANENT_STATUS_CODES
    )
