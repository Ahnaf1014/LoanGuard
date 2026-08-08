"""Create a local logical backup without exposing the configured password."""

import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from config import Config  # noqa: E402


def main():
    mysqldump = shutil.which("mysqldump")
    if not mysqldump:
        raise RuntimeError("mysqldump is not installed or is not on PATH")

    backup_dir = PROJECT_ROOT / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_path = backup_dir / f"{Config.DB_NAME}-{timestamp}.sql"

    command = [
        mysqldump,
        f"--host={Config.DB_HOST}",
        f"--port={Config.DB_PORT}",
        f"--user={Config.DB_USER}",
        "--single-transaction",
        "--routines",
        "--triggers",
        "--events",
        "--set-gtid-purged=OFF",
        "--default-character-set=utf8mb4",
        f"--result-file={backup_path}",
        Config.DB_NAME,
    ]
    if Config.DB_SSL:
        command.insert(-1, "--ssl-mode=REQUIRED")

    environment = os.environ.copy()
    environment["MYSQL_PWD"] = Config.DB_PASSWORD
    subprocess.run(command, check=True, env=environment)
    print(f"Backup created: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
