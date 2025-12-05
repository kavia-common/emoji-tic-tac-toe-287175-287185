# emoji-tic-tac-toe-287175-287185

- Backend database configuration: see backend/README_DB.md
- PostgreSQL is used when DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD are set (port 5001 by default in this environment); otherwise backend falls back to SQLite.
- Example environment file for backend is provided at backend/.env.example (do not commit real secrets).

Frontend integration:
- Ensure EXPO_PUBLIC_BACKEND_URL is set to http://localhost:3001/api in the frontend env so the React Native app can call the backend:
  EXPO_PUBLIC_BACKEND_URL=http://localhost:3001/api
- Endpoints used:
  - GET  /health/
  - POST /games/
  - GET  /games/{id}/
  - POST /games/{id}/move/
  - POST /games/{id}/reset/