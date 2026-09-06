"""
DealFlow360 — Database Configuration

Central database connection management using SQLAlchemy 2.0.
Supports PostgreSQL with connection pooling and session management.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_FILE = os.path.join(ROOT_DIR, "dealflow360.db")

raw_db_url = os.getenv("DATABASE_URL", "")

def _init_engine():
    global raw_db_url
    if raw_db_url.startswith("postgresql"):
        try:
            pg_engine = create_engine(
                raw_db_url,
                echo=os.getenv("APP_DEBUG", "false").lower() == "true",
                pool_size=10,
                max_overflow=20
            )
            with pg_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return pg_engine, raw_db_url
        except Exception as e:
            # Fall back to sqlite if PostgreSQL server is unreachable
            pass

    # SQLite. Honour an explicit sqlite:// DATABASE_URL so the app can be
    # pointed at a copy of the database (tests, a scratch run, a second
    # demo dataset) instead of always hard-binding to the repo root file.
    if raw_db_url.startswith("sqlite"):
        resolved_url = raw_db_url
        if resolved_url.startswith("sqlite:///./"):
            # A relative URL is relative to the project root, not the cwd.
            rel = resolved_url.replace("sqlite:///./", "")
            resolved_url = f"sqlite:///{os.path.join(ROOT_DIR, rel)}".replace("\\", "/")
    else:
        sqlite_path = DEFAULT_DB_FILE.replace("\\", "/")
        resolved_url = f"sqlite:///{sqlite_path}"
    sqlite_engine = create_engine(
        resolved_url,
        echo=os.getenv("APP_DEBUG", "false").lower() == "true",
        connect_args={"check_same_thread": False}
    )
    return sqlite_engine, resolved_url

engine, DATABASE_URL = _init_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Session:
    """FastAPI dependency — yields a database session and ensures cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health() -> dict:
    """Verify database connectivity and return diagnostic info."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            result2 = conn.execute(text("SELECT current_database()"))
            db_name = result2.scalar()
            return {
                "status": "healthy",
                "database": db_name,
                "engine": version,
                "pool_size": engine.pool.size(),
                "pool_checked_in": engine.pool.checkedin(),
                "pool_checked_out": engine.pool.checkedout(),
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }
