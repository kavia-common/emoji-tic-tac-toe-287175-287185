# Apply Django Migrations

This project already includes migration `api/migrations/0001_initial.py` which creates the `Game` table.

Steps:

1) Ensure PostgreSQL variables are set (preferred)
   - DB_HOST
   - DB_PORT=5001
   - DB_NAME
   - DB_USER
   - DB_PASSWORD

   If not set, the backend will fall back to SQLite (backend/db.sqlite3).

2) Install deps:
   pip install -r requirements.txt

3) Apply migrations:
   python manage.py migrate

4) Verify tables:
   - Django will report that `api.0001_initial` has been applied.

Troubleshooting:
- If connection fails, verify DB_HOST reachability and that DB_PORT matches the Postgres container (5001 in this environment).
- Ensure psycopg2-binary is installed (already in requirements.txt).
