"""The SQL sub-agent: writes PostgreSQL for one question and runs it in the sandbox."""

from __future__ import annotations

import logging
from datetime import date
from typing import Protocol

import psycopg
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ModelRequest,
    ModelRetryMiddleware,
    ToolCallLimitMiddleware,
    dynamic_prompt,
)
from langchain.tools import ToolRuntime, tool
from langchain_core.language_models import BaseChatModel

from ..sql_guard import UnsafeQueryError, validate_select
from . import prompts
from .context import CourierContext
from .models import is_retryable

logger = logging.getLogger("courier.sql")

MAX_QUERIES = 4


class SandboxRunner(Protocol):
    async def run_scoped(self, sql: str, scope: CourierContext): ...


def build_sql_agent(model: BaseChatModel, db: SandboxRunner, *, max_rows: int):
    @tool
    async def run_sql(query: str, runtime: ToolRuntime[CourierContext]) -> str:
        """Run one read-only PostgreSQL SELECT on the views described in your instructions.

        Returns JSON with the column names and a limited number of rows, or an error to fix.

        Args:
            query: A single SELECT statement.
        """
        try:
            safe_sql = validate_select(query, max_rows=max_rows)
        except UnsafeQueryError as exc:
            logger.info("Rejected SQL (%s): %s", exc, query)
            return f"Query rejected: {exc}."
        try:
            result = await db.run_scoped(safe_sql, runtime.context)
        except TimeoutError:
            return "Database error: the query took too long. Simplify it."
        except psycopg.Error as exc:
            detail = (exc.diag.message_primary or str(exc)).strip()
            logger.info("SQL failed (%s): %s", detail, safe_sql)
            return f"Database error: {detail}"
        logger.info("SQL returned %d row(s): %s", len(result.rows), safe_sql)
        return result.to_json()

    @dynamic_prompt
    def instructions(request: ModelRequest) -> str:
        return prompts.sql_agent_prompt(request.runtime.context, date.today())

    return create_agent(
        model,
        tools=[run_sql],
        context_schema=CourierContext,
        middleware=[
            instructions,
            ModelRetryMiddleware(max_retries=2, retry_on=is_retryable, on_failure="error"),
            ToolCallLimitMiddleware(tool_name="run_sql", run_limit=MAX_QUERIES),
            ModelCallLimitMiddleware(run_limit=MAX_QUERIES + 2, exit_behavior="end"),
        ],
        # Stateless: every question starts fresh, and nothing about it is stored.
        checkpointer=False,
        name="sql_agent",
    )
