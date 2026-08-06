from flask import Blueprint, render_template
from database.connection import get_connection

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_borrowers=total_borrowers,
        total_applications=total_applications,
        pending=pending,
        total_amount=total_amount,
    )
