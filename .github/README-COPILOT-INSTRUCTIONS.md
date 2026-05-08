Repository Copilot / PR scaffolding notes

What this PR scaffold contains:
- .github/PULL_REQUEST_TEMPLATE.md: a prioritized checklist derived from a code review
- .github/workflows/ci.yml: basic CI that runs backend pytest and builds frontend
- backend/tests/: minimal test scaffold to make CI useful and discoverable

Next recommended PRs (suggested order):
1. Remove default admin credentials and update README
2. Enforce SECRET_KEY in config and add tests
3. Make CSM SSL verify configurable and default to true
4. Fix db session leak and move DB writes off event loop
5. Add Alembic and disable create_all in production
6. Pin dependencies and add lockfile

How to run tests locally
- Backend tests: cd sop-platform && PYTHONPATH=backend python -m pytest -q backend/tests
