"""Unit tests for server-side form validation."""

import sys
import unittest
from decimal import Decimal
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from validation import (  # noqa: E402
    ValidationError,
    decimal_value,
    email_address,
    integer_value,
    optional_text,
    required_text,
)


class ValidationTests(unittest.TestCase):
    def test_required_text_strips_whitespace(self):
        self.assertEqual(
            required_text(
                {"name": "  Alice  "}, "name", label="Name", max_length=20
            ),
            "Alice",
        )

    def test_required_text_rejects_blank_value(self):
        with self.assertRaises(ValidationError):
            required_text({"name": "  "}, "name", label="Name", max_length=20)

    def test_optional_text_converts_blank_to_none(self):
        self.assertIsNone(
            optional_text({"city": " "}, "city", label="City", max_length=50)
        )

    def test_email_is_normalized(self):
        self.assertEqual(
            email_address({"email": " USER@Example.COM "}), "user@example.com"
        )

    def test_email_rejects_invalid_domain(self):
        with self.assertRaises(ValidationError):
            email_address({"email": "user@localhost"})

    def test_integer_bounds_are_inclusive(self):
        self.assertEqual(
            integer_value(
                {"score": "0"},
                "score",
                label="Score",
                minimum=0,
                maximum=850,
            ),
            0,
        )

    def test_decimal_rejects_excess_precision(self):
        with self.assertRaises(ValidationError):
            decimal_value(
                {"amount": "1.001"},
                "amount",
                label="Amount",
                minimum=Decimal("0.01"),
                maximum=Decimal("100"),
            )


if __name__ == "__main__":
    unittest.main()
