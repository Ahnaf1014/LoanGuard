"""Credit-assessment feature routes: list and create assessments."""

import pymysql
from flask import Blueprint, flash, redirect, render_template, request, url_for

from database.connection import get_connection

assessment_bp = Blueprint("assessment", __name__)


@assessment_bp.route("/assessments")
def assessments():
    """Render the credit-assessment register for all evaluated applications."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ca.assessment_id,
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
        FROM CREDIT_ASSESSMENT ca
        JOIN LOAN_APPLICATION la
            ON ca.application_id = la.application_id
        JOIN BORROWER b
            ON la.borrower_id = b.borrower_id
        JOIN BANK_STAFF s
            ON ca.analyst_id = s.staff_id
        ORDER BY ca.assessment_id
        """)

    assessments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("assessments.html", assessments=assessments)


@assessment_bp.route("/assessments/add", methods=["GET", "POST"])
def add_assessment():
    """Show the assessment form or persist a new assessment for an application."""

    if request.method == "POST":
        conn = get_connection()
        cursor = conn.cursor()

        try:
            application_id = int(request.form["application_id"])
            analyst_id = int(request.form["analyst_id"])
            assessment_date = request.form["assessment_date"]
            credit_score = int(request.form["credit_score"])
            risk_level = request.form["risk_level"]
            recommendation = request.form["recommendation"]
            default_probability = float(request.form["default_probability"])
            remarks = request.form.get("remarks", "")

            valid_risks = {"Low", "Medium", "High"}
            valid_recommendations = {"Approve", "Review", "Reject"}

            if risk_level not in valid_risks:
                raise ValueError("Invalid risk level")
            if recommendation not in valid_recommendations:
                raise ValueError("Invalid recommendation")
            if credit_score < 0 or default_probability < 0 or default_probability > 100:
                raise ValueError("Assessment values are out of range")

            cursor.execute(
                """
                INSERT INTO CREDIT_ASSESSMENT(
                    application_id,
                    analyst_id,
                    assessment_date,
                    credit_score,
                    risk_level,
                    recommendation,
                    default_probability,
                    remarks
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    application_id,
                    analyst_id,
                    assessment_date,
                    credit_score,
                    risk_level,
                    recommendation,
                    default_probability,
                    remarks,
                ),
            )

            conn.commit()
            flash("Credit assessment added successfully!", "success")

        except (KeyError, TypeError, ValueError, pymysql.MySQLError):
            conn.rollback()
            flash(
                "Could not create the assessment. Check the values and references.",
                "danger",
            )
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("assessment.assessments"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            la.application_id,
            CONCAT(b.first_name, ' ', b.last_name) AS borrower_name,
            la.requested_amount,
            la.application_status
        FROM LOAN_APPLICATION la
        JOIN BORROWER b
            ON la.borrower_id = b.borrower_id
        ORDER BY la.application_id
        """)
    applications = cursor.fetchall()

    cursor.execute("""
        SELECT staff_id, first_name, last_name
        FROM BANK_STAFF
        WHERE role = 'CreditAnalyst'
        ORDER BY staff_id
        """)
    analysts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "add_assessment.html",
        applications=applications,
        analysts=analysts,
    )
