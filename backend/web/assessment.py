"""Credit-assessment feature controllers: list and create assessments."""

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from core.exceptions import DatabaseError
from core.validation import ValidationError
from services.assessment_service import (
    RECOMMENDATIONS,
    RISK_LEVELS,
    AssessmentService,
)

assessment_bp = Blueprint("assessment", __name__)


@assessment_bp.route("/assessments")
def assessments():
    """Render the credit-assessment register for all evaluated applications."""
    assessment_rows = AssessmentService.list_assessments()
    return render_template("assessment/list.html", assessments=assessment_rows)


@assessment_bp.route("/assessments/add", methods=["GET", "POST"])
def add_assessment():
    """Show the assessment form or persist a new assessment."""
    if request.method == "POST":
        try:
            AssessmentService.create_assessment(request.form)
        except ValidationError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("assessment.add_assessment"))
        except DatabaseError:
            current_app.logger.exception("Failed to create credit assessment")
            flash(
                "The assessment could not be saved. Check the selected records.",
                "danger",
            )
            return redirect(url_for("assessment.add_assessment"))

        flash("Credit assessment added successfully.", "success")
        return redirect(url_for("assessment.assessments"))

    applications, analysts = AssessmentService.get_add_form_options()
    return render_template(
        "assessment/add.html",
        applications=applications,
        analysts=analysts,
        risk_levels=RISK_LEVELS,
        recommendations=RECOMMENDATIONS,
    )
