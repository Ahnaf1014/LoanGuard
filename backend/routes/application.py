from flask import Blueprint, render_template, request, redirect, flash
from database.connection import get_connection

application_bp = Blueprint("application", __name__)


@application_bp.route("/applications")
def applications():

    conn = get_connection()
    cursor = conn.cursor()

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

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

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

        cursor.close()
        conn.close()

        return redirect("/applications")

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

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute(
            """
            UPDATE LOAN_APPLICATION
            SET application_status=%s
            WHERE application_id=%s
        """,
            (request.form["application_status"], application_id),
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Application status updated successfully!", "success")

        return redirect("/applications")

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

    return render_template("edit_application.html", application=application)
