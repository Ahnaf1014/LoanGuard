"""Application entry point and route registration for LoanGuard.

This file deliberately contains only application-wide setup. Feature-specific
HTTP handlers live in ``routes/`` so borrower, application, and dashboard
work can evolve independently.
"""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from routes.application import application_bp
from routes.assessment import assessment_bp
from routes.borrower import borrower_bp
from routes.dashboard import dashboard_bp
from security import init_security


def create_app(config_object=Config):
    """Create and configure the Flask application."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(config_object)

    if (
        flask_app.config.get("APP_ENV") == "production"
        and flask_app.config["SECRET_KEY"] == "change-this-development-secret"
    ):
        raise RuntimeError("Production requires a unique SECRET_KEY.")

    if flask_app.config.get("TRUST_PROXY"):
        # Trust exactly one hosting proxy (for example, Render) for scheme/host.
        flask_app.wsgi_app = ProxyFix(
            flask_app.wsgi_app, x_for=1, x_proto=1, x_host=1
        )

    # Each blueprint owns one user-facing feature area and its URL endpoints.
    flask_app.register_blueprint(borrower_bp)
    flask_app.register_blueprint(application_bp)
    flask_app.register_blueprint(assessment_bp)
    flask_app.register_blueprint(dashboard_bp)
    init_security(flask_app)

    return flask_app


app = create_app()

if __name__ == "__main__":
    # Use ``flask run`` or this command after MySQL has been initialized.
    app.run(debug=Config.DEBUG)
