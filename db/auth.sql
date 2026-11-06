-- Customer logins. Password hashes (Argon2) live outside "public" so the SQL sandbox can
-- never see them; the app reads them through auth.login_lookup only.
-- Run as a superuser after the roles exist: scripts/setup_db.py does this.

CREATE SCHEMA IF NOT EXISTS auth;
REVOKE ALL ON SCHEMA auth FROM PUBLIC;

CREATE TABLE IF NOT EXISTS auth.credentials (
    user_id       integer     PRIMARY KEY REFERENCES public.users (id) ON DELETE CASCADE,
    password_hash text        NOT NULL,
    updated_at    timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE VIEW auth.login_lookup AS
SELECT
    u.id                       AS user_id,
    u.username,
    btrim(u.email, E' \t\r\n') AS email,
    u.full_name,
    c.password_hash
FROM public.users AS u
JOIN auth.credentials AS c ON c.user_id = u.id;

GRANT USAGE ON SCHEMA auth TO courier_app;
GRANT SELECT ON auth.login_lookup TO courier_app;
