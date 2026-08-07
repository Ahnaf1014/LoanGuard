USE LoanGuard;

-- Read model for reports and application-list style screens. It deliberately
-- exposes descriptive borrower and officer names rather than only foreign keys.
-- =====================================================
-- VIEW: Loan Application Summary
-- =====================================================
DROP VIEW IF EXISTS vw_loan_application_summary;

CREATE VIEW vw_loan_application_summary AS
SELECT
    la.application_id,
    CONCAT(b.first_name, ' ', b.last_name) AS borrower_name,
    CONCAT(lo.first_name, ' ', lo.last_name) AS loan_officer,
    la.requested_amount,
    la.loan_purpose,
    la.monthly_income,
    la.application_status,
    la.application_date
FROM
    LOAN_APPLICATION la
    JOIN BORROWER b ON la.borrower_id = b.borrower_id
    JOIN BANK_STAFF lo ON la.loan_officer_id = lo.staff_id;
