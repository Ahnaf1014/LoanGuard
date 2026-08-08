"""Read-only health check for the configured LoanGuard MySQL database."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from database.connection import cursor_scope  # noqa: E402

EXPECTED_TABLES = {
    "bank_staff",
    "bank_staff_phone",
    "borrower",
    "borrower_phone",
    "business_loan",
    "credit_assessment",
    "home_loan",
    "loan",
    "loan_application",
    "loan_payment",
    "personal_loan",
}

EXPECTED_TRIGGERS = {
    "trg_validate_loan_application",
    "trg_validate_loan_application_update",
    "trg_protect_funded_application",
    "trg_validate_payment_insert",
    "trg_update_loan_balance_insert",
    "trg_validate_payment_update",
    "trg_update_loan_balance_update",
    "trg_update_loan_balance_delete",
}


def main():
    failures = []

    with cursor_scope() as cursor:
        cursor.execute("SELECT DATABASE() AS name, VERSION() AS version")
        server = cursor.fetchone()

        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE'
            """
        )
        # Table-name casing varies with MySQL's lower_case_table_names setting.
        tables = {row["TABLE_NAME"].casefold() for row in cursor.fetchall()}

        cursor.execute(
            """
            SELECT trigger_name
            FROM information_schema.triggers
            WHERE trigger_schema = DATABASE()
            """
        )
        triggers = {row["TRIGGER_NAME"].casefold() for row in cursor.fetchall()}

        if EXPECTED_TABLES.issubset(tables):
            checks = {
                "invalid application decisions": """
                    SELECT COUNT(*) AS total
                    FROM LOAN_APPLICATION
                    WHERE (
                        application_status IN ('Approved', 'Rejected')
                        AND (manager_id IS NULL OR decision_date IS NULL)
                    ) OR (
                        application_status IN ('Pending', 'Under Review')
                        AND (manager_id IS NOT NULL OR decision_date IS NOT NULL)
                    )
                """,
                "invalid loan-officer roles": """
                    SELECT COUNT(*) AS total
                    FROM LOAN_APPLICATION AS la
                    JOIN BANK_STAFF AS s ON la.loan_officer_id = s.staff_id
                    WHERE s.role <> 'LoanOfficer'
                """,
                "invalid analyst roles": """
                    SELECT COUNT(*) AS total
                    FROM CREDIT_ASSESSMENT AS ca
                    JOIN BANK_STAFF AS s ON ca.analyst_id = s.staff_id
                    WHERE s.role <> 'CreditAnalyst'
                """,
                "invalid manager roles": """
                    SELECT COUNT(*) AS total
                    FROM LOAN_APPLICATION AS la
                    JOIN BANK_STAFF AS s ON la.manager_id = s.staff_id
                    WHERE s.role <> 'BranchManager'
                """,
                "invalid loan balances": """
                    SELECT COUNT(*) AS total
                    FROM LOAN
                    WHERE current_balance < 0 OR current_balance > approved_amount
                """,
            }
            for label, query in checks.items():
                cursor.execute(query)
                total = cursor.fetchone()["total"]
                if total:
                    failures.append(f"{label}: {total}")

    missing_tables = sorted(EXPECTED_TABLES - tables)
    if missing_tables:
        failures.append(f"missing tables: {', '.join(missing_tables)}")
    missing_triggers = sorted(EXPECTED_TRIGGERS - triggers)
    if missing_triggers:
        failures.append(f"missing triggers: {', '.join(missing_triggers)}")

    print(f"Database: {server['name']}")
    print(f"MySQL: {server['version']}")
    print(f"Tables: {len(tables)}; triggers: {len(triggers)}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("Database health check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
