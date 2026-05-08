# Copilot instructions for this repository

Purpose
- Short guide for Copilot sessions to quickly find build/run commands, architecture, and repo-specific conventions.

Build / run / test / lint commands

Backend (FastAPI, Python)
- Install deps: cd sop-platform/backend && pip3 install -r requirements.txt
- Run dev server: cd sop-platform/backend && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8888
- DB init (optional): psql -U postgres -c "CREATE DATABASE sop_platform;" && psql -U postgres -d sop_platform -f init.sql
- Env: copy and edit .env (config loaded via pydantic BaseSettings in app.config). App will create tables at startup via Base.metadata.create_all.
- Tests: No test framework or test scripts found in the repository. Do not assume test commands exist.
- Lint/format: No project linting tools configured. When adding changes, prefer adding black/flake8/isort config and npm lint scripts for frontend.

Frontend (Vue 3 + Vite)
- Install deps: cd sop-platform/frontend && npm install
- Dev server: cd sop-platform/frontend && npm run dev
- Build: npm run build
- Preview: npm run preview
- Tests/lint: No frontend test or lint scripts currently configured.

High-level architecture (big picture)
- Monorepo-like layout under `sop-platform/` with two main components:
  - backend/: FastAPI service (Python 3.8+) using SQLAlchemy, Pydantic (v2), python-dotenv, APScheduler for periodic syncs, and python-jose/bcrypt for JWT-based auth.
    - app/main.py: application entry; registers routers under /api, creates DB tables at startup, and starts AsyncIOScheduler jobs (hourly sync).
    - app/api/: route modules (assets.py, risks.py, intelligence.py, reports.py, auth.py).
    - app/services/: business logic and CSM API client (csm_client.py, sync_service.py).
    - app/models/: SQLAlchemy models (users, dashboard_stats, audit_logs, etc.).
    - app/config.py: pydantic BaseSettings; .env is used for overrides.
    - app/database.py: SQLAlchemy engine, SessionLocal, Base.
  - frontend/: Vue 3 + Vite SPA using Element Plus, Pinia, axios, and ECharts. The SPA calls backend APIs and expects backend on port 8888 (CORS enabled for all origins in dev).
- Data flow: backend periodically (and manually) syncs data from an external CSM platform via csm_client; synced data is stored in PostgreSQL and served to frontend through REST API endpoints.

Key conventions and repo-specific patterns
- Settings: Prefer pydantic-settings BaseSettings pattern with get_settings() cached via lru_cache. .env file is the source of environment overrides.
- DB lifecycle: Tables are created on app startup via Base.metadata.create_all(bind=engine) in FastAPI lifespan. SessionLocal is used per request; use get_db() dependency where applicable.
- Auth: JWT-based auth (SECRET_KEY in config). Passwords hashed with bcrypt; tokens via python-jose. auth routes live in app.api.auth and utilities in app.utils.auth.
- Scheduler: AsyncIOScheduler is started in app.main lifespan and uses an async sync_dashboard_data() function; keep asynchronous conventions when modifying sync logic.
- API root: All routers are included with prefix "/api". Swagger UI available at /docs when backend running.
- Default dev ports & credentials (documented in README): frontend http://localhost:3001, backend http://localhost:8888, default admin `admin` / `admin123` (change in production).
- Secrets: .env files present; do not commit secrets. app.config.Config points to .env by default.

AI / assistant files to consider
- CLAUDE.md exists at repo root with project notes and dev preferences; include its guidance in assistant workflows.
- No other assistant config files (.cursorrules, AGENTS.md, etc.) were found. If adding Copilot or other assistant rules, place them under .github/ or repo root and update this file.

Where to look first when editing
- backend/app/main.py: startup, scheduler, and router registration.
- backend/app/services/: sync logic and CSM client (integration points).
- backend/app/config.py and .env: environment-driven configuration.
- frontend/src/: views, api wrappers (axios), and stores (Pinia).

Minimal safety and review notes for Copilot suggestions
- Changes that touch config or .env should not print secrets or suggest committing .env files.
- When proposing DB schema changes, update migration plan (no migrations are configured now) and ensure backwards-compatible changes or add alembic if needed.
- When proposing adding tests or linters, add corresponding scripts to package.json (frontend) or a Makefile for common tasks.

If you update this file
- Keep it targeted: include commands and patterns actually present. Add test or lint commands only after they are added to the repo.

References incorporated
- sop-platform/README.md (startup, ports, default creds, API list)
- CLAUDE.md (developer preferences)

