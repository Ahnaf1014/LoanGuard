"""Business operations and validation for Borrower entities."""

import pymysql

from core.exceptions import (
    DatabaseError,
    DuplicateResourceError,
    ResourceConflictError,
)
from core.validation import email_address, optional_text, required_text
from database.repositories.borrower_repo import BorrowerRepository


class BorrowerService:
    """Provides business logic for Borrower CRUD operations."""

    @staticmethod
    def _extract_values(form):
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

    @classmethod
    def list_borrowers(cls):
        """Return all borrowers."""
        return BorrowerRepository.get_all()

    @classmethod
    def get_borrower(cls, borrower_id: int):
        """Return borrower by ID or None."""
        return BorrowerRepository.get_by_id(borrower_id)

    @classmethod
    def create_borrower(cls, form):
        """Validate and create a borrower."""
        values = cls._extract_values(form)
        try:
            return BorrowerRepository.create(values)
        except pymysql.err.IntegrityError as exc:
            raise DuplicateResourceError("Email or NID already exists.") from exc
        except pymysql.MySQLError as exc:
            raise DatabaseError("The borrower could not be saved.") from exc

    @classmethod
    def update_borrower(cls, borrower_id: int, form):
        """Validate and update a borrower; report whether it exists."""
        values = cls._extract_values(form)
        try:
            return BorrowerRepository.update(values, borrower_id)
        except pymysql.err.IntegrityError as exc:
            raise DuplicateResourceError("Email or NID already exists.") from exc
        except pymysql.MySQLError as exc:
            raise DatabaseError("The borrower could not be updated.") from exc

    @classmethod
    def delete_borrower(cls, borrower_id: int) -> bool:
        """Delete an unreferenced borrower."""
        try:
            return BorrowerRepository.delete(borrower_id)
        except pymysql.err.IntegrityError as exc:
            raise ResourceConflictError(
                "Cannot delete a borrower with loan applications."
            ) from exc
        except pymysql.MySQLError as exc:
            raise DatabaseError("The borrower could not be deleted.") from exc
