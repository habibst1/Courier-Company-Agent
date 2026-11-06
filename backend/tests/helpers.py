"""Test doubles shared by the test modules."""

from __future__ import annotations

import itertools
from collections.abc import Iterable

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from pydantic import SecretStr

from app.config import Settings


class ScriptedModel(GenericFakeChatModel):
    """Replays a fixed list of replies and accepts tools, standing in for a real chat model."""

    def bind_tools(self, tools, **kwargs):
        return self


class BrokenModel(ScriptedModel):
    """A chat model whose provider is down."""

    def _generate(self, *args, **kwargs):
        raise RuntimeError("provider unavailable")

    async def _agenerate(self, *args, **kwargs):
        raise RuntimeError("provider unavailable")

    def _stream(self, *args, **kwargs):
        raise RuntimeError("provider unavailable")

    async def _astream(self, *args, **kwargs):
        raise RuntimeError("provider unavailable")
        yield  # pragma: no cover - makes this an async generator


_call_ids = itertools.count(1)


def tool_call(name: str, **args) -> AIMessage:
    return AIMessage("", tool_calls=[{"name": name, "args": args, "id": f"call_{next(_call_ids)}"}])


def scripted(replies: Iterable[AIMessage | str]) -> ScriptedModel:
    return ScriptedModel(messages=iter(list(replies)))


def offline_settings(**overrides) -> Settings:
    values = {
        "agent_database_url": SecretStr("postgresql://courier_agent:x@localhost/none"),
        "app_database_url": SecretStr("postgresql://courier_app:x@localhost/none"),
        "session_secret": SecretStr("s" * 40),
        "checkpointer": "memory",
    } | overrides
    return Settings(_env_file=None, **values)
