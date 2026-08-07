USE LoanGuard;

DROP TRIGGER IF EXISTS trg_update_loan_balance;

DELIMITER $$

CREATE TRIGGER trg_update_loan_balance
AFTER INSERT ON LOAN_PAYMENT
FOR EACH ROW
BEGIN

    IF NEW.payment_status = 'Paid' THEN

        UPDATE LOAN
        SET current_balance = current_balance - NEW.amount
        WHERE loan_id = NEW.loan_id;

    END IF;

END$$

DELIMITER ;