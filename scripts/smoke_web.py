"""Read-only smoke test for every implemented HTML page."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app import app  # noqa: E402

PATHS = (
    "/",
    "/borrowers",
    "/borrowers/add",
    "/applications",
    "/applications/add",
    "/assessments",
    "/assessments/add",
)


def main():
    failures = []
    app.config["TESTING"] = True

    with app.test_client() as client:
        for path in PATHS:
            response = client.get(path)
            print(f"{response.status_code} GET {path}")
            if response.status_code != 200:
                failures.append(path)

    if failures:
        print(f"Failed pages: {', '.join(failures)}")
        return 1
    print("Web smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
