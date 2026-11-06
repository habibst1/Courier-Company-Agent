import pytest

from app.sql_guard import UnsafeQueryError, validate_select

ALLOWED = [
    "SELECT tracking_number, status FROM shipments ORDER BY created_at DESC LIMIT 5",
    "select count(*) from shipments where status = 'in_transit';",
    "SELECT status, count(*) AS n FROM shipments GROUP BY status",
    "SELECT * FROM agent.shipments",
    "SELECT s.tracking_number, e.location_city, e.scanned_at FROM shipments s "
    "JOIN tracking_events e ON e.tracking_number = s.tracking_number "
    "WHERE s.created_at > now() - interval '30 days' ORDER BY e.scanned_at DESC",
    "WITH latest AS (SELECT tracking_number, max(scanned_at) AS at FROM tracking_events "
    "GROUP BY tracking_number) SELECT * FROM latest",
    "SELECT to_char(expected_delivery_date, 'YYYY-MM-DD'), age(current_date, created_at::date), "
    "date_trunc('month', created_at), extract(day FROM created_at) FROM shipments",
    "SELECT tracking_number FROM shipments UNION SELECT tracking_number FROM tracking_events",
    "SELECT s.tracking_number, last.status FROM shipments s CROSS JOIN LATERAL "
    "(SELECT status FROM tracking_events t WHERE t.tracking_number = s.tracking_number "
    "ORDER BY scanned_at DESC LIMIT 1) last",
    "SELECT full_name, email FROM my_account",
    "SELECT city, country FROM my_addresses WHERE city ILIKE '%tun%'",
    "SELECT string_agg(DISTINCT destination_city, ', ') FROM shipments",
    "SELECT tracking_number, row_number() OVER (ORDER BY created_at) FROM shipments",
]

REJECTED = {
    "write": "UPDATE shipments SET status = 'delivered'",
    "delete": "DELETE FROM shipments",
    "ddl": "DROP TABLE shipments",
    "two statements": "SELECT 1; DROP TABLE shipments",
    "delete in cte": "WITH d AS (DELETE FROM shipments RETURNING *) SELECT * FROM d",
    "select into": "SELECT * INTO stolen FROM shipments",
    "row locks": "SELECT * FROM shipments FOR UPDATE",
    "copy to program": "COPY shipments TO PROGRAM 'calc.exe'",
    "set": "SET search_path = public",
    "base table": "SELECT * FROM public.shipments",
    "other table": "SELECT * FROM users",
    "credentials": "SELECT * FROM auth.credentials",
    "catalog": "SELECT * FROM pg_catalog.pg_user",
    "information schema": "SELECT * FROM information_schema.tables",
    "scope table": "SELECT * FROM agent.scope",
    "set_config": "SELECT set_config('courier.user_id', '2', false)",
    "quoted set_config": "SELECT \"set_config\"('a', 'b', false)",
    "qualified set_config": "SELECT pg_catalog.set_config('a', 'b', false)",
    "current_setting": "SELECT current_setting('search_path')",
    "sleep": "SELECT pg_sleep(30)",
    "file read": "SELECT pg_read_file('postgresql.conf')",
    "query_to_xml": "SELECT query_to_xml('select * from public.users', true, true, '')",
    "generate_series": "SELECT count(*) FROM generate_series(1, 100000000)",
    "dblink": "SELECT * FROM shipments WHERE dblink_connect('x') = 'OK'",
    "nextval": "SELECT nextval('public.shipments_id_seq')",
    "empty": "  ;  ",
    "not sql": "show me my shipments please",
}


@pytest.mark.parametrize("sql", ALLOWED)
def test_accepts_plain_selects_over_the_views(sql):
    checked = validate_select(sql, max_rows=50)
    assert checked.upper().startswith(("SELECT", "WITH"))


@pytest.mark.parametrize("sql", REJECTED.values(), ids=REJECTED.keys())
def test_rejects_everything_else(sql):
    with pytest.raises(UnsafeQueryError):
        validate_select(sql, max_rows=50)


def test_adds_a_row_cap_when_missing():
    assert validate_select("SELECT * FROM shipments", max_rows=50).endswith("LIMIT 51")


def test_lowers_a_cap_that_is_too_high_and_keeps_a_smaller_one():
    assert validate_select("SELECT * FROM shipments LIMIT 1000", max_rows=50).endswith("LIMIT 51")
    assert validate_select("SELECT * FROM shipments LIMIT 3", max_rows=50).endswith("LIMIT 3")


def test_caps_set_operations_by_wrapping_them():
    sql = validate_select(
        "SELECT tracking_number FROM shipments UNION SELECT tracking_number FROM tracking_events",
        max_rows=10,
    )
    assert sql.startswith("SELECT * FROM (") and sql.endswith("LIMIT 11")


def test_error_messages_help_the_sub_agent_fix_the_query():
    with pytest.raises(UnsafeQueryError, match="the only views are"):
        validate_select("SELECT * FROM users", max_rows=50)
    with pytest.raises(UnsafeQueryError, match=r"pg_sleep\(\) is not allowed"):
        validate_select("SELECT pg_sleep(1)", max_rows=50)
