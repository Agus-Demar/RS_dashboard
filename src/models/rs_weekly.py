"""
Weekly Relative Strength model.

Stores calculated Mansfield RS values for each GICS sub-industry per week.
"""
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Float, Integer, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.gics import GICSSubIndustry


class RSWeekly(Base, TimestampMixin):
    """
    Weekly Mansfield RS calculations per sub-industry.
    
    This is the core table for dashboard visualization.
    Each record represents one sub-industry's RS for one week.
    """
    __tablename__ = "rs_weekly"
    __table_args__ = (
        UniqueConstraint(
            "subindustry_code", "week_end_date",
            name="uq_rs_subindustry_week"
        ),
        Index("idx_rs_weekly_week_end", "week_end_date"),
        Index("idx_rs_weekly_subindustry", "subindustry_code"),
    )
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to GICS sub-industry
    subindustry_code: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("gics_subindustry.code"),
        nullable=False
    )
    
    # Week boundaries
    week_end_date: Mapped[date] = mapped_column(Date, nullable=False)  # Friday
    week_start_date: Mapped[date] = mapped_column(Date, nullable=False)  # Monday
    
    # Mansfield RS components
    rs_line: Mapped[float] = mapped_column(Float, nullable=False)
    rs_line_sma_52w: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    mansfield_rs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Percentile rank (0-100) for color coding
    rs_percentile: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Aggregation metadata
    constituents_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_market_cap: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Relationship
    subindustry: Mapped["GICSSubIndustry"] = relationship(
        "GICSSubIndustry",
        back_populates="rs_weekly_records"
    )
    
    def __repr__(self) -> str:
        return (
            f"<RSWeekly(subindustry={self.subindustry_code}, "
            f"week={self.week_end_date}, rs={self.mansfield_rs})>"
        )

