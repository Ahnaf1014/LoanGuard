# LoanGuard coding style

## Python and Flask

- Keep imports grouped: standard/library dependencies, Flask, then local code.
- Give each feature one Flask `Blueprint` in `backend/routes/`.
- Use explicit function names that match a route's intent.
- Use docstrings/comments where a transaction, business rule, or relationship
  needs explanation; avoid comments that merely repeat code.
- Use `url_for()` for internal redirects and form actions where practical.
- Return `abort(404)` for a requested record that does not exist.

## SQL

- Use uppercase table names to match the existing schema.
- Use multiline SQL for readability and parameterize every user-derived value.
- Prefer joins for display data instead of one query per listed record.
- Keep transactions explicit: `commit` only after a complete write; `rollback`
  in the matching exception path.

## Templates

- Extend `base.html` for all feature pages.
- Use Bootstrap classes already present in the project.
- Keep Jinja loops and conditions presentation-only; query and validation logic
  belongs in route modules.
- Use POST for destructive state changes and display flash feedback afterward.
