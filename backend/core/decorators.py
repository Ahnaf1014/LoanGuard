"""Reusable authentication and role-based authorization decorators."""

from functools import wraps

from flask import abort, redirect, request, url_for
from werkzeug.routing import BuildError

from core.auth import current_user


def login_required(view):
    """Require a signed-in user and preserve the originally requested URL."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            try:
                login_url = url_for("auth.login", next=request.full_path.rstrip("?"))
            except (BuildError, RuntimeError):
                # A project may adopt the decorator before registering auth routes.
                abort(401)
            return redirect(login_url)
        return view(*args, **kwargs)

    return wrapped


def roles_accepted(*roles: str):
    """Require authentication and membership in one of ``roles``."""

    if not roles:
        raise ValueError("roles_accepted requires at least one role")
    allowed_roles = frozenset(roles)

    def decorate(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if user is None:
                return login_required(view)(*args, **kwargs)
            if user.role not in allowed_roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorate
