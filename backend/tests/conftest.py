from __future__ import annotations

import asyncio

import pytest

from app.config import get_settings
from app.database import Database


def pytest_asyncio_loop_factories(config, item):
    # psycopg's async mode needs a selector event loop; Windows defaults to Proactor.
    return {"selector": asyncio.SelectorEventLoop}


@pytest.fixture
async def database():
    """The real local database, prepared by scripts/setup_db.py. Skips when it isn't there."""
    try:
        settings = get_settings()
    except Exception as exc:
        pytest.skip(f"backend/.env is not configured: {exc}")
    db = Database(settings)
    try:
        await asyncio.wait_for(db.open(), timeout=15)
    except Exception as exc:
        await db.close()
        pytest.skip(f"PostgreSQL is not reachable with backend/.env: {exc}")
    yield db
    await db.close()
