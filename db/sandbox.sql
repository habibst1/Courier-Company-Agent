-- Sandbox for LLM-written SQL.
--
-- The SQL sub-agent's queries run as courier_agent, which can only SELECT from the views
-- in schema "agent". Every view joins agent.active_scope, which returns the scope row that
-- the app bound to *this* backend process (pg_backend_pid()). The app binds that row from a
-- separate courier_app connection right before running a query and deletes it right after.
--
-- courier_agent has no privileges on agent.scope or on any table in "public", so even a query
-- that slipped past the app's SQL checks could not widen its own scope (set_config does not help:
-- the scope lives in a table, keyed by a PID the session cannot change) or read other rows.
--
-- Run as a superuser after the roles exist: scripts/setup_db.py does both.

CREATE SCHEMA IF NOT EXISTS agent;
REVOKE ALL ON SCHEMA agent FROM PUBLIC;

CREATE TABLE IF NOT EXISTS agent.scope (
    pid             integer     PRIMARY KEY,
    mode            text        NOT NULL CHECK (mode IN ('customer', 'recipient')),
    user_id         integer,
    tracking_number text,
    bound_at        timestamptz NOT NULL DEFAULT clock_timestamp(),
    CHECK (
        (mode = 'customer'  AND user_id IS NOT NULL AND tracking_number IS NULL) OR
        (mode = 'recipient' AND tracking_number IS NOT NULL AND user_id IS NULL)
    )
);
COMMENT ON TABLE agent.scope IS
    'Who the sandbox connection with this backend PID may see. Written only by courier_app.';

DROP VIEW IF EXISTS agent.my_account, agent.my_addresses, agent.tracking_events, agent.shipments,
    agent.active_scope;

-- The scope bound to the current backend. A two-minute window guards against stale rows.
CREATE VIEW agent.active_scope AS
SELECT sc.mode, sc.user_id, sc.tracking_number
FROM agent.scope AS sc
WHERE sc.pid = pg_backend_pid()
  AND sc.bound_at > now() - interval '2 minutes';

-- Customers see the shipments they sent; recipients see the one shipment they track.
-- Street-level address details are only shown to customers.
CREATE VIEW agent.shipments WITH (security_barrier = true) AS
SELECT
    s.tracking_number,
    s.status,
    s.weight                AS weight_kg,
    s.created_at,
    s.expected_delivery_date,
    o.city                  AS origin_city,
    o.state                 AS origin_state,
    o.country               AS origin_country,
    d.city                  AS destination_city,
    d.state                 AS destination_state,
    d.country               AS destination_country,
    CASE WHEN sc.mode = 'customer' THEN o.address_line END AS origin_address_line,
    CASE WHEN sc.mode = 'customer' THEN o.postal_code  END AS origin_postal_code,
    CASE WHEN sc.mode = 'customer' THEN d.address_line END AS destination_address_line,
    CASE WHEN sc.mode = 'customer' THEN d.postal_code  END AS destination_postal_code
FROM public.shipments AS s
JOIN agent.active_scope AS sc
  ON (sc.mode = 'customer'  AND s.user_id = sc.user_id)
  OR (sc.mode = 'recipient' AND s.tracking_number = sc.tracking_number)
LEFT JOIN public.addresses AS o ON o.id = s.origin_address_id
LEFT JOIN public.addresses AS d ON d.id = s.destination_address_id;

CREATE VIEW agent.tracking_events WITH (security_barrier = true) AS
SELECT
    s.tracking_number,
    t.status,
    t.location_city,
    t.location_details,
    t.scanned_at
FROM public.tracking_updates AS t
JOIN public.shipments AS s ON s.id = t.shipment_id
JOIN agent.active_scope AS sc
  ON (sc.mode = 'customer'  AND s.user_id = sc.user_id)
  OR (sc.mode = 'recipient' AND s.tracking_number = sc.tracking_number);

CREATE VIEW agent.my_addresses WITH (security_barrier = true) AS
SELECT a.address_line, a.city, a.state, a.country, a.postal_code, a.created_at
FROM public.addresses AS a
JOIN agent.active_scope AS sc ON sc.mode = 'customer' AND a.user_id = sc.user_id;

CREATE VIEW agent.my_account WITH (security_barrier = true) AS
SELECT
    u.username,
    u.full_name,
    btrim(u.email, E' \t\r\n') AS email,
    btrim(u.phone, E' \t\r\n') AS phone,
    u.created_at               AS member_since
FROM public.users AS u
JOIN agent.active_scope AS sc ON sc.mode = 'customer' AND u.id = sc.user_id;

COMMENT ON VIEW agent.shipments IS 'Shipments visible in this chat.';
COMMENT ON VIEW agent.tracking_events IS 'Scan history of the shipments visible in this chat.';
COMMENT ON VIEW agent.my_addresses IS 'The signed-in customer''s saved addresses (empty for recipients).';
COMMENT ON VIEW agent.my_account IS 'The signed-in customer''s profile (empty for recipients).';

-- Privileges: the sandbox reads views only; the app may bind and clear scopes.
GRANT USAGE ON SCHEMA agent TO courier_agent, courier_app;
GRANT SELECT ON agent.shipments, agent.tracking_events, agent.my_addresses, agent.my_account
    TO courier_agent;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent.scope TO courier_app;
