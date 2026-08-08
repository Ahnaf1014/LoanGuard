"""Tests for CSRF enforcement and browser security headers."""

import re
import sys
import unittest
from pathlib import Path

from flask import Flask, render_template_string

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from core.security import init_security  # noqa: E402


class SecurityTests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, SECRET_KEY="test-only-secret")
        init_security(app)

        @app.route("/form", methods=["GET", "POST"])
        def form():
            return render_template_string(
                '<form method="post"><input name="_csrf_token" '
                'value="{{ csrf_token() }}"></form>'
            )

        self.client = app.test_client()

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post("/form")
        self.assertEqual(response.status_code, 400)

    def test_generated_csrf_token_allows_post(self):
        page = self.client.get("/form")
        token = re.search(rb'value="([^"]+)"', page.data).group(1).decode()
        response = self.client.post("/form", data={"_csrf_token": token})
        self.assertEqual(response.status_code, 200)

    def test_security_headers_are_present(self):
        response = self.client.get("/form")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_https_response_enables_hsts(self):
        response = self.client.get("/form", base_url="https://localhost")
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )


if __name__ == "__main__":
    unittest.main()
