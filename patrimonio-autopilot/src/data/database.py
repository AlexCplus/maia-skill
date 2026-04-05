import os
from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker


DB_URL = os.environ.get("DB_URL", "sqlite:///./autopilot.db").strip()
IS_SQLITE = DB_URL.startswith("sqlite")

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    from src.data import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    if IS_SQLITE:
        _migrate_sqlite_legacy_schema()


def _migrate_sqlite_legacy_schema() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "portfolios" not in table_names:
        return

    with engine.begin() as conn:
        if "users" not in table_names:
            conn.execute(
                text(
                    """
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY,
                        email VARCHAR(256) NOT NULL UNIQUE,
                        password_hash VARCHAR(256) NOT NULL,
                        created_at DATETIME NOT NULL
                    )
                    """
                )
            )
            conn.execute(
                text(
                    """
                    INSERT INTO users (email, password_hash, created_at)
                    VALUES ('legacy@local', 'legacy-placeholder', CURRENT_TIMESTAMP)
                    """
                )
            )

        portfolio_columns = {c["name"] for c in inspect(engine).get_columns("portfolios")}
        if "owner_id" not in portfolio_columns:
            conn.execute(text("ALTER TABLE portfolios ADD COLUMN owner_id INTEGER"))

        default_user_id = conn.execute(text("SELECT id FROM users ORDER BY id ASC LIMIT 1")).scalar_one()
        conn.execute(
            text("UPDATE portfolios SET owner_id = :owner_id WHERE owner_id IS NULL"),
            {"owner_id": int(default_user_id)},
        )
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_portfolios_owner_id ON portfolios(owner_id)"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

