"""
Job execution log model.

Tracks scheduled job runs for monitoring and debugging.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class JobStatus(str, Enum):
    """Job execution status."""
    STARTED = "started"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"


class JobLog(Base):
    """
    Job execution tracking.
    
    Records each scheduled job run with timing, status, and any errors.
    """
    __tablename__ = "job_log"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Job identification
    job_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[JobStatus] = mapped_column(
        SQLEnum(JobStatus),
        nullable=False,
        default=JobStatus.STARTED
    )
    
    # Results
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional metadata (JSON string)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return (
            f"<JobLog(job={self.job_name}, status={self.status}, "
            f"started={self.started_at})>"
        )

