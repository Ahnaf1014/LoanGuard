"""MySQL connection helpers used by all database-backed feature routes."""

import ssl
from contextlib import contextmanager

import pymysql

from config import Config


def _build_ssl_config():
    """Build a verifying SSL context from system CAs, a CA file, or PEM text."""
    if not Config.DB_SSL_CA:
        return ssl.create_default_context()

    ca_value = Config.DB_SSL_CA.strip()
    if "-----BEGIN CERTIFICATE-----" in ca_value:
        return ssl.create_default_context(cadata=ca_value)

    return ssl.create_default_context(cafile=ca_value)


def get_connection():
    """Return a transaction-controlled connection with dictionary rows.

    Callers own the returned connection: they must commit successful writes,
    roll back failed writes, and always close both cursor and connection.
    """

    connect_kwargs = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "database": Config.DB_NAME,
        # Dictionary rows let templates use readable names such as
        # ``borrower.first_name`` rather than brittle numeric column indexes.
        "cursorclass": pymysql.cursors.DictCursor,
        "charset": "utf8mb4",
        "connect_timeout": Config.DB_CONNECT_TIMEOUT,
        "read_timeout": Config.DB_READ_TIMEOUT,
        "write_timeout": Config.DB_WRITE_TIMEOUT,
        # Explicit commits keep multi-step writes atomic and reversible.
        "autocommit": False,
    }

    if Config.DB_SSL:
        connect_kwargs["ssl"] = _build_ssl_config()

    return pymysql.connect(**connect_kwargs)


@contextmanager
def cursor_scope(*, commit=False):
    """Yield a cursor and always close its connection.

    Write scopes commit once after all statements succeed and roll back on any
    exception. Read scopes still benefit from deterministic cursor/connection
    cleanup when a query or template-preparation step fails.
    """

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            yield cursor
        if commit:
            connection.commit()
    except Exception:
        if commit:
            connection.rollback()
        raise
    finally:
        connection.close()
