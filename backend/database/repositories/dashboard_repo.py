"""Data access operations for portfolio dashboard metrics."""

from database.connection import cursor_scope


class DashboardRepository:
    """Encapsulates raw SQL queries for portfolio metrics."""

    @staticmethod
    def get_metrics():
        """Retrieve total portfolio totals and status summary metrics."""
        with cursor_scope() as cursor:
            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM BORROWER) AS total_borrowers,
                    COUNT(*) AS total_applications,
                    COALESCE(SUM(application_status = 'Pending'), 0) AS pending,
                    COALESCE(SUM(requested_amount), 0) AS total_amount
                FROM LOAN_APPLICATION
                """
            )
            return cursor.fetchone()
