"""Database access through two connection pools with very different powers.

sandbox  The courier_agent role. Runs the SQL sub-agent's queries. It can only read the agent.*
         views, which show nothing until a scope is bound to the connection's backend PID.
app      The courier_app role. Binds and clears those scopes, checks logins and stores
         conversation checkpoints. LLM-written SQL never runs on it.

See db/sandbox.sql for the database side of this design.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from .agent.context import CourierContext
from .config import Settings

logger = logging.getLogger("courier.db")

_BIND_SCOPE = """
INSERT INTO agent.scope (pid, mode, user_id, tracking_number, bound_at)
VALUES (%s, %s, %s, %s, clock_timestamp())
ON CONFLICT (pid) DO UPDATE
SET mode = EXCLUDED.mode, user_id = EXCLUDED.user_id,
    tracking_number = EXCLUDED.tracking_number, bound_at = EXCLUDED.bound_at
"""
_UNBIND_SCOPE = "DELETE FROM agent.scope WHERE pid = %s"
_CLEAR_STALE_SCOPES = """
DELETE FROM agent.scope AS s
WHERE s.bound_at < now() - interval '10 minutes'
   OR NOT EXISTS (SELECT 1 FROM pg_stat_activity AS a WHERE a.pid = s.pid)
"""


@dataclass(frozen=True)
class QueryResult:
    columns: list[str]
    rows: list[dict[str, Any]]
    truncated: bool

    def to_json(self) -> str:
        return json.dumps(
            {
                "columns": self.columns,
                "rows": self.rows,
                "row_count": len(self.rows),
                "truncated": self.truncated,
            },
            default=_json_value,
            ensure_ascii=False,
        )


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return str(value)


class Database:
    def __init__(self, settings: Settings) -> None:
        self._timeout = settings.sql_timeout_seconds
        self._max_rows = settings.sql_max_rows
        self._sandbox = AsyncConnectionPool(
            settings.agent_database_url.get_secret_value(),
            min_size=1,
            max_size=5,
            open=False,
            name="sandbox",
            kwargs={"autocommit": False, "row_factory": dict_row},
        )
        # Settings required by LangGraph's AsyncPostgresSaver, which shares this pool.
        self.app_pool = AsyncConnectionPool(
            settings.app_database_url.get_secret_value(),
            min_size=1,
            max_size=10,
            open=False,
            name="app",
            kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
        )

    async def open(self) -> None:
        await self._sandbox.open(wait=True, timeout=15)
        await self.app_pool.open(wait=True, timeout=15)
        async with self.app_pool.connection() as conn:
            await conn.execute(_CLEAR_STALE_SCOPES)

    async def close(self) -> None:
        await self._sandbox.close()
        await self.app_pool.close()

    async def ping(self) -> bool:
        try:
            async with self.app_pool.connection(timeout=3) as conn:
                await conn.execute("SELECT 1")
        except Exception:
            logger.warning("Database ping failed", exc_info=True)
            return False
        return True

    async def run_scoped(
        self, sql: str, scope: CourierContext, *, max_rows: int | None = None
    ) -> QueryResult:
        """Run one statement as the sandbox role, seeing only what `scope` may see.

        `sql` must come from sql_guard.validate_select or be a fixed internal query. It runs as a
        prepared statement (so PostgreSQL rejects anything with more than one statement) inside a
        READ ONLY transaction that is always rolled back.
        """
        limit = max_rows or self._max_rows
        async with self._sandbox.connection() as conn:
            pid = conn.info.backend_pid
            await self._bind(pid, scope)
            try:
                async with asyncio.timeout(self._timeout), conn.transaction(force_rollback=True):
                    await conn.execute("SET TRANSACTION READ ONLY")
                    cursor = await conn.execute(sql, prepare=True)
                    rows = await cursor.fetchmany(limit + 1)
                    columns = [column.name for column in cursor.description or ()]
            finally:
                await self._unbind(pid)
        return QueryResult(columns=columns, rows=rows[:limit], truncated=len(rows) > limit)

    async def tracking_number_exists(self, tracking_number: str) -> bool:
        scope = CourierContext(mode="recipient", tracking_number=tracking_number)
        result = await self.run_scoped("SELECT 1 AS found FROM agent.shipments", scope, max_rows=1)
        return bool(result.rows)

    async def customer_profile(self, user_id: int) -> dict[str, Any] | None:
        scope = CourierContext(mode="customer", user_id=user_id)
        result = await self.run_scoped(
            "SELECT username, full_name, email, phone FROM agent.my_account", scope, max_rows=1
        )
        return result.rows[0] if result.rows else None

    async def find_login(self, identifier: str) -> dict[str, Any] | None:
        """The login row for a user name or e-mail address (case-insensitive), if any."""
        async with self.app_pool.connection() as conn:
            cursor = await conn.execute(
                "SELECT user_id, username, full_name, password_hash FROM auth.login_lookup "
                "WHERE lower(username) = lower(%s) OR lower(email) = lower(%s) LIMIT 1",
                (identifier, identifier),
            )
            return await cursor.fetchone()

    async def _bind(self, pid: int, scope: CourierContext) -> None:
        async with self.app_pool.connection() as conn:
            await conn.execute(_BIND_SCOPE, (pid, scope.mode, scope.user_id, scope.tracking_number))

    async def _unbind(self, pid: int) -> None:
        try:
            async with self.app_pool.connection() as conn:
                await conn.execute(_UNBIND_SCOPE, (pid,))
        except Exception:
            # The row expires after two minutes and the next query on this connection rebinds it.
            logger.warning("Could not clear the scope for backend %s", pid, exc_info=True)
