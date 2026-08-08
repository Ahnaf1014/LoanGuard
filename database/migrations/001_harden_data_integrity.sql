-- One-time upgrade for databases created before the hardened schema.
-- Apply this file once, then apply database/triggers.sql.

UPDATE LOAN_APPLICATION
SET manager_id = NULL,
    decision_date = NULL
WHERE application_status IN ('Pending', 'Under Review');

ALTER TABLE LOAN_APPLICATION
    MODIFY application_status ENUM (
        'Pending',
        'Under Review',
        'Approved',
        'Rejected'
    ) NOT NULL DEFAULT 'Pending',
    ADD CONSTRAINT chk_application_decision CHECK (
        (
            application_status IN ('Approved', 'Rejected')
            AND decision_date IS NOT NULL
        )
        OR (
            application_status IN ('Pending', 'Under Review')
            AND decision_date IS NULL
        )
    );

ALTER TABLE CREDIT_ASSESSMENT
    ADD CONSTRAINT chk_assessment_score CHECK (
        credit_score >= 0
        AND credit_score <= 850
    );

ALTER TABLE LOAN
    ADD CONSTRAINT chk_loan_installment CHECK (monthly_installment > 0),
    ADD CONSTRAINT chk_loan_balance CHECK (
        current_balance >= 0
        AND current_balance <= approved_amount
    ),
    ADD CONSTRAINT chk_loan_dates CHECK (due_date >= disbursement_date);

ALTER TABLE LOAN_PAYMENT
    ADD CONSTRAINT chk_payment_installment CHECK (installment_no > 0),
    ADD CONSTRAINT chk_payment_amount CHECK (amount > 0);
