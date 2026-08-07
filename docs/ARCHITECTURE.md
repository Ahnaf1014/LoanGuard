# LoanGuard architecture and feature map

LoanGuard separates the web interface from database setup so each concern can
be changed without mixing UI, request handling, and schema definitions.

```
backend/app.py
├── config.py                 application and MySQL settings
├── database/connection.py    connection factory used by all routes
├── routes/
│   ├── dashboard.py          portfolio totals and home page
│   ├── borrower.py           borrower list, create, edit, delete
│   └── application.py        application list, create, status review
└── templates/                Bootstrap/Jinja pages for the routes above

database/
├── schema.sql                tables, keys, constraints, and indexes
├── seed.sql                  demonstration staff, borrowers, and loan data
├── views.sql                 reusable report-oriented queries
├── procedures.sql            reusable MySQL procedure
└── triggers.sql              automatic loan-balance maintenance
```

## Request flow

1. `app.py` registers one Flask blueprint for each feature.
2. A route uses `database/connection.py` to open a MySQL transaction.
3. The route executes parameterized SQL, commits successful writes, or rolls
   back failed writes.
4. The route renders the matching template or redirects to the feature list.

## Where to add a feature

Create a focused module in `backend/routes/`, add its templates under
`backend/templates/`, then register its blueprint in `backend/app.py`. Keep
database definitions and database-only logic in `database/`; run those files
in the order documented in the README.

## Local configuration

Copy `.env.example` to `.env`, set the MySQL credentials, initialize MySQL
with the database scripts, and then start `backend/app.py`. Never commit `.env`.
