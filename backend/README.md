# Backend (Django) - Emoji Tic Tac Toe

This service exposes the REST API for the Tic Tac Toe game.

## Quick start

- Install dependencies:
  pip install -r requirements.txt

- Database:
  - By default falls back to SQLite at backend/db.sqlite3 when DB env vars are not set.
  - To use PostgreSQL, set the following env vars (see .env.example):
    - DB_HOST
    - DB_PORT (use 5001 in this environment unless overridden; defaults to 5432 if unset)
    - DB_NAME
    - DB_USER
    - DB_PASSWORD

See README_DB.md for full details.

## Apply database migrations

Ensure the Game table is created via Django migrations.

1) Export PostgreSQL env vars (recommended) or rely on SQLite fallback:
   - DB_HOST
   - DB_PORT=5001
   - DB_NAME
   - DB_USER
   - DB_PASSWORD

2) Run migrations:
   python manage.py migrate

You should see migration 0001_initial applied, creating the `api_game` table.

## Run the dev server

- Start server on port 3001:
  python manage.py runserver 0.0.0.0:3001

## Verify endpoints

- Health: GET http://localhost:3001/api/health/
  -> {"message": "Server is up!"}

- Create game: POST http://localhost:3001/api/games/
- Retrieve game: GET http://localhost:3001/api/games/{id}/
- Make move: POST http://localhost:3001/api/games/{id}/move/   body: {"index": 0-8}
- Reset game: POST http://localhost:3001/api/games/{id}/reset/

OpenAPI docs available at http://localhost:3001/docs

## Notes

- Requirements include psycopg2-binary for Postgres support.
- When running with a reverse proxy, CORS is enabled and forwarded headers are respected.
