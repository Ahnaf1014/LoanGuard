"""Minimal, database-agnostic session identity helpers."""

from dataclasses import asdict, dataclass

from flask import session

_SESSION_USER_KEY = "authenticated_user"


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    """The small, non-sensitive identity stored in a signed Flask session."""

    staff_id: int
    email: str
    role: str
    display_name: str


def login_user(user: AuthenticatedUser) -> None:
    """Rotate session state and persist the authenticated identity."""

    session.clear()
    session[_SESSION_USER_KEY] = asdict(user)
    session.permanent = True


def logout_user() -> None:
    """Remove all session state, including the CSRF token."""

    session.clear()


def current_user() -> AuthenticatedUser | None:
    """Return the session identity, discarding malformed session data."""

    data = session.get(_SESSION_USER_KEY)
    if not isinstance(data, dict):
        return None
    try:
        return AuthenticatedUser(
            staff_id=int(data["staff_id"]),
            email=str(data["email"]),
            role=str(data["role"]),
            display_name=str(data["display_name"]),
        )
    except (KeyError, TypeError, ValueError):
        session.pop(_SESSION_USER_KEY, None)
        return None


def is_authenticated() -> bool:
    """Report whether the request has a valid session identity."""

    return current_user() is not None


def init_auth(app) -> None:
    """Expose request identity helpers to templates."""

    app.jinja_env.globals.update(
        current_user=current_user,
        is_authenticated=is_authenticated,
    )
