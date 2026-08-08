"""Data access operations for the LOAN_APPLICATION table."""

from database.connection import cursor_scope


class ApplicationRepository:
    """Encapsulates raw SQL queries for Loan Application operations."""

    @staticmethod
    def get_all():
        """Retrieve all loan applications with applicant names."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT la.application_id,
                       la.application_date,
                       la.requested_amount,
                       la.application_status,
                       b.first_name,
                       b.last_name
                FROM LOAN_APPLICATION AS la
                JOIN BORROWER AS b ON la.borrower_id = b.borrower_id
                ORDER BY la.application_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_id(application_id: int):
        """Retrieve application details by primary key ID."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT application_id, application_status, manager_id, decision_date
                FROM LOAN_APPLICATION
                WHERE application_id = %s
                """,
                (application_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def get_borrower_options():
        """Retrieve borrower list for application form dropdowns."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT borrower_id, first_name, last_name
                FROM BORROWER
                ORDER BY first_name, last_name, borrower_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_loan_officer_options():
        """Retrieve loan officers list for application form dropdowns."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT staff_id, first_name, last_name
                FROM BANK_STAFF
                WHERE role = 'LoanOfficer'
                ORDER BY first_name, last_name, staff_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_branch_manager_options():
        """Retrieve branch managers list for decision dropdowns."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT staff_id, first_name, last_name
                FROM BANK_STAFF
                WHERE role = 'BranchManager'
                ORDER BY first_name, last_name, staff_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def create(values: dict):
        """Insert a pending loan application verifying loan officer role."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO LOAN_APPLICATION (
                    borrower_id,
                    loan_officer_id,
                    manager_id,
                    application_date,
                    requested_amount,
                    loan_purpose,
                    occupation,
                    monthly_income
                )
                SELECT %s, staff_id, NULL, %s, %s, %s, %s, %s
                FROM BANK_STAFF
                WHERE staff_id = %s AND role = 'LoanOfficer'
                """,
                (
                    values["borrower_id"],
                    values["application_date"],
                    values["requested_amount"],
                    values["loan_purpose"],
                    values["occupation"],
                    values["monthly_income"],
                    values["loan_officer_id"],
                ),
            )
            return cursor.rowcount

    @staticmethod
    def update_status(application_id: int, status: str, manager_id: int | None):
        """Update status and record manager decision date."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                SELECT application_id
                FROM LOAN_APPLICATION
                WHERE application_id = %s
                FOR UPDATE
                """,
                (application_id,),
            )
            if cursor.fetchone() is None:
                return False

            if manager_id is not None:
                cursor.execute(
                    """
                    SELECT staff_id
                    FROM BANK_STAFF
                    WHERE staff_id = %s AND role = 'BranchManager'
                    """,
                    (manager_id,),
                )
                if cursor.fetchone() is None:
                    return None  # Invalid manager

            cursor.execute(
                """
                UPDATE LOAN_APPLICATION
                SET application_status = %s,
                    manager_id = %s,
                    decision_date = CASE
                        WHEN %s IN ('Approved', 'Rejected') THEN CURRENT_TIMESTAMP
                        ELSE NULL
                    END
                WHERE application_id = %s
                """,
                (status, manager_id, status, application_id),
            )
            return True
