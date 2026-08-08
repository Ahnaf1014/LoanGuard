"""Business operations and validation for Loan Application entities."""

from decimal import Decimal

import pymysql

from core.exceptions import DatabaseError, NotFoundError
from core.validation import (
    ValidationError,
    decimal_value,
    iso_date,
    positive_int,
    required_text,
)
from database.repositories.application_repo import ApplicationRepository

APPLICATION_STATUSES = ("Pending", "Under Review", "Approved", "Rejected")
DECISION_STATUSES = {"Approved", "Rejected"}
MAX_MONEY = Decimal("9999999999.99")


class ApplicationService:
    """Provides business logic for Loan Application operations."""

    @staticmethod
    def _extract_values(form):
        return {
            "borrower_id": positive_int(form, "borrower_id", label="Borrower"),
            "loan_officer_id": positive_int(
                form, "loan_officer_id", label="Loan officer"
            ),
            "application_date": iso_date(
                form, "application_date", label="Application date"
            ),
            "requested_amount": decimal_value(
                form,
                "requested_amount",
                label="Requested amount",
                minimum=Decimal("0.01"),
                maximum=MAX_MONEY,
            ),
            "loan_purpose": required_text(
                form, "loan_purpose", label="Loan purpose", max_length=255
            ),
            "occupation": required_text(
                form, "occupation", label="Occupation", max_length=100
            ),
            "monthly_income": decimal_value(
                form,
                "monthly_income",
                label="Monthly income",
                minimum=Decimal("0.01"),
                maximum=MAX_MONEY,
            ),
        }

    @classmethod
    def list_applications(cls):
        """Return all applications formatted with borrower names."""
        return ApplicationRepository.get_all()

    @classmethod
    def get_add_form_options(cls):
        """Return borrowers and loan officers for application creation."""
        borrowers = ApplicationRepository.get_borrower_options()
        loan_officers = ApplicationRepository.get_loan_officer_options()
        return borrowers, loan_officers

    @classmethod
    def create_application(cls, form):
        """Validate form and persist application. Raises ValidationError on failure."""
        values = cls._extract_values(form)
        try:
            rowcount = ApplicationRepository.create(values)
        except pymysql.err.IntegrityError as exc:
            raise ValidationError("Select valid borrower and staff records.") from exc
        except pymysql.MySQLError as exc:
            raise DatabaseError("The application could not be saved.") from exc
        if rowcount != 1:
            raise ValidationError("Select a valid loan officer.")

    @classmethod
    def get_edit_form_data(cls, application_id: int):
        """Return application and branch managers for status update form."""
        application = ApplicationRepository.get_by_id(application_id)
        managers = ApplicationRepository.get_branch_manager_options()
        return application, managers

    @classmethod
    def update_status(cls, application_id: int, form):
        """Validate status update and update record. Raises ValidationError or KeyError."""
        status = form.get("application_status", "")
        if status not in APPLICATION_STATUSES:
            raise ValidationError("Select a valid application status.")

        manager_id = (
            positive_int(form, "manager_id", label="Branch manager")
            if status in DECISION_STATUSES
            else None
        )

        try:
            result = ApplicationRepository.update_status(
                application_id, status, manager_id
            )
        except pymysql.MySQLError as exc:
            raise DatabaseError("The application status could not be updated.") from exc
        if result is False:
            raise NotFoundError("Application not found.")
        if result is None:
            raise ValidationError("Select a valid branch manager.")
