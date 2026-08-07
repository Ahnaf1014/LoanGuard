# LoanGuard features

## Implemented

### Dashboard

Shows total borrowers, total applications, pending applications, and the sum of
requested application amounts.

### Borrower management

Lists borrowers and supports add, edit, and POST-only delete. MySQL uniqueness
constraints enforce NID and email rules; application foreign keys prevent a
borrower with history from being deleted.

### Loan applications

Lists applications with borrower names, creates an application assigned to a
loan officer, and changes the application status through the allowed enum.

### Credit assessments

Lists assessments with borrower and analyst names. The create flow selects an
application and a `CreditAnalyst`, validates risk/recommendation/value ranges,
then inserts a new assessment.

## Planned / schema-supported

- Branch-manager decision assignment and decision timestamps.
- Loan creation after approval.
- Personal, home, and business loan subtype creation.
- Payment recording and repayment/balance views.
- Authentication and role-based authorization.
- Search, pagination, reporting, tests, and API endpoints.
