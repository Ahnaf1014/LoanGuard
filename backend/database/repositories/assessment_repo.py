"""Data access operations for the CREDIT_ASSESSMENT table."""

from database.connection import cursor_scope


class AssessmentRepository:
    """Encapsulates raw SQL queries for Credit Assessment operations."""

    @staticmethod
    def get_all():
        """Retrieve all credit assessments with borrower and analyst names."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT ca.assessment_id,
                       ca.assessment_date,
                       ca.credit_score,
                       ca.risk_level,
                       ca.recommendation,
                       ca.default_probability,
                       CONCAT(b.first_name, ' ', b.last_name) AS borrower_name,
                       CONCAT(s.first_name, ' ', s.last_name) AS analyst_name,
                       la.application_id,
                       la.requested_amount,
                       la.application_status
                FROM CREDIT_ASSESSMENT AS ca
                JOIN LOAN_APPLICATION AS la
                    ON ca.application_id = la.application_id
                JOIN BORROWER AS b ON la.borrower_id = b.borrower_id
                JOIN BANK_STAFF AS s ON ca.analyst_id = s.staff_id
                ORDER BY ca.assessment_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_application_options():
        """Retrieve application list for assessment dropdowns."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT la.application_id,
                       CONCAT(b.first_name, ' ', b.last_name) AS borrower_name,
                       la.requested_amount,
                       la.application_status
                FROM LOAN_APPLICATION AS la
                JOIN BORROWER AS b ON la.borrower_id = b.borrower_id
                ORDER BY la.application_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_analyst_options():
        """Retrieve credit analyst list for assessment dropdowns."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT staff_id, first_name, last_name
                FROM BANK_STAFF
                WHERE role = 'CreditAnalyst'
                ORDER BY first_name, last_name, staff_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def create(data: dict):
        """Insert a credit assessment verifying credit analyst role."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO CREDIT_ASSESSMENT (
                    application_id,
                    analyst_id,
                    assessment_date,
                    credit_score,
                    risk_level,
                    recommendation,
                    default_probability,
                    remarks
                )
                SELECT %s, staff_id, %s, %s, %s, %s, %s, %s
                FROM BANK_STAFF
                WHERE staff_id = %s AND role = 'CreditAnalyst'
                """,
                (
                    data["application_id"],
                    data["assessment_date"],
                    data["credit_score"],
                    data["risk_level"],
                    data["recommendation"],
                    data["default_probability"],
                    data["remarks"],
                    data["analyst_id"],
                ),
            )
            return cursor.rowcount
