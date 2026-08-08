"""Borrower feature routes: list, create, update, and delete borrowers."""

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
from validation import ValidationError, email_address, optional_text, required_text

borrower_bp = Blueprint("borrower", __name__)

_BORROWER_COLUMNS = """
    borrower_id,
    first_name,
    last_name,
    nid,
    email,
    house_no,
    street,
    city,
    postal_code
"""


def _borrower_values(form):
    return (
        required_text(form, "first_name", label="First name", max_length=50),
        required_text(form, "last_name", label="Last name", max_length=50),
        required_text(form, "nid", label="NID", max_length=20),
        email_address(form),
        optional_text(form, "house_no", label="House number", max_length=20),
        optional_text(form, "street", label="Street", max_length=100),
        optional_text(form, "city", label="City", max_length=50),
        optional_text(form, "postal_code", label="Postal code", max_length=10),
    )


@borrower_bp.route("/borrowers")
def borrowers():
    """Render the borrower directory ordered by its stable primary key."""

    with cursor_scope() as cursor:
        cursor.execute(
            f"""
            SELECT {_BORROWER_COLUMNS}
            FROM BORROWER
            ORDER BY borrower_id
            """
        )
        borrower_rows = cursor.fetchall()

    return render_template("borrowers.html", borrowers=borrower_rows)


@borrower_bp.route("/borrowers/add", methods=["GET", "POST"])
def add_borrower():
    """Show the create form or persist one new borrower from a POST request."""

    if request.method == "GET":
        return render_template("add_borrower.html")

    try:
        values = _borrower_values(request.form)
    except ValidationError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("borrower.add_borrower"))

    try:
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO BORROWER (
                    first_name,
                    last_name,
                    nid,
                    email,
                    house_no,
                    street,
                    city,
                    postal_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                values,
            )
    except pymysql.err.IntegrityError:
        flash("Email or NID already exists.", "danger")
        return redirect(url_for("borrower.add_borrower"))
    except pymysql.MySQLError:
        current_app.logger.exception("Failed to create borrower")
        flash("The borrower could not be saved. Please try again.", "danger")
        return redirect(url_for("borrower.add_borrower"))

    flash("Borrower added successfully.", "success")
    return redirect(url_for("borrower.borrowers"))


@borrower_bp.route("/borrowers/delete/<int:borrower_id>", methods=["POST"])
def delete_borrower(borrower_id):
    """Delete an unreferenced borrower after an explicit POST confirmation."""

    try:
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                "DELETE FROM BORROWER WHERE borrower_id = %s",
                (borrower_id,),
            )
            deleted = cursor.rowcount > 0
    except pymysql.err.IntegrityError:
        flash("Cannot delete a borrower with loan applications.", "danger")
        return redirect(url_for("borrower.borrowers"))
    except pymysql.MySQLError:
        current_app.logger.exception("Failed to delete borrower %s", borrower_id)
        flash("The borrower could not be deleted. Please try again.", "danger")
        return redirect(url_for("borrower.borrowers"))

    if deleted:
        flash("Borrower deleted successfully.", "success")
    else:
        flash("Borrower not found.", "warning")
    return redirect(url_for("borrower.borrowers"))


@borrower_bp.route("/borrowers/edit/<int:borrower_id>", methods=["GET", "POST"])
def edit_borrower(borrower_id):
    """Show or update a borrower; return 404 when the ID does not exist."""

    if request.method == "POST":
        try:
            values = _borrower_values(request.form)
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))

        try:
            with cursor_scope(commit=True) as cursor:
                cursor.execute(
                    """
                    UPDATE BORROWER
                    SET first_name = %s,
                        last_name = %s,
                        nid = %s,
                        email = %s,
                        house_no = %s,
                        street = %s,
                        city = %s,
                        postal_code = %s
                    WHERE borrower_id = %s
                    """,
                    (*values, borrower_id),
                )
                if cursor.rowcount == 0:
                    cursor.execute(
                        "SELECT borrower_id FROM BORROWER WHERE borrower_id = %s",
                        (borrower_id,),
                    )
                    exists = cursor.fetchone() is not None
                else:
                    exists = True
        except pymysql.err.IntegrityError:
            flash("Email or NID already exists.", "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))
        except pymysql.MySQLError:
            current_app.logger.exception("Failed to update borrower %s", borrower_id)
            flash("The borrower could not be updated. Please try again.", "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))

        if not exists:
            abort(404)
        flash("Borrower updated successfully.", "success")
        return redirect(url_for("borrower.borrowers"))

    with cursor_scope() as cursor:
        cursor.execute(
            f"""
            SELECT {_BORROWER_COLUMNS}
            FROM BORROWER
            WHERE borrower_id = %s
            """,
            (borrower_id,),
        )
        borrower = cursor.fetchone()

    if borrower is None:
        abort(404)
    return render_template("edit_borrower.html", borrower=borrower)
