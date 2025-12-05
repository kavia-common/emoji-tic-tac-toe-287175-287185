# Backend Database Configuration

This Django backend supports PostgreSQL via environment variables with a fallback to SQLite for local/dev.

## PostgreSQL (default when env vars provided)

Set the following environment variables:

- DB_HOST
- DB_PORT (defaults to 5432 if not provided; this environment uses 5001)
- DB_NAME
- DB_USER
- DB_PASSWORD

When these are present, Django uses `django.db.backends.postgresql`.

Example `.env` (see `.env.example`):

```
DB_HOST=localhost
DB_PORT=5001
DB_NAME=emoji_ttt
DB_USER=postgres
DB_PASSWORD=postgres_password
```

## SQLite (fallback)

If the PG env vars are not set, Django automatically falls back to SQLite at:

```
<project>/backend/db.sqlite3
```

No additional configuration is required for the fallback.

## Notes

- The project requirements include `psycopg2-binary` to enable PostgreSQL connections.
- The database container is expected to be available on port `5001`.
- No secrets are committed; ensure these env vars are set by the orchestrator.
