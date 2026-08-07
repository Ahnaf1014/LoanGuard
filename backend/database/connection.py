"""MySQL connection factory used by all database-backed feature routes."""

import os

import pymysql

from config import Config


def _build_ssl_config():
    """Return an SSL config that accepts either a CA file path or PEM text."""
    if not Config.DB_SSL_CA:
        # Render's Linux image includes standard CA bundle certificates.
        return {"ca": "/etc/ssl/certs/ca-certificates.crt"}

    ca_value = Config.DB_SSL_CA.strip()
    if "-----BEGIN CERTIFICATE-----" in ca_value:
        cert_path = "/tmp/aiven-ca.pem"
        with open(cert_path, "w", encoding="utf-8") as cert_file:
            cert_file.write(ca_value)
        return {"ca": cert_path}

    return {"ca": ca_value}


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
        # Explicit commits keep multi-step writes atomic and reversible.
        "autocommit": False,
    }

    if Config.DB_SSL:
        connect_kwargs["ssl"] = _build_ssl_config()

    return pymysql.connect(**connect_kwargs)
