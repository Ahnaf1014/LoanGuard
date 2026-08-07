# LoanGuard database memory

## Core relationships

- A borrower has many loan applications and phone numbers.
- A loan officer processes many applications.
- A branch manager may decide many applications; `manager_id` is optional until
  a decision exists.
- An application has many credit assessments and at most one loan.
- A credit analyst creates many assessments.
- A loan has many payments and exactly one subtype: personal, home, or business.

## Main tables

| Area | Tables |
|---|---|
| People | `BORROWER`, `BORROWER_PHONE`, `BANK_STAFF`, `BANK_STAFF_PHONE` |
| Decision workflow | `LOAN_APPLICATION`, `CREDIT_ASSESSMENT` |
| Lending | `LOAN`, `PERSONAL_LOAN`, `HOME_LOAN`, `BUSINESS_LOAN`, `LOAN_PAYMENT` |

## Important constraints

- Borrower NID and email are unique.
- Application amount and income must be positive.
- Application status is `Pending`, `Under Review`, `Approved`, or `Rejected`.
- Assessment risk/recommendation/probability are constrained by enums/checks.
- Loan application and loan number are unique in `LOAN`.
- Payment transaction references and `(loan_id, installment_no)` are unique.
- Deleting a borrower with applications is restricted; deleting an application
  cascades to its assessments.

## Database objects

- `vw_loan_application_summary`: descriptive application/report view.
- `sp_get_applications_by_status`: status-filtered application procedure.
- `trg_update_loan_balance`: subtracts a newly inserted Paid payment from the
  matching loan balance.

## Data access rule

Use PyMySQL `%s` placeholders and a parameter tuple. A write must either
`commit()` after success or `rollback()` after an exception, then close cursor
and connection.
