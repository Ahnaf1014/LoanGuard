# LoanGuard architecture

```
Browser
  → Flask blueprint route
  → PyMySQL connection and parameterized SQL
  → MySQL tables / views / procedures / triggers
  → route context or flash message
  → Jinja template
  → Browser
```

## Backend layout

- `backend/app.py`: creates Flask and registers every feature blueprint.
- `backend/config.py`: reads Flask and MySQL settings from environment values.
- `backend/database/connection.py`: creates transactional `DictCursor`
  connections.
- `backend/routes/`: one module per user-facing feature.
- `backend/templates/`: base layout and corresponding feature pages.

## Feature ownership

| Blueprint | Route module | Templates | Responsibility |
|---|---|---|---|
| dashboard | `dashboard.py` | `dashboard.html` | Portfolio totals |
| borrower | `borrower.py` | borrower add/edit/list pages | Borrower records |
| application | `application.py` | application add/edit/list pages | Loan requests and status |
| assessment | `assessment.py` | assessment add/list pages | Analyst evaluations |

## Database layout

Repository-level `database/` contains deployable MySQL scripts. It is separate
from `backend/database/`, whose only responsibility is runtime connections.
