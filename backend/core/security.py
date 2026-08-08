"""Small application-wide web security controls."""

import hmac
import secrets

from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

_CSRF_SESSION_KEY = "_csrf_token"
_SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def hash_password(password: str) -> str:
    """Hash a password using Werkzeug's current secure default algorithm."""

    if not isinstance(password, str) or not password:
        raise ValueError("Password must not be empty.")
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Safely compare a password against its stored adaptive hash."""

    if not password_hash or not password:
        return False
    return check_password_hash(password_hash, password)


def _csrf_token():
    token = session.get(_CSRF_SESSION_KEY)
    if token is None:
        token = secrets.token_urlsafe(32)
        session[_CSRF_SESSION_KEY] = token
    return token


def init_security(app):
    """Register CSRF validation and conservative browser security headers."""

    app.jinja_env.globals["csrf_token"] = _csrf_token

    @app.before_request
    def protect_state_changes():
        if request.method in _SAFE_METHODS:
            return None

        expected = session.get(_CSRF_SESSION_KEY, "")
        submitted = request.form.get("_csrf_token", "")
        if (
            not expected
            or not submitted
            or not hmac.compare_digest(expected, submitted)
        ):
            abort(400, description="The form security token is missing or invalid.")
        return None

    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy", "strict-origin-when-cross-origin"
        )
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "img-src 'self' data:; "
            "style-src 'self' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net data:; "
            "script-src 'self' https://cdn.jsdelivr.net",
        )
        if response.mimetype == "text/html":
            response.headers.setdefault("Cache-Control", "no-store")
        if request.is_secure:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response
