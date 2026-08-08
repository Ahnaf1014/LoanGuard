# LoanGuard

LoanGuard is a Flask and MySQL loan-management system built around explicit,
parameterized SQL. It supports borrower records, loan applications, manager
decisions, credit assessments, portfolio metrics, and the underlying loan and
payment data model.

## Implemented workflows

- Dashboard totals for borrowers, applications, pending work, and requested value
- Borrower create, list, edit, and protected delete
- Loan-application creation with validated loan-officer assignment
- Application decisions with branch-manager attribution and timestamps
- Credit-assessment creation with validated analyst assignment
- MySQL views, stored procedures, constraints, and payment-balance triggers

The schema also models approved loans, loan subtypes, and repayments. Dedicated
web pages for those areas are not implemented yet.

## Technology

- Python 3.12+
- Flask 3
- PyMySQL
- MySQL 8.0+
- Jinja, Bootstrap 5, and plain JavaScript

## Project layout

```text
backend/
  app.py                 Flask application factory and entry point
  config.py              environment-backed configuration
  database/connection.py MySQL connection and transaction helpers
  routes/                 feature blueprints
  security.py             CSRF and browser security controls
  validation.py           shared server-side form validation
  templates/              Jinja pages
  static/                 CSS and JavaScript
database/
  schema.sql              tables, constraints, and indexes
  seed.sql                demonstration records
  views.sql               reporting view
  procedures.sql          status-filter procedure
  triggers.sql            loan/payment workflow protection
scripts/
  check_database.py       read-only configured-database health check
tests/                    standard-library unit tests
```

## Local setup

### 1. Create the Python environment

From the repository root on Windows:

```powershell
py -3.12 -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

If the `py` launcher is unavailable, select an installed Python 3.12+ executable
when creating the environment.

### 2. Configure environment variables

```powershell
Copy-Item .env.example backend/.env
```

Edit `backend/.env` for the local MySQL server. Generate a development secret,
for example:

```powershell
backend/.venv/Scripts/python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Never commit `backend/.env`; it is intentionally ignored.

### 3. Initialize MySQL

Create a database named `LoanGuard` with `utf8mb4`, then run these files against
that selected database in order:

1. `database/schema.sql`
2. `database/seed.sql`
3. `database/views.sql`
4. `database/procedures.sql`
5. `database/triggers.sql`

The SQL files do not hard-code a provider-specific database name. The active
MySQL connection determines the target database.

### 4. Run the application

```powershell
Set-Location backend
.venv/Scripts/python.exe app.py
```

Open <http://127.0.0.1:5000>.

## VS Code workspace

Open the repository root in VS Code. The shared workspace includes:

- the correct `backend/.venv` interpreter path;
- Flask debugging (`LoanGuard: Flask`);
- test, compile, dependency-install, and database-health tasks;
- SQLTools MySQL connection metadata without a stored password;
- formatter, linter, Jinja, SQL, YAML, and environment-file recommendations.

Run tasks from **Terminal → Run Task**. SQLTools prompts for the MySQL password
when connecting to `LoanGuard (Local MySQL)`.

## Validation

```powershell
backend/.venv/Scripts/python.exe -m unittest discover -v -s tests -p test_*.py
backend/.venv/Scripts/python.exe -m compileall -q backend tests
backend/.venv/Scripts/python.exe scripts/check_database.py
```

The database check is read-only. It verifies required tables, trigger versions,
staff-role relationships, decision metadata, and loan balances.

For a database created before the hardened constraints and triggers, back it up
and apply the one-time upgrade from the repository root:

```powershell
backend/.venv/Scripts/python.exe scripts/apply_sql.py --yes database/migrations/001_harden_data_integrity.sql database/triggers.sql
```

## Deployment

`render.yaml` and `Procfile` define a Gunicorn deployment. Configure all
`DB_*` values for a MySQL 8-compatible provider. Production also requires:

- `APP_ENV=production`
- a unique `SECRET_KEY`
- `SESSION_COOKIE_SECURE=true`
- `TRUST_PROXY=true` only when exactly one trusted hosting proxy fronts the app
- TLS database settings appropriate for the provider

Important: authentication and role-based authorization are not implemented.
Do not expose this application to untrusted users or real customer data until
those controls and an audit trail are added.

## Security characteristics

The current application provides parameterized SQL, transaction rollback,
server-side validation, CSRF protection, secure cookie defaults, restrictive
browser headers, POST-only deletion, role validation for workflow assignments,
and database constraints. These controls do not replace authentication or
authorization.

## License

No license has been selected. The repository's `LICENSE` file is intentionally
empty until the owner chooses licensing terms.
