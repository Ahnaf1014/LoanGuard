"""Business operations for Dashboard statistics."""

from database.repositories.dashboard_repo import DashboardRepository


class DashboardService:
    """Provides business logic for portfolio dashboard indicators."""

    @staticmethod
    def get_summary_metrics():
        """Retrieve total borrowers, applications, pending count, and requested total."""
        return DashboardRepository.get_metrics()
