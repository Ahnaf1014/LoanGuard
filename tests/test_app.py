"""Application-factory smoke tests that do not require MySQL."""

import sys
import unittest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-only-secret"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class ApplicationFactoryTests(unittest.TestCase):
    def test_expected_feature_routes_are_registered(self):
        flask_app = create_app(TestConfig)
        endpoints = {rule.endpoint for rule in flask_app.url_map.iter_rules()}
        self.assertTrue(
            {
                "dashboard.dashboard",
                "borrower.borrowers",
                "application.applications",
                "assessment.assessments",
            }.issubset(endpoints)
        )

    def test_production_rejects_default_secret(self):
        class UnsafeProductionConfig(TestConfig):
            APP_ENV = "production"
            SECRET_KEY = "change-this-development-secret"

        with self.assertRaises(RuntimeError):
            create_app(UnsafeProductionConfig)


if __name__ == "__main__":
    unittest.main()
