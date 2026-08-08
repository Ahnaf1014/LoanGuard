"""Borrower feature controllers: list, create, update, and delete borrowers."""

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

from core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceConflictError,
)
from core.validation import ValidationError
from services.borrower_service import BorrowerService

borrower_bp = Blueprint("borrower", __name__)


@borrower_bp.route("/borrowers")
def borrowers():
    """Render the borrower directory ordered by its stable primary key."""
    borrower_rows = BorrowerService.list_borrowers()
    return render_template("borrower/list.html", borrowers=borrower_rows)


@borrower_bp.route("/borrowers/add", methods=["GET", "POST"])
def add_borrower():
    """Show the create form or persist one new borrower from a POST request."""
    if request.method == "GET":
        return render_template("borrower/add.html")

    try:
        BorrowerService.create_borrower(request.form)
    except ValidationError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("borrower.add_borrower"))
    except DuplicateResourceError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("borrower.add_borrower"))
    except DatabaseError:
        current_app.logger.exception("Failed to create borrower")
        flash("The borrower could not be saved. Please try again.", "danger")
        return redirect(url_for("borrower.add_borrower"))

    flash("Borrower added successfully.", "success")
    return redirect(url_for("borrower.borrowers"))


@borrower_bp.route("/borrowers/delete/<int:borrower_id>", methods=["POST"])
def delete_borrower(borrower_id):
    """Delete an unreferenced borrower after an explicit POST confirmation."""
    try:
        deleted = BorrowerService.delete_borrower(borrower_id)
    except ResourceConflictError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("borrower.borrowers"))
    except DatabaseError:
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
            exists = BorrowerService.update_borrower(borrower_id, request.form)
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))
        except DuplicateResourceError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))
        except DatabaseError:
            current_app.logger.exception("Failed to update borrower %s", borrower_id)
            flash("The borrower could not be updated. Please try again.", "danger")
            return redirect(url_for("borrower.edit_borrower", borrower_id=borrower_id))

        if not exists:
            abort(404)
        flash("Borrower updated successfully.", "success")
        return redirect(url_for("borrower.borrowers"))

    borrower = BorrowerService.get_borrower(borrower_id)
    if borrower is None:
        abort(404)
    return render_template("borrower/edit.html", borrower=borrower)
