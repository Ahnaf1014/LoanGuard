"""Transactional integration checks for critical database triggers."""

import sys
from decimal import Decimal
from pathlib import Path

import pymysql

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from database.connection import get_connection  # noqa: E402


def _expect_database_rejection(cursor, statement, parameters):
    try:
        cursor.execute(statement, parameters)
    except pymysql.MySQLError:
        return
    raise AssertionError("The database accepted an operation that should be rejected")


def main():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT p.payment_id, p.amount, l.loan_id, l.current_balance
                FROM LOAN_PAYMENT AS p
                JOIN LOAN AS l ON p.loan_id = l.loan_id
                WHERE p.payment_status = 'Pending' AND p.amount <= l.current_balance
                ORDER BY p.payment_id
                LIMIT 1
                FOR UPDATE
                """
            )
            payment = cursor.fetchone()
            if payment is None:
                raise AssertionError(
                    "A pending seed payment is required for this check"
                )

            cursor.execute(
                "UPDATE LOAN_PAYMENT SET payment_status = 'Paid' WHERE payment_id = %s",
                (payment["payment_id"],),
            )
            cursor.execute(
                "SELECT current_balance FROM LOAN WHERE loan_id = %s",
                (payment["loan_id"],),
            )
            updated_balance = cursor.fetchone()["current_balance"]
            expected_balance = payment["current_balance"] - payment["amount"]
            if updated_balance != expected_balance:
                raise AssertionError("Paid status did not update the loan balance")
        connection.rollback()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT loan_id, current_balance
                FROM LOAN
                ORDER BY loan_id
                LIMIT 1
                FOR UPDATE
                """
            )
            loan = cursor.fetchone()
            cursor.execute(
                """
                SELECT COALESCE(MAX(installment_no), 0) + 1000 AS installment_no
                FROM LOAN_PAYMENT
                WHERE loan_id = %s
                """,
                (loan["loan_id"],),
            )
            installment_no = cursor.fetchone()["installment_no"]
            _expect_database_rejection(
                cursor,
                """
                INSERT INTO LOAN_PAYMENT (
                    loan_id,
                    installment_no,
                    payment_date,
                    amount,
                    payment_method,
                    transaction_reference,
                    payment_status
                )
                VALUES (%s, %s, CURRENT_DATE, %s, 'Cash', %s, 'Paid')
                """,
                (
                    loan["loan_id"],
                    installment_no,
                    loan["current_balance"] + Decimal("0.01"),
                    "LG-ROLLBACK-OVERPAY-CHECK",
                ),
            )
        connection.rollback()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT la.application_id
                FROM LOAN_APPLICATION AS la
                JOIN LOAN AS l ON la.application_id = l.application_id
                LIMIT 1
                FOR UPDATE
                """
            )
            funded = cursor.fetchone()
            _expect_database_rejection(
                cursor,
                """
                UPDATE LOAN_APPLICATION
                SET application_status = 'Under Review',
                    manager_id = NULL,
                    decision_date = NULL
                WHERE application_id = %s
                """,
                (funded["application_id"],),
            )
        connection.rollback()
    finally:
        connection.rollback()
        connection.close()

    print("Database workflow integration checks passed; all changes rolled back.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
