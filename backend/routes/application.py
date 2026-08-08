"""Loan-application feature routes: list, create, and update status."""

from decimal import Decimal

import pymysql
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from database.connection import cursor_scope
from validation import (
    ValidationError,
    decimal_value,
    iso_date,
    positive_int,
    required_text,
)

application_bp = Blueprint("application", __name__)

APPLICATION_STATUSES = ("Pending", "Under Review", "Approved", "Rejected")
DECISION_STATUSES = {"Approved", "Rejected"}
MAX_MONEY = Decimal("9999999999.99")


@application_bp.route("/applications")
def applications():
    """Render applications together with each applicant's display name."""

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
        application_rows = cursor.fetchall()

    return render_template("applications.html", applications=application_rows)


def _application_values(form):
    return {
        "borrower_id": positive_int(form, "borrower_id", label="Borrower"),
        "loan_officer_id": positive_int(
            form, "loan_officer_id", label="Loan officer"
        ),
        "application_date": iso_date(
            form, "application_date", label="Application date"
        ),
        "requested_amount": decimal_value(
            form,
            "requested_amount",
            label="Requested amount",
            minimum=Decimal("0.01"),
            maximum=MAX_MONEY,
        ),
        "loan_purpose": required_text(
            form, "loan_purpose", label="Loan purpose", max_length=255
        ),
        "occupation": required_text(
            form, "occupation", label="Occupation", max_length=100
        ),
        "monthly_income": decimal_value(
            form,
            "monthly_income",
            label="Monthly income",
            minimum=Decimal("0.01"),
            maximum=MAX_MONEY,
        ),
    }


@application_bp.route("/applications/add", methods=["GET", "POST"])
def add_application():
    """Show supporting dropdown data or create a pending loan application."""

    if request.method == "POST":
        try:
            values = _application_values(request.form)
            with cursor_scope(commit=True) as cursor:
                # INSERT ... SELECT also enforces the selected staff member's role.
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
                if cursor.rowcount != 1:
                    raise ValidationError("Select a valid loan officer.")
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("application.add_application"))
        except pymysql.MySQLError:
            current_app.logger.exception("Failed to create loan application")
            flash(
                "The application could not be saved. Check the selected records.",
                "danger",
            )
            return redirect(url_for("application.add_application"))

        flash("Loan application created successfully.", "success")
        return redirect(url_for("application.applications"))

    with cursor_scope() as cursor:
        cursor.execute(
            """
            SELECT borrower_id, first_name, last_name
            FROM BORROWER
            ORDER BY first_name, last_name, borrower_id
            """
        )
        borrowers = cursor.fetchall()
        cursor.execute(
            """
            SELECT staff_id, first_name, last_name
            FROM BANK_STAFF
            WHERE role = 'LoanOfficer'
            ORDER BY first_name, last_name, staff_id
            """
        )
        loan_officers = cursor.fetchall()

    return render_template(
        "add_application.html", borrowers=borrowers, loan_officers=loan_officers
    )


@application_bp.route(
    "/applications/edit/<int:application_id>", methods=["GET", "POST"]
)
def edit_application(application_id):
    """Show an application's status or persist a manager-backed decision."""

    if request.method == "POST":
        status = request.form.get("application_status", "")
        if status not in APPLICATION_STATUSES:
            flash("Select a valid application status.", "danger")
            return redirect(
                url_for("application.edit_application", application_id=application_id)
            )

        try:
            manager_id = (
                positive_int(request.form, "manager_id", label="Branch manager")
                if status in DECISION_STATUSES
                else None
            )
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
                    abort(404)

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
                        raise ValidationError("Select a valid branch manager.")

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
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(
                url_for("application.edit_application", application_id=application_id)
            )
        except pymysql.MySQLError:
            current_app.logger.exception(
                "Failed to update loan application %s", application_id
            )
            flash("The application status could not be updated.", "danger")
            return redirect(
                url_for("application.edit_application", application_id=application_id)
            )

        flash("Application status updated successfully.", "success")
        return redirect(url_for("application.applications"))

    with cursor_scope() as cursor:
        cursor.execute(
            """
            SELECT application_id, application_status, manager_id, decision_date
            FROM LOAN_APPLICATION
            WHERE application_id = %s
            """,
            (application_id,),
        )
        application = cursor.fetchone()
        cursor.execute(
            """
            SELECT staff_id, first_name, last_name
            FROM BANK_STAFF
            WHERE role = 'BranchManager'
            ORDER BY first_name, last_name, staff_id
            """
        )
        managers = cursor.fetchall()

    if application is None:
        abort(404)
    return render_template(
        "edit_application.html",
        application=application,
        statuses=APPLICATION_STATUSES,
        decision_statuses=DECISION_STATUSES,
        managers=managers,
    )
