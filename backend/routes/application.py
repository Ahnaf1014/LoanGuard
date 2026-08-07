"""Loan-application feature routes: list, create, and update status."""

import pymysql
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from database.connection import get_connection

# Application creation and review pages are grouped under this blueprint.
application_bp = Blueprint("application", __name__)


@application_bp.route("/applications")
def applications():
    """Render applications together with each applicant's display name."""

    conn = get_connection()
    cursor = conn.cursor()

    # The join avoids an N+1 query while keeping the list page lightweight.
    cursor.execute("""
        SELECT
            application_id,
            application_date,
            requested_amount,
            application_status,
            first_name,
            last_name
        FROM LOAN_APPLICATION
        JOIN BORROWER
            ON LOAN_APPLICATION.borrower_id = BORROWER.borrower_id
        ORDER BY application_id
    """)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("applications.html", applications=applications)


@application_bp.route("/applications/add", methods=["GET", "POST"])
def add_application():
    """Show supporting dropdown data or create a pending loan application."""
    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # manager_id is intentionally NULL until a manager makes a decision.
            cursor.execute(
                """
            INSERT INTO LOAN_APPLICATION(

                borrower_id,
                loan_officer_id,
                manager_id,
                application_date,
                requested_amount,
                loan_purpose,
                occupation,
                monthly_income

            )

            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)

                """,
                (
                    request.form["borrower_id"],
                    request.form["loan_officer_id"],
                    None,
                    request.form["application_date"],
                    request.form["requested_amount"],
                    request.form["loan_purpose"],
                    request.form["occupation"],
                    request.form["monthly_income"],
                ),
            )
            conn.commit()
            flash("Loan application created successfully!", "success")
        except (KeyError, ValueError, pymysql.MySQLError):
            # FK, check, and malformed-input failures must not leave partial data.
            conn.rollback()
            flash("Could not create the application. Check all values and references.", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("application.applications"))

    conn = get_connection()
    cursor = conn.cursor()

    # Only borrower and LoanOfficer records are valid choices for this form.
    cursor.execute("""
        SELECT borrower_id,
               first_name,
               last_name
        FROM BORROWER
    """)

    borrowers = cursor.fetchall()

    cursor.execute("""
        SELECT
            staff_id,
            first_name,
            last_name
        FROM BANK_STAFF
        WHERE role = 'LoanOfficer'
""")

    loan_officers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "add_application.html", borrowers=borrowers, loan_officers=loan_officers
    )


@application_bp.route(
    "/applications/edit/<int:application_id>", methods=["GET", "POST"]
)
def edit_application(application_id):
    """Show an application's status or persist one allowed status transition."""

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        try:
            status = request.form["application_status"]
            # Never rely solely on the browser select; validate the enum server-side.
            if status not in {"Pending", "Under Review", "Approved", "Rejected"}:
                raise ValueError

            cursor.execute(
                """
            UPDATE LOAN_APPLICATION
            SET application_status=%s
            WHERE application_id=%s
        """,
                (status, application_id),
            )
            # A deleted application cannot be silently treated as successfully updated.
            if cursor.rowcount == 0:
                abort(404)
            conn.commit()
            flash("Application status updated successfully!", "success")
        except (KeyError, ValueError, pymysql.MySQLError):
            conn.rollback()
            flash("Could not update the application status.", "danger")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("application.applications"))

    cursor.execute(
        """
        SELECT *
        FROM LOAN_APPLICATION
        WHERE application_id=%s
    """,
        (application_id,),
    )

    application = cursor.fetchone()

    cursor.close()
    conn.close()

    # A typed URL may reference an application removed by another user.
    if application is None:
        abort(404)

    return render_template("edit_application.html", application=application)
