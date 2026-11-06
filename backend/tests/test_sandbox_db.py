"""The database side of the sandbox, against the real local database.

Several tests send SQL straight to Database.run_scoped, skipping sql_guard on purpose: they show
that PostgreSQL itself holds the line even if a query got past the application's checks."""

import psycopg
import pytest

from app.agent.context import CourierContext

pytestmark = pytest.mark.db

CUSTOMER_1 = CourierContext(mode="customer", user_id=1)
CUSTOMER_2 = CourierContext(mode="customer", user_id=2)
RECIPIENT = CourierContext(mode="recipient", tracking_number="TN4255-8215-9617")


async def count(db, sql, scope):
    result = await db.run_scoped(sql, scope)
    return result.rows[0]["n"]


async def tracking_numbers(db, scope):
    result = await db.run_scoped("SELECT tracking_number FROM shipments", scope, max_rows=500)
    return {row["tracking_number"] for row in result.rows}


async def test_customers_only_see_their_own_shipments(database):
    mine = await tracking_numbers(database, CUSTOMER_1)
    theirs = await tracking_numbers(database, CUSTOMER_2)
    assert mine and theirs
    assert not mine & theirs
    # No WHERE clause needed: the view itself is scoped to the bound customer.
    assert await count(database, "SELECT count(*) AS n FROM shipments", CUSTOMER_1) == len(mine)


async def test_recipient_sees_one_shipment_without_street_addresses(database):
    result = await database.run_scoped(
        "SELECT tracking_number, destination_city, destination_address_line FROM shipments",
        RECIPIENT,
    )
    assert result.rows == [
        {
            "tracking_number": "TN4255-8215-9617",
            "destination_city": "Lyon",
            "destination_address_line": None,
        }
    ]
    events = await database.run_scoped(
        "SELECT DISTINCT tracking_number FROM tracking_events", RECIPIENT
    )
    assert [r["tracking_number"] for r in events.rows] == ["TN4255-8215-9617"]
    assert (await database.run_scoped("SELECT * FROM my_account", RECIPIENT)).rows == []


async def test_scope_is_cleared_after_each_query(database):
    await database.run_scoped("SELECT 1 AS n", CUSTOMER_1)
    async with database.app_pool.connection() as conn:
        rows = await (await conn.execute("SELECT count(*) AS n FROM agent.scope")).fetchone()
    assert rows["n"] == 0


@pytest.mark.parametrize(
    ("sql", "error"),
    [
        ("SELECT count(*) AS n FROM public.shipments", psycopg.errors.InsufficientPrivilege),
        ("SELECT * FROM agent.scope", psycopg.errors.InsufficientPrivilege),
        ("SELECT * FROM auth.credentials", psycopg.errors.InsufficientPrivilege),
        ("DELETE FROM agent.scope", psycopg.errors.ReadOnlySqlTransaction),
        ("UPDATE public.shipments SET status = 'lost'", psycopg.errors.ReadOnlySqlTransaction),
        ("SELECT 1; DELETE FROM agent.scope", psycopg.errors.SyntaxError),
    ],
)
async def test_database_blocks_what_the_guard_would_block(database, sql, error):
    with pytest.raises(error):
        await database.run_scoped(sql, CUSTOMER_1)


async def test_set_config_cannot_widen_the_scope(database):
    mine = await count(database, "SELECT count(*) AS n FROM shipments", CUSTOMER_1)
    sneaky = await count(
        database,
        "SELECT (SELECT count(*) FROM shipments) AS n, set_config('courier.user_id', '2', false)",
        CUSTOMER_1,
    )
    assert sneaky == mine


async def test_lookups_used_by_the_api(database):
    assert await database.tracking_number_exists("TN4255-8215-9617")
    assert not await database.tracking_number_exists("TN0000-0000-0000")
    profile = await database.customer_profile(1)
    assert profile["username"] == "habib_bencheikhali"
    assert profile["email"] == "habib.bencheikh@email.com"  # trailing newlines trimmed by the view
    assert await database.customer_profile(999_999) is None


async def test_demo_logins_were_seeded(database):
    from app.config import BACKEND_DIR
    from app.security import verify_password

    env = dict(
        line.split("=", 1)
        for line in (BACKEND_DIR / ".env").read_text(encoding="utf-8").splitlines()
        if "=" in line and not line.startswith("#")
    )
    row = await database.find_login("HABIB_BENCHEIKHALI")
    assert row["user_id"] == 1 and row["password_hash"].startswith("$argon2")
    assert await verify_password(row["password_hash"], env["DEMO_PASSWORD"])
    assert await database.find_login("habib.bencheikh@email.com") is not None
    assert await database.find_login("nobody-by-this-name") is None
