"""Unit tests for session identity, RBAC, and password controls."""

import sys
import unittest
from pathlib import Path

from flask import Flask

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from core.auth import (  # noqa: E402
    AuthenticatedUser,
    current_user,
    login_user,
    logout_user,
)
from core.decorators import login_required, roles_accepted  # noqa: E402
from core.security import hash_password, verify_password  # noqa: E402


class CoreTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, SECRET_KEY="test-only-secret")

        @app.get("/private")
        @login_required
        def private():
            return "private"

        @app.get("/manager")
        @roles_accepted("BranchManager")
        def manager():
            return "manager"

        self.app = app
        self.client = app.test_client()

    def _login(self, role="LoanOfficer"):
        with self.client.session_transaction() as flask_session:
            flask_session["authenticated_user"] = {
                "staff_id": 7,
                "email": "staff@example.com",
                "role": role,
                "display_name": "Test Staff",
            }

    def test_session_identity_round_trip_and_logout(self):
        with self.app.test_request_context("/"):
            identity = AuthenticatedUser(7, "staff@example.com", "LoanOfficer", "Staff")
            login_user(identity)
            self.assertEqual(current_user(), identity)
            logout_user()
            self.assertIsNone(current_user())

    def test_login_required_rejects_anonymous_request(self):
        self.assertEqual(self.client.get("/private").status_code, 401)

    def test_role_decorator_enforces_allowed_roles(self):
        self._login("LoanOfficer")
        self.assertEqual(self.client.get("/manager").status_code, 403)
        self._login("BranchManager")
        self.assertEqual(self.client.get("/manager").status_code, 200)

    def test_password_hashing(self):
        encoded = hash_password("correct horse battery staple")
        self.assertTrue(verify_password(encoded, "correct horse battery staple"))
        self.assertFalse(verify_password(encoded, "wrong"))


if __name__ == "__main__":
    unittest.main()
