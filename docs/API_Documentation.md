# HTTP interface

LoanGuard currently provides server-rendered HTML endpoints, not a public JSON
API. State-changing endpoints accept form-encoded POST requests and require a
session-bound CSRF token.

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Dashboard |
| GET | `/borrowers` | List borrowers |
| GET, POST | `/borrowers/add` | Create borrower |
| GET, POST | `/borrowers/edit/<id>` | Edit borrower |
| POST | `/borrowers/delete/<id>` | Delete unreferenced borrower |
| GET | `/applications` | List applications |
| GET, POST | `/applications/add` | Create application |
| GET, POST | `/applications/edit/<id>` | Update status/manager decision |
| GET | `/assessments` | List assessments |
| GET, POST | `/assessments/add` | Create assessment |

Successful form writes use the POST/Redirect/GET pattern. Validation and
database errors are reported through flash messages.
