# LoanGuard architecture

```text
Browser
  -> Flask application-wide security controls
  -> Feature blueprint
  -> Shared validation
  -> Transaction-scoped PyMySQL cursor
  -> MySQL constraints / views / procedures / triggers
  -> Jinja response or POST/Redirect/GET feedback
```

## Backend responsibilities

- `backend/app.py`: application factory, configuration, proxy handling, and
  blueprint registration.
- `backend/config.py`: environment-backed Flask and MySQL settings.
- `backend/security.py`: CSRF validation and browser response headers.
- `backend/validation.py`: reusable input parsing and bounds checks.
- `backend/database/connection.py`: TLS-capable connections and deterministic
  transaction/cursor cleanup.
- `backend/routes/`: one blueprint per user-facing feature.
- `backend/templates/`: presentation-only Jinja pages.

## Feature ownership

| Blueprint | Module | Responsibility |
|---|---|---|
| `dashboard` | `routes/dashboard.py` | Portfolio totals |
| `borrower` | `routes/borrower.py` | Borrower CRUD |
| `application` | `routes/application.py` | Applications and manager decisions |
| `assessment` | `routes/assessment.py` | Analyst assessments |

Repository-level `database/` owns deployable MySQL definitions. It is separate
from `backend/database/`, which owns runtime connectivity only.

## Architectural boundary

This project intentionally uses raw parameterized SQL rather than an ORM.
Authentication, authorization, payments UI, loan origination UI, pagination,
and audit logging remain future modules. Authentication and audit logging are
required before production use.
