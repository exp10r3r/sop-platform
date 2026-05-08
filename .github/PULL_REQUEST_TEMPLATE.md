## PR checklist

Use this template to create a focused PR that addresses the code-review findings.

Checklist (mark each item in the PR description when completed):

- [ ] Remove default admin credentials (remove INSERT in backend/init.sql and README references)
- [ ] Require/validate SECRET_KEY in production (backend/app/config.py)
- [ ] Make CSM SSL verification configurable and default to true (backend/app/services/csm_client.py + config)
- [ ] Ensure DB sessions closed in finally blocks and avoid leaking connections (backend/app/main.py)
- [ ] Run DB writes off the event loop (use run_in_threadpool or migrate to async SQLAlchemy)
- [ ] Lock down CORS to configured ALLOWED_ORIGINS (backend/app/main.py + config)
- [ ] Add Alembic migrations and disable create_all() in production
- [ ] Pin backend dependencies / add lockfile or constraints
- [ ] Add unit/integration tests (backend/tests/...) and CI workflow
- [ ] Add a security review for logging and secret handling

PR description guidelines
- Brief summary of the change
- Files changed and why
- How to test locally (commands)
- Which checklist items this PR completes

Reviewer guidance
- Verify secrets are not introduced in code or commits
- Verify tests pass on CI
- Confirm migration strategy and rollout plan for DB schema changes
