"""MySQL connection factory used by all database-backed feature routes."""

import pymysql

from config import Config


def get_connection():
    """Return a transaction-controlled connection with dictionary rows.

    Callers own the returned connection: they must commit successful writes,
    roll back failed writes, and always close both cursor and connection.
    """

    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        # Dictionary rows let templates use readable names such as
        # ``borrower.first_name`` rather than brittle numeric column indexes.
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
        # Explicit commits keep multi-step writes atomic and reversible.
        autocommit=False,
    )
