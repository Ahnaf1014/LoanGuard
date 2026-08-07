# LoanGuard common mistakes

- Do not add SQLAlchemy or another ORM; raw PyMySQL SQL is a project constraint.
- Do not concatenate form values into SQL strings. Use `%s` placeholders.
- Do not forget `commit()` after a successful insert/update/delete or
  `rollback()` after a failed write.
- Do not return early while leaving a cursor or connection open.
- Do not make destructive actions GET routes; borrower deletion is POST-only.
- Do not trust HTML `required`, `min`, or select values alone. Validate values in
  the route and rely on database constraints as a final safeguard.
- Do not change enum values in templates without matching the schema and route
  validation.
- Do not create a loan for a non-approved application; the schema permits a
  one-to-one loan relationship but the workflow must enforce approval.
- Do not commit `.env`, real credentials, or real password data. Seed
  `password_hash` values are demonstration data, not production authentication.
- Do not confuse `backend/database/` (runtime connector code) with
  repository-level `database/` (MySQL scripts).
