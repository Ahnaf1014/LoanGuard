"""Loan-application feature controllers: list, create, and update status."""

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

from core.exceptions import DatabaseError, NotFoundError
from core.validation import ValidationError
from services.application_service import (
    APPLICATION_STATUSES,
    DECISION_STATUSES,
    ApplicationService,
)

application_bp = Blueprint("application", __name__)


@application_bp.route("/applications")
def applications():
    """Render applications together with each applicant's display name."""
    application_rows = ApplicationService.list_applications()
    return render_template("application/list.html", applications=application_rows)


@application_bp.route("/applications/add", methods=["GET", "POST"])
def add_application():
    """Show supporting dropdown data or create a pending loan application."""
    if request.method == "POST":
        try:
            ApplicationService.create_application(request.form)
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("application.add_application"))
        except DatabaseError:
            current_app.logger.exception("Failed to create loan application")
            flash(
                "The application could not be saved. Check the selected records.",
                "danger",
            )
            return redirect(url_for("application.add_application"))

        flash("Loan application created successfully.", "success")
        return redirect(url_for("application.applications"))

    borrowers, loan_officers = ApplicationService.get_add_form_options()
    return render_template(
        "application/add.html", borrowers=borrowers, loan_officers=loan_officers
    )


@application_bp.route(
    "/applications/edit/<int:application_id>", methods=["GET", "POST"]
)
def edit_application(application_id):
    """Show an application's status or persist a manager-backed decision."""
    if request.method == "POST":
        try:
            ApplicationService.update_status(application_id, request.form)
        except NotFoundError:
            abort(404)
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(
                url_for("application.edit_application", application_id=application_id)
            )
        except DatabaseError:
            current_app.logger.exception(
                "Failed to update loan application %s", application_id
            )
            flash("The application status could not be updated.", "danger")
            return redirect(
                url_for("application.edit_application", application_id=application_id)
            )

        flash("Application status updated successfully.", "success")
        return redirect(url_for("application.applications"))

    application, managers = ApplicationService.get_edit_form_data(application_id)
    if application is None:
        abort(404)

    return render_template(
        "application/edit.html",
        application=application,
        statuses=APPLICATION_STATUSES,
        decision_statuses=DECISION_STATUSES,
        managers=managers,
    )
