"""
API dependencies.

Provides dependency injection for database sessions and other shared resources.
"""
from typing import Generator

from sqlalchemy.orm import Session

from src.models import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    
    Yields:
        SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

