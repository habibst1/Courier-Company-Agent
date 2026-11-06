"""Test doubles shared by the test modules."""

from __future__ import annotations

import itertools
import json
import re
from collections.abc import Iterable

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGenerationChunk
from pydantic import SecretStr

from app.config import Settings


class ScriptedModel(GenericFakeChatModel):
    """Replays a fixed list of replies and accepts tools, standing in for a real chat model.

    Unlike GenericFakeChatModel, it keeps tool calls when streamed, as real models do.
    """

    def bind_tools(self, tools, **kwargs):
        return self

    def _stream(self, messages, stop=None, run_manager=None, **kwargs):
        reply = self._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
        message = reply.generations[0].message
        if message.tool_calls:
            calls = [
                {"name": c["name"], "args": json.dumps(c["args"]), "id": c["id"], "index": i}
                for i, c in enumerate(message.tool_calls)
            ]
            yield ChatGenerationChunk(
                message=AIMessageChunk(content="", tool_call_chunks=calls, chunk_position="last")
            )
            return
        tokens = re.split(r"(\s)", message.content) if message.content else []
        for index, token in enumerate(tokens):
            last = "last" if index == len(tokens) - 1 else None
            chunk = ChatGenerationChunk(message=AIMessageChunk(content=token, chunk_position=last))
            if run_manager:
                run_manager.on_llm_new_token(token, chunk=chunk)
            yield chunk


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
