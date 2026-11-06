-- Optional: move every demo date forward so the newest shipment was created two days ago.
-- The seed data dates from August-September 2025, so without this the assistant correctly
-- reports every undelivered package as months late. Safe to run more than once.
--
--   psql -U postgres -d courier_db -f db/refresh_demo_dates.sql

BEGIN;

CREATE TEMP TABLE demo_shift ON COMMIT DROP AS
SELECT (now() - interval '2 days') - max(created_at) AS delta FROM public.shipments;

UPDATE public.shipments
SET created_at             = created_at + (SELECT delta FROM demo_shift),
    expected_delivery_date = (expected_delivery_date + (SELECT delta FROM demo_shift))::date;

UPDATE public.tracking_updates
SET scanned_at = scanned_at + (SELECT delta FROM demo_shift);

UPDATE public.addresses SET created_at = created_at + (SELECT delta FROM demo_shift);
UPDATE public.users     SET created_at = created_at + (SELECT delta FROM demo_shift);

COMMIT;
