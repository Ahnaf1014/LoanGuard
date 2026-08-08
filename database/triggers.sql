-- Loan and payment workflow protections. Run this file after seed.sql so the
-- seed's pre-calculated balances are not adjusted a second time.

DROP TRIGGER IF EXISTS trg_validate_loan_application;
DROP TRIGGER IF EXISTS trg_validate_loan_application_update;
DROP TRIGGER IF EXISTS trg_protect_funded_application;
DROP TRIGGER IF EXISTS trg_validate_payment_insert;
DROP TRIGGER IF EXISTS trg_update_loan_balance_insert;
DROP TRIGGER IF EXISTS trg_validate_payment_update;
DROP TRIGGER IF EXISTS trg_update_loan_balance_update;
DROP TRIGGER IF EXISTS trg_update_loan_balance_delete;
-- Remove the legacy trigger name when upgrading an existing database.
DROP TRIGGER IF EXISTS trg_update_loan_balance;

DELIMITER $$

CREATE TRIGGER trg_validate_loan_application
BEFORE INSERT ON LOAN
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM LOAN_APPLICATION
        WHERE application_id = NEW.application_id
          AND application_status = 'Approved'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A loan requires an approved application';
    END IF;
END$$

CREATE TRIGGER trg_validate_loan_application_update
BEFORE UPDATE ON LOAN
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM LOAN_APPLICATION
        WHERE application_id = NEW.application_id
          AND application_status = 'Approved'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A loan requires an approved application';
    END IF;
END$$

CREATE TRIGGER trg_protect_funded_application
BEFORE UPDATE ON LOAN_APPLICATION
FOR EACH ROW
BEGIN
    IF NEW.application_status <> 'Approved'
       AND EXISTS (
           SELECT 1
           FROM LOAN
           WHERE application_id = NEW.application_id
       ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'A funded application must remain approved';
    END IF;
END$$

CREATE TRIGGER trg_validate_payment_insert
BEFORE INSERT ON LOAN_PAYMENT
FOR EACH ROW
BEGIN
    DECLARE available_balance DECIMAL(12, 2);

    IF NEW.payment_status = 'Paid' THEN
        SELECT current_balance
        INTO available_balance
        FROM LOAN
        WHERE loan_id = NEW.loan_id;

        IF NEW.amount > available_balance THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Paid amount exceeds the current loan balance';
        END IF;
    END IF;
END$$

CREATE TRIGGER trg_update_loan_balance_insert
AFTER INSERT ON LOAN_PAYMENT
FOR EACH ROW
BEGIN
    IF NEW.payment_status = 'Paid' THEN
        UPDATE LOAN
        SET current_balance = current_balance - NEW.amount
        WHERE loan_id = NEW.loan_id;
    END IF;
END$$

CREATE TRIGGER trg_validate_payment_update
BEFORE UPDATE ON LOAN_PAYMENT
FOR EACH ROW
BEGIN
    DECLARE available_balance DECIMAL(12, 2);

    IF NEW.loan_id <> OLD.loan_id THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'An existing payment cannot be moved to another loan';
    END IF;

    IF NEW.payment_status = 'Paid' THEN
        SELECT current_balance
            + CASE WHEN OLD.payment_status = 'Paid' THEN OLD.amount ELSE 0 END
        INTO available_balance
        FROM LOAN
        WHERE loan_id = NEW.loan_id;

        IF NEW.amount > available_balance THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Paid amount exceeds the current loan balance';
        END IF;
    END IF;
END$$

CREATE TRIGGER trg_update_loan_balance_update
AFTER UPDATE ON LOAN_PAYMENT
FOR EACH ROW
BEGIN
    UPDATE LOAN
    SET current_balance = current_balance
        + CASE WHEN OLD.payment_status = 'Paid' THEN OLD.amount ELSE 0 END
        - CASE WHEN NEW.payment_status = 'Paid' THEN NEW.amount ELSE 0 END
    WHERE loan_id = NEW.loan_id;
END$$

CREATE TRIGGER trg_update_loan_balance_delete
AFTER DELETE ON LOAN_PAYMENT
FOR EACH ROW
BEGIN
    IF OLD.payment_status = 'Paid' THEN
        UPDATE LOAN
        SET current_balance = current_balance + OLD.amount
        WHERE loan_id = OLD.loan_id;
    END IF;
END$$

DELIMITER ;
