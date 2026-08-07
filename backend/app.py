"""Application entry point and route registration for LoanGuard.

This file deliberately contains only application-wide setup. Feature-specific
HTTP handlers live in ``routes/`` so borrower, application, and dashboard
work can evolve independently.
"""

from flask import Flask

from config import Config
from routes.application import application_bp
from routes.assessment import assessment_bp
from routes.borrower import borrower_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)


# Flask uses this key to protect the integrity of flash-message sessions.
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["DEBUG"] = Config.DEBUG

# Each blueprint owns one user-facing feature area and its URL endpoints.
app.register_blueprint(borrower_bp)
app.register_blueprint(application_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    # Use ``flask run`` or this command after MySQL has been initialized.
    app.run(debug=Config.DEBUG)
