USE LoanGuard;

-- Payment writes are the single event that changes a loan's outstanding
-- balance. Only confirmed Paid records affect the amount owed.
DROP TRIGGER IF EXISTS trg_update_loan_balance;

DELIMITER $$

CREATE TRIGGER trg_update_loan_balance
AFTER INSERT ON LOAN_PAYMENT
FOR EACH ROW
BEGIN

    IF NEW.payment_status = 'Paid' THEN

        -- This update occurs in the same transaction as the payment insert.
        UPDATE LOAN
        SET current_balance = current_balance - NEW.amount
        WHERE loan_id = NEW.loan_id;

    END IF;

END$$

DELIMITER ;
