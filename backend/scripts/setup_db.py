"""Prepare PostgreSQL for the CourierTrack backend.

What it does, in order (safe to run again):
  1. Loads db/schema.sql and db/seed.sql, but only when public.shipments doesn't exist yet.
  2. Creates or updates the roles named in AGENT_DATABASE_URL and APP_DATABASE_URL.
  3. Applies db/sandbox.sql, db/auth.sql and db/checkpoints.sql.
  4. Gives every customer without a login the DEMO_PASSWORD (--reset-passwords: everyone).

Usage, from backend/ with the virtualenv active:
    python scripts/setup_db.py [--reset-passwords]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import psycopg
from argon2 import PasswordHasher
from psycopg import sql
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BACKEND_DIR.parent / "db"

AGENT_ROLE = "courier_agent"
APP_ROLE = "courier_app"


class SetupSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    admin_database_url: SecretStr
    agent_database_url: SecretStr
    app_database_url: SecretStr
    demo_password: SecretStr


def role_credentials(url: SecretStr, expected_role: str) -> str:
    parts = urlsplit(url.get_secret_value())
    if unquote(parts.username or "") != expected_role:
        sys.exit(f"The URL for {expected_role} must use the user name {expected_role!r}.")
    password = unquote(parts.password or "")
    if len(password) < 16:
        sys.exit(f"Use a password of at least 16 characters for {expected_role}.")
    return password


def database_name(url: SecretStr) -> str:
    return urlsplit(url.get_secret_value()).path.lstrip("/")


def run_file(admin_url: str, name: str) -> None:
    # A fresh connection per file: pg_dump output empties search_path for its session.
    with psycopg.connect(admin_url, autocommit=True) as conn:
        conn.execute((DB_DIR / name).read_text(encoding="utf-8"))
    print(f"  applied db/{name}")


def ensure_role(conn: psycopg.Connection, role: str, password: str, database: str) -> None:
    exists = conn.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (role,)).fetchone()
    verb = "ALTER" if exists else "CREATE"
    conn.execute(
        sql.SQL(
            "{} ROLE {} LOGIN PASSWORD {} "
            "NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS"
        ).format(sql.SQL(verb), sql.Identifier(role), sql.Literal(password))
    )
    conn.execute(
        sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
            sql.Identifier(database), sql.Identifier(role)
        )
    )
    print(f"  {verb.lower()}d role {role}")


def set_role_options(conn: psycopg.Connection, role: str, database: str, options: dict) -> None:
    for name, value in options.items():
        conn.execute(
            sql.SQL("ALTER ROLE {} IN DATABASE {} SET {} = {}").format(
                sql.Identifier(role),
                sql.Identifier(database),
                sql.Identifier(name),
                sql.Literal(value),
            )
        )


def seed_demo_passwords(admin_url: str, password: str, reset: bool) -> int:
    hasher = PasswordHasher()
    with psycopg.connect(admin_url, autocommit=True) as conn:
        query = "SELECT id FROM public.users"
        if not reset:
            query += " WHERE id NOT IN (SELECT user_id FROM auth.credentials)"
        user_ids = [row[0] for row in conn.execute(query)]
        for user_id in user_ids:
            conn.execute(
                "INSERT INTO auth.credentials (user_id, password_hash) VALUES (%s, %s) "
                "ON CONFLICT (user_id) DO UPDATE "
                "SET password_hash = EXCLUDED.password_hash, updated_at = now()",
                (user_id, hasher.hash(password)),
            )
    return len(user_ids)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--reset-passwords",
        action="store_true",
        help="give every customer the current DEMO_PASSWORD, not only those without a login",
    )
    args = parser.parse_args()

    settings = SetupSettings()
    admin_url = settings.admin_database_url.get_secret_value()
    database = database_name(settings.admin_database_url)
    agent_password = role_credentials(settings.agent_database_url, AGENT_ROLE)
    app_password = role_credentials(settings.app_database_url, APP_ROLE)
    for url in (settings.agent_database_url, settings.app_database_url):
        if database_name(url) != database:
            sys.exit("ADMIN_, AGENT_ and APP_DATABASE_URL must point at the same database.")

    print(f"Preparing database {database!r}")
    with psycopg.connect(admin_url, autocommit=True) as conn:
        has_tables = conn.execute("SELECT to_regclass('public.shipments')").fetchone()[0]
    if has_tables:
        print("  tables already exist; schema.sql and seed.sql skipped")
    else:
        run_file(admin_url, "schema.sql")
        run_file(admin_url, "seed.sql")

    with psycopg.connect(admin_url, autocommit=True) as conn:
        ensure_role(conn, AGENT_ROLE, agent_password, database)
        ensure_role(conn, APP_ROLE, app_password, database)
        # Guards on every sandbox session. The app also opens each query READ ONLY.
        set_role_options(
            conn,
            AGENT_ROLE,
            database,
            {
                "search_path": "agent",
                "default_transaction_read_only": "on",
                "statement_timeout": "5s",
                "idle_in_transaction_session_timeout": "15s",
                "lc_messages": "C",  # English errors, which the SQL sub-agent reads to fix queries
            },
        )
        set_role_options(conn, APP_ROLE, database, {"search_path": "checkpoints"})

    for name in ("sandbox.sql", "auth.sql", "checkpoints.sql"):
        run_file(admin_url, name)

    count = seed_demo_passwords(
        admin_url, settings.demo_password.get_secret_value(), args.reset_passwords
    )
    print(f"  demo password set for {count} customer(s)")
    print(
        "Done. Customers sign in with their username (e.g. habib_bencheikhali) and DEMO_PASSWORD."
    )


if __name__ == "__main__":
    main()
