"""
StockCharts Industry model.

Industry classification based on StockCharts.com sector drill-down structure:
- Sector (11 sectors, 2-digit code)
- Industry (130 industries, 6-digit code)

This replaces the previous GICS-based 8-digit sub-industry codes with
StockCharts-compatible 6-digit industry codes for RS/SCTR calculation.
"""
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.stock import Stock
    from src.models.rs_weekly import RSWeekly


class GICSSubIndustry(Base):
    """
    StockCharts Industry classification.
    
    Uses 6-digit StockCharts industry codes (e.g., "350100" for Biotechnology)
    for consistent RS and SCTR calculations.
    """
    __tablename__ = "gics_subindustry"
    
    # Primary key: 6-digit StockCharts industry code (e.g., "350100")
    code: Mapped[str] = mapped_column(String(6), primary_key=True)
    
    # Sub-industry name
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Industry (6-digit code)
    industry_code: Mapped[str] = mapped_column(String(6), nullable=False)
    industry_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Industry Group (4-digit code)
    industry_group_code: Mapped[str] = mapped_column(String(4), nullable=False)
    industry_group_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Sector (2-digit code)
    sector_code: Mapped[str] = mapped_column(String(2), nullable=False)
    sector_name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Relationships
    stocks: Mapped[List["Stock"]] = relationship(
        "Stock",
        back_populates="gics_subindustry",
        lazy="dynamic"
    )
    rs_weekly_records: Mapped[List["RSWeekly"]] = relationship(
        "RSWeekly",
        back_populates="subindustry",
        lazy="dynamic"
    )
    
    def __repr__(self) -> str:
        return f"<GICSSubIndustry(code={self.code}, name={self.name})>"

