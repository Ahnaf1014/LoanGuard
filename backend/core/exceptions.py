"""Application exceptions that services can expose without leaking drivers."""


class LoanGuardError(Exception):
    """Base class for expected application-level failures."""


class ValidationError(LoanGuardError, ValueError):
    """Submitted data violates an application rule."""


class NotFoundError(LoanGuardError):
    """A requested domain resource does not exist."""


class DuplicateResourceError(LoanGuardError):
    """A unique resource already exists."""


class ResourceConflictError(LoanGuardError):
    """An operation conflicts with related or current resource state."""


class DatabaseError(LoanGuardError):
    """A persistence operation failed for a non-domain-specific reason."""
