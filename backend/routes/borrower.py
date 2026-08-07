"""Borrower feature routes: list, create, update, and delete borrowers."""

import pymysql
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from database.connection import get_connection

# All borrower endpoints are named ``borrower.<function_name>`` for url_for.
borrower_bp = Blueprint("borrower", __name__)


@borrower_bp.route("/borrowers")
def borrowers():
    """Render the borrower directory ordered by its stable primary key."""

    conn = get_connection()
    cursor = conn.cursor()

    # Templates need the full address record for future display extensions.
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
    """Show the create form or persist one new borrower from a POST request."""

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        try:

            # Parameterized SQL prevents submitted values from becoming SQL code.
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
            flash("Borrower added successfully!", "success")

        except pymysql.err.IntegrityError:

            # Unique NID and email constraints are enforced by MySQL.
            conn.rollback()
            flash("Email or NID already exists.", "danger")

        finally:

            cursor.close()
            conn.close()

        return redirect(url_for("borrower.borrowers"))

    return render_template("add_borrower.html")


@borrower_bp.route("/borrowers/delete/<int:borrower_id>", methods=["POST"])
def delete_borrower(borrower_id):
    """Delete an unreferenced borrower after an explicit POST confirmation."""

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM BORROWER
            WHERE borrower_id=%s
            """,
            (borrower_id,),
        )

        # rowcount distinguishes a stale UI link from a successful deletion.
        if cursor.rowcount == 0:
            conn.rollback()
            flash("Borrower not found.", "warning")
        else:
            conn.commit()
            flash("Borrower deleted successfully.", "success")

    except pymysql.err.IntegrityError:

        # The foreign key intentionally protects application history.
        conn.rollback()
        flash(
            "Cannot delete borrower because loan applications exist.",
            "danger",
        )

    finally:

        cursor.close()
        conn.close()

    return redirect(url_for("borrower.borrowers"))


@borrower_bp.route("/borrowers/edit/<int:borrower_id>", methods=["GET", "POST"])
def edit_borrower(borrower_id):
    """Show or update a borrower; return 404 when the ID does not exist."""

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        try:

            # NID is included here because the edit form exposes it to staff.
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
            flash("Borrower updated successfully!", "success")

        except pymysql.err.IntegrityError:

            conn.rollback()
            flash("Email or NID already exists.", "danger")

        finally:

            cursor.close()
            conn.close()

        return redirect(url_for("borrower.borrowers"))

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

    # Avoid rendering a form whose ``borrower`` value would be missing.
    if borrower is None:
        abort(404)

    return render_template("edit_borrower.html", borrower=borrower)
