"""The courier assistant: the agent people chat with. It answers general questions itself and
hands data questions to the SQL sub-agent through the ask_shipment_database tool."""

from __future__ import annotations

import asyncio
import logging
from datetime import date
from weakref import WeakValueDictionary

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ModelRequest,
    ModelRetryMiddleware,
    SummarizationMiddleware,
    ToolCallLimitMiddleware,
    dynamic_prompt,
)
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.types import Checkpointer

from ..security import ChatSession
from . import prompts
from .context import CourierContext
from .models import is_retryable

logger = logging.getLogger("courier.assistant")

LOOKUP_TOOL = "ask_shipment_database"
HIDDEN_FLAG = "courier_hidden"
FALLBACK_REPLY = "Sorry, I couldn't put an answer together. Could you rephrase your question?"


class AssistantUnavailable(RuntimeError):
    """The model or the database failed; the user should try again shortly."""


def build_assistant_graph(
    model: BaseChatModel,
    sql_agent,
    checkpointer: Checkpointer,
    *,
    summary_model: BaseChatModel | None = None,
    summary_trigger_tokens: int,
    summary_keep_messages: int,
):
    @tool(LOOKUP_TOOL)
    async def ask_shipment_database(question: str, runtime: ToolRuntime[CourierContext]) -> str:
        """Look up facts in the courier database for the person in this chat: their shipments,
        statuses, delivery dates, scan history, saved addresses and account details.

        Args:
            question: One complete, standalone question in English, including any tracking
                numbers, cities or dates from the conversation that it depends on.
        """
        try:
            result = await sql_agent.ainvoke(
                {"messages": [HumanMessage(question)]}, context=runtime.context
            )
        except Exception:
            logger.exception("The SQL sub-agent failed")
            return (
                "The lookup failed. Tell the user the shipment records can't be reached right now "
                "and to try again shortly."
            )
        answer = result["messages"][-1].text.strip()
        return answer or "The lookup returned nothing."

    @dynamic_prompt
    def instructions(request: ModelRequest) -> str:
        return prompts.assistant_prompt(request.runtime.context, date.today())

    return create_agent(
        model,
        tools=[ask_shipment_database],
        context_schema=CourierContext,
        middleware=[
            instructions,
            SummarizationMiddleware(
                summary_model or model,
                trigger=("tokens", summary_trigger_tokens),
                keep=("messages", summary_keep_messages),
                summary_prompt=prompts.SUMMARY_PROMPT,
            ),
            ModelRetryMiddleware(max_retries=2, retry_on=is_retryable, on_failure="error"),
            ToolCallLimitMiddleware(tool_name=LOOKUP_TOOL, run_limit=3),
            ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
        ],
        checkpointer=checkpointer,
        name="courier_assistant",
    )


def user_message(text: str, *, hidden: bool = False) -> HumanMessage:
    """A user turn. Hidden turns (the automatic first tracking question) are left out of the
    history the UI shows; the flag is never sent to the model provider."""
    return HumanMessage(text, additional_kwargs={HIDDEN_FLAG: True} if hidden else {})


def final_reply(messages: list[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls and message.text.strip():
            return message.text.strip()
    return FALLBACK_REPLY


class CourierAssistant:
    """What the API needs from the agent, with LangGraph details kept in one place."""

    def __init__(self, graph) -> None:
        self.graph = graph
        self._locks: WeakValueDictionary[str, asyncio.Lock] = WeakValueDictionary()

    def thread_lock(self, thread_id: str) -> asyncio.Lock:
        """One run at a time per conversation, so turns can't interleave in the checkpoint."""
        lock = self._locks.get(thread_id)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[thread_id] = lock
        return lock

    @staticmethod
    def config(session: ChatSession) -> dict:
        return {"configurable": {"thread_id": session.thread_id}}

    async def reply(self, session: ChatSession, text: str, *, hidden: bool = False) -> str:
        async with self.thread_lock(session.thread_id):
            try:
                result = await self.graph.ainvoke(
                    {"messages": [user_message(text, hidden=hidden)]},
                    self.config(session),
                    context=session.context,
                )
            except Exception as exc:
                logger.exception("Assistant run failed (thread %s)", session.thread_id[:8])
                raise AssistantUnavailable from exc
        return final_reply(result["messages"])
