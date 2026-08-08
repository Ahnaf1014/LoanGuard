"""Apply trusted repository SQL files using the configured MySQL connection."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = (PROJECT_ROOT / "database").resolve()
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from database.connection import get_connection  # noqa: E402


def statements(sql_path):
    """Yield statements while honoring mysql-client DELIMITER directives."""

    delimiter = ";"
    buffer = []

    with sql_path.open(encoding="utf-8") as sql_file:
        for raw_line in sql_file:
            stripped = raw_line.strip()
            if stripped.upper().startswith("DELIMITER "):
                if buffer and "".join(buffer).strip():
                    raise ValueError("DELIMITER changed in the middle of a statement")
                delimiter = stripped.split(maxsplit=1)[1]
                continue

            buffer.append(raw_line)
            combined = "".join(buffer).rstrip()
            if combined.endswith(delimiter):
                statement = combined[: -len(delimiter)].strip()
                if statement:
                    yield statement
                buffer = []

    if "".join(buffer).strip():
        raise ValueError(f"Unterminated SQL statement in {sql_path}")


def trusted_path(raw_path):
    sql_path = (PROJECT_ROOT / raw_path).resolve()
    if DATABASE_DIR not in sql_path.parents or sql_path.suffix.lower() != ".sql":
        raise ValueError("SQL files must be inside the repository database directory")
    if not sql_path.is_file():
        raise ValueError(f"SQL file does not exist: {sql_path}")
    return sql_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files", nargs="+", help="SQL files relative to the project root"
    )
    parser.add_argument(
        "--yes", action="store_true", help="confirm that database changes are intended"
    )
    args = parser.parse_args()

    if not args.yes:
        parser.error("refusing to modify the database without --yes")

    sql_paths = [trusted_path(path) for path in args.files]
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for sql_path in sql_paths:
                count = 0
                for statement in statements(sql_path):
                    cursor.execute(statement)
                    count += 1
                relative_path = sql_path.relative_to(PROJECT_ROOT)
                print(f"Applied {relative_path} ({count} statements)")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
