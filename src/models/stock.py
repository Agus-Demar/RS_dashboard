"""
Stock model for tracking individual securities.
"""
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.gics import GICSSubIndustry
    from src.models.price import StockPrice


class Stock(Base, TimestampMixin):
    """
    Stock master data.
    
    Tracks individual securities with their GICS classification
    and current market cap.
    """
    __tablename__ = "stock"
    
    # Primary key: ticker symbol (e.g., "AAPL")
    ticker: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    # Company name
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # GICS classification
    gics_subindustry_code: Mapped[str] = mapped_column(
        ForeignKey("gics_subindustry.code"),
        nullable=False,
        index=True
    )
    
    # Market capitalization (latest)
    market_cap: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Whether this stock is actively tracked
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    gics_subindustry: Mapped["GICSSubIndustry"] = relationship(
        "GICSSubIndustry",
        back_populates="stocks"
    )
    prices: Mapped[List["StockPrice"]] = relationship(
        "StockPrice",
        back_populates="stock",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Stock(ticker={self.ticker}, name={self.name})>"

