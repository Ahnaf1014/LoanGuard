# LoanGuard architecture

LoanGuard is a Flask and MySQL decision-support system for bank staff. It uses
raw parameterized SQL by design and supports human loan decisions; it does not
automatically approve applications.

```text
Browser
  -> Flask core security / authentication controls
  -> Web feature blueprint
  -> Service and validation layer
  -> Repository and transaction-scoped PyMySQL cursor
  -> MySQL constraints / views / procedures / triggers
  -> Jinja response or POST/Redirect/GET feedback
```

## Backend responsibilities

- `backend/app.py`: application factory, configuration, proxy handling, and
  blueprint registration.
- `backend/config.py`: environment-backed Flask and MySQL settings.
- `backend/core/`: authentication, authorization, security, exceptions, and
  reusable validation primitives.
- `backend/database/connection.py`: TLS-capable connections and deterministic
  transaction/cursor cleanup.
- `backend/database/repositories/`: raw parameterized SQL data access.
- `backend/services/`: business rules and workflow coordination.
- `backend/web/`: one presentation blueprint per user-facing feature.
- `backend/templates/`: presentation-only Jinja pages.

## Feature ownership

| Blueprint | Module | Responsibility |
|---|---|---|
| `dashboard` | `web/dashboard.py` | Portfolio totals |
| `borrower` | `web/borrower.py` | Borrower CRUD |
| `application` | `web/application.py` | Applications and manager decisions |
| `assessment` | `web/assessment.py` | Analyst assessments |

Repository-level `database/` owns deployable MySQL definitions. It is separate
from `backend/database/`, which owns runtime connectivity only.

## Architectural boundary

This project intentionally uses raw parameterized SQL rather than an ORM.
Login endpoints, authorization rollout, payments UI, loan origination UI,
pagination, and audit logging remain future work. Authorization and audit
logging are required before production use.

## Current scope

The web application implements dashboards, borrower management, applications,
manager decisions, and credit assessments. The database also models loans,
personal/home/business subtypes, and payments; those web workflows remain
future work.
