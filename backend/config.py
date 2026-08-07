"""Environment-backed configuration shared by the Flask application.

Keep credentials outside source control: copy ``.env.example`` to ``.env``
and change the values there. The safe local defaults reduce setup friction,
but the example secret must be replaced in deployed environments.
"""

import os

from dotenv import load_dotenv

# ``load_dotenv`` is harmless when no .env file exists and permits both
# ``python app.py`` from backend/ and ``flask`` commands to use local settings.
load_dotenv()


class Config:
    """Single source of truth for Flask and MySQL configuration values."""
    # Defaults make a local development setup work without requiring every
    # setting to be present in an environment file. Production deployments
    # should always provide a strong SECRET_KEY through the environment.
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret")

    # These describe the MySQL server created from database/schema.sql.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "LoanGuard")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    # Debug is opt-in because Flask's debugger must not be exposed in production.
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}
