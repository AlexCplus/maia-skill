import sqlite3
import os
from pathlib import Path


def has_column(cursor: sqlite3.Cursor, table: str, column: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns


def table_exists(cursor: sqlite3.Cursor, table: str) -> bool:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cursor.fetchone() is not None


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    db_url = os.environ.get("DB_URL", "sqlite:///./autopilot.db").strip()
    if not db_url.startswith("sqlite:///"):
        print(f"Unsupported DB_URL for this migration script: {db_url}")
        return 1

    sqlite_path = db_url.replace("sqlite:///", "", 1)
    db_path = Path(sqlite_path)
    if not db_path.is_absolute():
        db_path = project_root / db_path
    db_path = db_path.resolve()

    print(f"Using DB_URL={db_url}")
    print(f"Resolved database path: {db_path}")
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return 1

    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.cursor()

        if not table_exists(cursor, "users"):
            cursor.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    email VARCHAR(256) NOT NULL UNIQUE,
                    password_hash VARCHAR(256) NOT NULL,
                    created_at DATETIME NOT NULL
                )
                """
            )
            print("Created table: users")
        else:
            print("Table users already exists")

        cursor.execute(
            """
            INSERT INTO users (email, password_hash, created_at)
            SELECT 'legacy@local', 'legacy-placeholder', datetime('now')
            WHERE NOT EXISTS (SELECT 1 FROM users)
            """
        )
        cursor.execute("SELECT id FROM users ORDER BY id ASC LIMIT 1")
        default_user_id = cursor.fetchone()[0]

        if not has_column(cursor, "portfolios", "owner_id"):
            cursor.execute("ALTER TABLE portfolios ADD COLUMN owner_id INTEGER")
            cursor.execute("UPDATE portfolios SET owner_id = ? WHERE owner_id IS NULL", (default_user_id,))
            print("Added column portfolios.owner_id and backfilled legacy rows")
        else:
            cursor.execute("UPDATE portfolios SET owner_id = ? WHERE owner_id IS NULL", (default_user_id,))
            print("Column portfolios.owner_id already exists; backfilled NULL values")

        cursor.execute("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_portfolios_owner_id ON portfolios(owner_id)")

        conn.commit()

    print("Migration completed successfully.")
    print("Next step: re-register with your real email/password via /auth/register.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

