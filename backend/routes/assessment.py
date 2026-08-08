"""Credit-assessment feature routes: list and create assessments."""

from decimal import Decimal

import pymysql
from flask import (
    Blueprint,
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
    integer_value,
    iso_date,
    optional_text,
    positive_int,
)

assessment_bp = Blueprint("assessment", __name__)

RISK_LEVELS = ("Low", "Medium", "High")
RECOMMENDATIONS = ("Approve", "Review", "Reject")


@assessment_bp.route("/assessments")
def assessments():
    """Render the credit-assessment register for all evaluated applications."""

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
        assessment_rows = cursor.fetchall()

    return render_template("assessments.html", assessments=assessment_rows)


@assessment_bp.route("/assessments/add", methods=["GET", "POST"])
def add_assessment():
    """Show the assessment form or persist a new assessment."""

    if request.method == "POST":
        try:
            application_id = positive_int(
                request.form, "application_id", label="Application"
            )
            analyst_id = positive_int(request.form, "analyst_id", label="Analyst")
            assessment_date = iso_date(
                request.form, "assessment_date", label="Assessment date"
            )
            credit_score = integer_value(
                request.form,
                "credit_score",
                label="Credit score",
                minimum=0,
                maximum=850,
            )
            risk_level = request.form.get("risk_level", "")
            recommendation = request.form.get("recommendation", "")
            if risk_level not in RISK_LEVELS:
                raise ValidationError("Select a valid risk level.")
            if recommendation not in RECOMMENDATIONS:
                raise ValidationError("Select a valid recommendation.")
            default_probability = decimal_value(
                request.form,
                "default_probability",
                label="Default probability",
                minimum=Decimal("0"),
                maximum=Decimal("100"),
            )
            remarks = optional_text(
                request.form, "remarks", label="Remarks", max_length=4000
            )

            with cursor_scope(commit=True) as cursor:
                # The SELECT side enforces that the submitted analyst has the
                # CreditAnalyst role; a foreign key alone cannot express that.
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
                        application_id,
                        assessment_date,
                        credit_score,
                        risk_level,
                        recommendation,
                        default_probability,
                        remarks,
                        analyst_id,
                    ),
                )
                if cursor.rowcount != 1:
                    raise ValidationError("Select a valid credit analyst.")
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("assessment.add_assessment"))
        except pymysql.MySQLError:
            current_app.logger.exception("Failed to create credit assessment")
            flash(
                "The assessment could not be saved. Check the selected records.",
                "danger",
            )
            return redirect(url_for("assessment.add_assessment"))

        flash("Credit assessment added successfully.", "success")
        return redirect(url_for("assessment.assessments"))

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
        applications = cursor.fetchall()
        cursor.execute(
            """
            SELECT staff_id, first_name, last_name
            FROM BANK_STAFF
            WHERE role = 'CreditAnalyst'
            ORDER BY first_name, last_name, staff_id
            """
        )
        analysts = cursor.fetchall()

    return render_template(
        "add_assessment.html",
        applications=applications,
        analysts=analysts,
        risk_levels=RISK_LEVELS,
        recommendations=RECOMMENDATIONS,
    )
