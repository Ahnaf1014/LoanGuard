"""Shared parsing and validation for HTML form inputs."""

from datetime import date
from decimal import Decimal, InvalidOperation
from email.utils import parseaddr

from core.exceptions import ValidationError


def required_text(form, field, *, label, max_length):
    value = form.get(field, "").strip()
    if not value:
        raise ValidationError(f"{label} is required.")
    if len(value) > max_length:
        raise ValidationError(f"{label} must be at most {max_length} characters.")
    return value


def optional_text(form, field, *, label, max_length):
    value = form.get(field, "").strip()
    if len(value) > max_length:
        raise ValidationError(f"{label} must be at most {max_length} characters.")
    return value or None


def email_address(form, field="email"):
    value = required_text(form, field, label="Email", max_length=100).lower()
    parsed_name, parsed_address = parseaddr(value)
    if parsed_name or parsed_address != value or "@" not in value:
        raise ValidationError("Enter a valid email address.")
    local, domain = value.rsplit("@", 1)
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise ValidationError("Enter a valid email address.")
    return value


def integer_value(form, field, *, label, minimum=None, maximum=None):
    try:
        value = int(form.get(field, ""))
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{label} must be a whole number.") from exc
    if minimum is not None and value < minimum:
        raise ValidationError(f"{label} must be at least {minimum}.")
    if maximum is not None and value > maximum:
        raise ValidationError(f"{label} must be at most {maximum}.")
    return value


def positive_int(form, field, *, label):
    return integer_value(form, field, label=label, minimum=1)


def decimal_value(form, field, *, label, minimum, maximum):
    try:
        value = Decimal(form.get(field, ""))
    except (InvalidOperation, TypeError) as exc:
        raise ValidationError(f"{label} must be a number.") from exc
    if not value.is_finite() or value < minimum or value > maximum:
        raise ValidationError(f"{label} must be between {minimum} and {maximum}.")
    if value.as_tuple().exponent < -2:
        raise ValidationError(f"{label} must have at most two decimal places.")
    return value


def iso_date(form, field, *, label):
    try:
        return date.fromisoformat(form.get(field, ""))
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{label} must be a valid date.") from exc
