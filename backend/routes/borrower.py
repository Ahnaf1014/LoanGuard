from flask import Blueprint, render_template, request, redirect
from database.connection import get_connection

borrower_bp = Blueprint("borrower", __name__)


@borrower_bp.route("/borrowers")
def borrowers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM BORROWER
        ORDER BY borrower_id
    """)

    borrowers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("borrowers.html", borrowers=borrowers)


@borrower_bp.route("/borrowers/add", methods=["GET", "POST"])
def add_borrower():

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO BORROWER(
                first_name,
                last_name,
                nid,
                email,
                house_no,
                street,
                city,
                postal_code
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """,
            (
                request.form["first_name"],
                request.form["last_name"],
                request.form["nid"],
                request.form["email"],
                request.form["house_no"],
                request.form["street"],
                request.form["city"],
                request.form["postal_code"],
            ),
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/borrowers")
    # GET
    return render_template("add_borrower.html")


@borrower_bp.route("/borrowers/delete/<int:borrower_id>")
def delete_borrower(borrower_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM BORROWER
        WHERE borrower_id=%s
    """,
        (borrower_id,),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/borrowers")


@borrower_bp.route("/borrowers/edit/<int:borrower_id>", methods=["GET", "POST"])
def edit_borrower(borrower_id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute(
            """
            UPDATE BORROWER
            SET
                first_name=%s,
                last_name=%s,
                nid=%s,
                email=%s,
                house_no=%s,
                street=%s,
                city=%s,
                postal_code=%s
            WHERE borrower_id=%s
        """,
            (
                request.form["first_name"],
                request.form["last_name"],
                request.form["nid"],
                request.form["email"],
                request.form["house_no"],
                request.form["street"],
                request.form["city"],
                request.form["postal_code"],
                borrower_id,
            ),
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/borrowers")

    cursor.execute(
        """
        SELECT *
        FROM BORROWER
        WHERE borrower_id=%s
    """,
        (borrower_id,),
    )

    borrower = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_borrower.html", borrower=borrower)
