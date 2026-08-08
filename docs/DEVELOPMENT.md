# Development guide

## Architecture rules

- Keep HTTP parsing and responses in `backend/web/`.
- Keep business rules and database-error translation in `backend/services/`.
- Keep parameterized SQL in `backend/database/repositories/`.
- Keep cross-cutting authentication, security, exceptions, and validation in
  `backend/core/`.
- Preserve raw PyMySQL access; do not introduce an ORM.

## Python and Flask

- Group standard-library, third-party, and local imports.
- Give each feature one Flask `Blueprint` and use explicit route names.
- Use `url_for()` for internal links, redirects, and form actions.
- Return HTTP 404 for missing records.
- Comment business rules and transaction boundaries, not obvious syntax.
- Do not leak PyMySQL exceptions into web controllers; services translate them
  into application exceptions.

## SQL and transactions

- Parameterize every user-derived value with `%s` placeholders.
- Prefer joins over per-row queries.
- Use `cursor_scope()` for deterministic commit, rollback, and cleanup.
- Treat database constraints as the final data-integrity boundary.
- Keep schema enums, service validation, and form options synchronized.
- Never create a loan for an application that is not approved.

## Templates and security

- Extend `layouts/base.html` from feature templates.
- Keep Jinja presentation-only; validation and queries belong in lower layers.
- Use POST for state changes and POST/Redirect/GET after successful writes.
- Include `_csrf_token` in every state-changing form.
- Validate on the server even when HTML fields use `required`, `min`, or
  constrained options.
- Never commit `.env`, credentials, backups, or real password data.

## Verification

```powershell
backend/.venv/Scripts/python.exe -m unittest discover -v -s tests
backend/.venv/Scripts/python.exe -m compileall -q backend tests scripts
backend/.venv/Scripts/python.exe scripts/check_database.py
backend/.venv/Scripts/python.exe scripts/smoke_web.py
```
