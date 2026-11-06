"""The long-lived objects the API uses, built once at startup."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from .agent.assistant import CourierAssistant, build_assistant_graph
from .agent.models import make_chat_model
from .agent.sql_agent import build_sql_agent
from .config import Settings
from .database import Database
from .security import LoginTokens, SessionTokens


@dataclass
class Services:
    settings: Settings
    db: Database
    tokens: SessionTokens
    logins: LoginTokens
    assistant: CourierAssistant


@asynccontextmanager
async def build_services(settings: Settings) -> AsyncIterator[Services]:
    chat_model = make_chat_model(settings.model, settings)
    sql_model = make_chat_model(settings.sql_model or settings.model, settings)

    db = Database(settings)
    await db.open()
    try:
        if settings.checkpointer == "postgres":
            # Tables live in the "checkpoints" schema (courier_app's search_path).
            checkpointer = AsyncPostgresSaver(db.app_pool)
            await checkpointer.setup()
        else:
            checkpointer = InMemorySaver()

        sql_agent = build_sql_agent(sql_model, db, max_rows=settings.sql_max_rows)
        graph = build_assistant_graph(
            chat_model,
            sql_agent,
            checkpointer,
            summary_trigger_tokens=settings.summary_trigger_tokens,
            summary_keep_messages=settings.summary_keep_messages,
        )
        yield Services(
            settings=settings,
            db=db,
            tokens=SessionTokens(
                settings.session_secret.get_secret_value(), settings.session_max_age_hours
            ),
            logins=LoginTokens(
                settings.session_secret.get_secret_value(), settings.login_max_age_hours
            ),
            assistant=CourierAssistant(graph),
        )
    finally:
        await db.close()
