# Backend (Django) - Emoji Tic Tac Toe

This service exposes the REST API for the Tic Tac Toe game.

## Quick start

- Install dependencies:
  pip install -r requirements.txt

- Database:
  - By default falls back to SQLite at backend/db.sqlite3 when DB env vars are not set.
  - To use PostgreSQL, set the following env vars (see .env.example):
    - DB_HOST
    - DB_PORT (5001 in this environment unless overridden; defaults to 5432 if unset)
    - DB_NAME
    - DB_USER
    - DB_PASSWORD

See README_DB.md for full details.

## Helpful commands

- Apply migrations:
  python manage.py migrate

- Run dev server:
  python manage.py runserver 0.0.0.0:3001

## Notes

- Requirements include psycopg2-binary for Postgres support.
- OpenAPI docs available at /docs when the server is running.
