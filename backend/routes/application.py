from flask import Blueprint, render_template, request, redirect
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
                1,
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

    cursor.close()
    conn.close()

    return render_template("add_application.html", borrowers=borrowers)
