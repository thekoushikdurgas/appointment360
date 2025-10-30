"""
Database configuration and initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager
from pathlib import Path
import os

# Import settings
from config.settings import (
    BASE_DIR,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    DATABASE_URL
)

# PostgreSQL Configuration Only
# Use DATABASE_URL from settings if available, otherwise construct it
db_url = DATABASE_URL if DATABASE_URL else f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(
    db_url,
    pool_size=20,  # Increase connection pool for better performance
    max_overflow=40,
    pool_pre_ping=True,  # Verify connections before using
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    This should be called once during application startup
    """
    # Import all models here so they're registered with Base
    from models.contact import Contact
    from models.export_log import ExportLog
    from models.user import User
    from models.import_job import ImportJob  # Import job model
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully (PostgreSQL)")


def drop_db():
    """
    Drop all tables (use with caution!)
    """
    Base.metadata.drop_all(bind=engine)


def reset_db():
    """
    Drop and recreate all tables
    """
    drop_db()
    init_db()

