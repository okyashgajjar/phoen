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

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dealflow360.db")

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("APP_DEBUG", "false").lower() == "true",
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

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
