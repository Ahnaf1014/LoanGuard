USE LoanGuard;

-- Reusable status filter for reporting tools. The input is VARCHAR because
-- callers may be different MySQL clients; the table enum remains authoritative.
DROP PROCEDURE IF EXISTS sp_get_applications_by_status;

DELIMITER $$

CREATE PROCEDURE sp_get_applications_by_status(
    IN p_status VARCHAR(20)
)
BEGIN

    SELECT
        application_id,
        borrower_id,
        loan_officer_id,
        requested_amount,
        application_status,
        application_date
    FROM LOAN_APPLICATION
    WHERE application_status = p_status
    ORDER BY application_date DESC;

END$$

DELIMITER ;
