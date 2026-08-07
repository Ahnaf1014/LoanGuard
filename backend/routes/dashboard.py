"""Dashboard feature: read-only portfolio totals shown on the home page."""

from flask import Blueprint, render_template

from database.connection import get_connection

# A blueprint keeps dashboard URLs separate from borrower/application features.
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    """Load summary metrics and render the dashboard landing page."""

    conn = get_connection()
    cursor = conn.cursor()

    # Run small aggregate queries instead of loading every record into memory.
    cursor.execute("SELECT COUNT(*) AS total FROM BORROWER")
    total_borrowers = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM LOAN_APPLICATION")
    total_applications = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM LOAN_APPLICATION
        WHERE application_status='Pending'
    """)
    pending = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT IFNULL(SUM(requested_amount),0) AS total
        FROM LOAN_APPLICATION
    """)
    total_amount = cursor.fetchone()["total"]

    # This route is read-only; closing releases the MySQL connection promptly.
    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_borrowers=total_borrowers,
        total_applications=total_applications,
        pending=pending,
        total_amount=total_amount,
    )
