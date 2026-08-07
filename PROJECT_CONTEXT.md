# LoanGuard project context

## Purpose

LoanGuard is an automated loan decision-support system for a DBMS course. It
helps bank staff maintain borrower records, process applications, record credit
assessments, manage approved loans, and track repayments. It supports human
decisions; it does not automatically approve a loan.

## Technical constraints

- Backend: Python, Flask, PyMySQL, Jinja2, Bootstrap.
- Database: MySQL 8.0+.
- Persistence: raw, parameterized SQL only. Do not introduce an ORM.
- Configuration: environment variables loaded from `.env`; `.env` is ignored.
- Database setup order: schema, seed, views, procedures, triggers.

## Current implementation boundary

Implemented web modules are dashboard reporting, borrower management, loan
application management, and credit-assessment entry/listing. The schema also
supports loan, loan subtype, payment, and manager-decision workflows, but those
do not yet have dedicated Flask route/template modules.

## Preservation rule

Keep the existing Flask blueprint → raw SQL → Jinja-template architecture. Use
the schema constraints and foreign keys as the source of truth for data rules.
