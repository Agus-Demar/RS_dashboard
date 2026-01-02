"""
GICS Sub-Industry model.

Global Industry Classification Standard (GICS) hierarchy:
- Sector (11 sectors, 2-digit code)
- Industry Group (25 groups, 4-digit code)
- Industry (74 industries, 6-digit code)
- Sub-Industry (163 sub-industries, 8-digit code)
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
    GICS Sub-Industry classification.
    
    This is the most granular level of the GICS hierarchy.
    Each sub-industry belongs to an industry, industry group, and sector.
    """
    __tablename__ = "gics_subindustry"
    
    # Primary key: 8-digit GICS code (e.g., "10101010")
    code: Mapped[str] = mapped_column(String(8), primary_key=True)
    
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

