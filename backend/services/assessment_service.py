"""Business operations and validation for Credit Assessment entities."""

from decimal import Decimal

import pymysql

from core.exceptions import DatabaseError
from core.validation import (
    ValidationError,
    decimal_value,
    integer_value,
    iso_date,
    optional_text,
    positive_int,
)
from database.repositories.assessment_repo import AssessmentRepository

RISK_LEVELS = ("Low", "Medium", "High")
RECOMMENDATIONS = ("Approve", "Review", "Reject")


class AssessmentService:
    """Provides business logic for Credit Assessment operations."""

    @classmethod
    def list_assessments(cls):
        """Return all credit assessments with borrower and analyst names."""
        return AssessmentRepository.get_all()

    @classmethod
    def get_add_form_options(cls):
        """Return applications and credit analysts for assessment creation."""
        applications = AssessmentRepository.get_application_options()
        analysts = AssessmentRepository.get_analyst_options()
        return applications, analysts

    @classmethod
    def create_assessment(cls, form):
        """Validate form and persist credit assessment."""
        application_id = positive_int(
            form, "application_id", label="Application"
        )
        analyst_id = positive_int(form, "analyst_id", label="Analyst")
        assessment_date = iso_date(
            form, "assessment_date", label="Assessment date"
        )
        credit_score = integer_value(
            form,
            "credit_score",
            label="Credit score",
            minimum=0,
            maximum=850,
        )
        risk_level = form.get("risk_level", "")
        recommendation = form.get("recommendation", "")
        if risk_level not in RISK_LEVELS:
            raise ValidationError("Select a valid risk level.")
        if recommendation not in RECOMMENDATIONS:
            raise ValidationError("Select a valid recommendation.")
        default_probability = decimal_value(
            form,
            "default_probability",
            label="Default probability",
            minimum=Decimal("0"),
            maximum=Decimal("100"),
        )
        remarks = optional_text(
            form, "remarks", label="Remarks", max_length=4000
        )

        data = {
            "application_id": application_id,
            "analyst_id": analyst_id,
            "assessment_date": assessment_date,
            "credit_score": credit_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "default_probability": default_probability,
            "remarks": remarks,
        }

        try:
            rowcount = AssessmentRepository.create(data)
        except pymysql.err.IntegrityError as exc:
            raise ValidationError("Select a valid application and analyst.") from exc
        except pymysql.MySQLError as exc:
            raise DatabaseError("The assessment could not be saved.") from exc
        if rowcount != 1:
            raise ValidationError("Select a valid credit analyst.")
