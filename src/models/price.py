"""
Stock price model for historical price data.
"""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Date, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.stock import Stock


class StockPrice(Base):
    """
    Historical stock price data.
    
    Stores daily OHLCV data for each stock.
    """
    __tablename__ = "stock_price"
    __table_args__ = (
        UniqueConstraint("ticker", "date", name="uq_stock_price_ticker_date"),
        Index("idx_stock_price_ticker_date", "ticker", "date"),
        Index("idx_stock_price_date", "date"),
    )
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign key to Stock
    ticker: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("stock.ticker"),
        nullable=False
    )
    
    # Trading date
    date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # OHLCV data
    open: Mapped[float] = mapped_column(Float, nullable=True)
    high: Mapped[float] = mapped_column(Float, nullable=True)
    low: Mapped[float] = mapped_column(Float, nullable=True)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    adj_close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Relationship
    stock: Mapped["Stock"] = relationship("Stock", back_populates="prices")
    
    def __repr__(self) -> str:
        return f"<StockPrice(ticker={self.ticker}, date={self.date}, close={self.close})>"

