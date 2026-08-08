"""Dashboard feature: read-only portfolio totals shown on the home page."""

from flask import Blueprint, render_template

from database.connection import cursor_scope

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    """Load summary metrics and render the dashboard landing page."""

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
        metrics = cursor.fetchone()

    return render_template("dashboard.html", **metrics)
