"""
SQLAlchemy base configuration and database setup.
"""
from datetime import datetime
from typing import Generator

from sqlalchemy import create_engine, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


# Create engine
engine = create_engine(
    settings.db_url,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.db_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Dependency for getting database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database by creating all tables."""
    # Import all models to ensure they're registered
    from src.models import gics, stock, price, rs_weekly, job_log  # noqa: F401
    
    Base.metadata.create_all(bind=engine)

