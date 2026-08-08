"""Data access operations for the BORROWER table."""

from database.connection import cursor_scope

_BORROWER_COLUMNS = """
    borrower_id,
    first_name,
    last_name,
    nid,
    email,
    house_no,
    street,
    city,
    postal_code
"""


class BorrowerRepository:
    """Encapsulates raw SQL queries for Borrower entity management."""

    @staticmethod
    def get_all():
        """Retrieve all borrowers ordered by borrower_id."""
        with cursor_scope() as cursor:
            cursor.execute(
                f"""
                SELECT {_BORROWER_COLUMNS}
                FROM BORROWER
                ORDER BY borrower_id
                """
            )
            return cursor.fetchall()

    @staticmethod
    def get_by_id(borrower_id: int):
        """Retrieve a single borrower by primary key ID."""
        with cursor_scope() as cursor:
            cursor.execute(
                f"""
                SELECT {_BORROWER_COLUMNS}
                FROM BORROWER
                WHERE borrower_id = %s
                """,
                (borrower_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def create(values: tuple):
        """Insert a new borrower record."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO BORROWER (
                    first_name,
                    last_name,
                    nid,
                    email,
                    house_no,
                    street,
                    city,
                    postal_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                values,
            )
            return cursor.lastrowid

    @staticmethod
    def update(values: tuple, borrower_id: int):
        """Update an existing borrower record."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE BORROWER
                SET first_name = %s,
                    last_name = %s,
                    nid = %s,
                    email = %s,
                    house_no = %s,
                    street = %s,
                    city = %s,
                    postal_code = %s
                WHERE borrower_id = %s
                """,
                (*values, borrower_id),
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT borrower_id FROM BORROWER WHERE borrower_id = %s",
                    (borrower_id,),
                )
                exists = cursor.fetchone() is not None
            else:
                exists = True
            return exists

    @staticmethod
    def delete(borrower_id: int) -> bool:
        """Delete an unreferenced borrower record."""
        with cursor_scope(commit=True) as cursor:
            cursor.execute(
                "DELETE FROM BORROWER WHERE borrower_id = %s",
                (borrower_id,),
            )
            return cursor.rowcount > 0
