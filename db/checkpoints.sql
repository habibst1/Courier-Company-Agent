-- Conversation memory. LangGraph's AsyncPostgresSaver creates its tables here on startup
-- (courier_app's search_path points at this schema; scripts/setup_db.py sets it).

CREATE SCHEMA IF NOT EXISTS checkpoints AUTHORIZATION courier_app;
REVOKE ALL ON SCHEMA checkpoints FROM PUBLIC;
