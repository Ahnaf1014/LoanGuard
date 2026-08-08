"""Unit tests for transaction-scope lifecycle guarantees."""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from database.connection import cursor_scope  # noqa: E402


class CursorScopeTests(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = self.connection.cursor.return_value.__enter__.return_value

    def test_write_scope_commits_and_closes(self):
        with patch("database.connection.get_connection", return_value=self.connection):
            with cursor_scope(commit=True) as cursor:
                self.assertIs(cursor, self.cursor)

        self.connection.commit.assert_called_once_with()
        self.connection.rollback.assert_not_called()
        self.connection.close.assert_called_once_with()

    def test_write_scope_rolls_back_and_closes_on_error(self):
        with patch("database.connection.get_connection", return_value=self.connection):
            with self.assertRaises(RuntimeError):
                with cursor_scope(commit=True):
                    raise RuntimeError("test failure")

        self.connection.commit.assert_not_called()
        self.connection.rollback.assert_called_once_with()
        self.connection.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
