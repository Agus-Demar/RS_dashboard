"""
Health check and system status endpoints.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.services.data_service import get_data_stats

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str = "1.0.0"


class DataStatsResponse(BaseModel):
    """Data statistics response."""
    subindustry_count: int
    stock_count: int
    price_count: int
    rs_record_count: int
    latest_rs_week: Optional[str]
    oldest_price_date: Optional[str]
    newest_price_date: Optional[str]


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Basic health check endpoint.
    
    Returns service status and version.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@router.get("/api/status", response_model=DataStatsResponse)
def get_status(db: Session = Depends(get_db)):
    """
    Get detailed system status and data statistics.
    
    Returns counts of records and date ranges.
    """
    stats = get_data_stats(db)
    
    return DataStatsResponse(
        subindustry_count=stats['subindustry_count'],
        stock_count=stats['stock_count'],
        price_count=stats['price_count'],
        rs_record_count=stats['rs_record_count'],
        latest_rs_week=str(stats['latest_rs_week']) if stats['latest_rs_week'] else None,
        oldest_price_date=str(stats['oldest_price_date']) if stats['oldest_price_date'] else None,
        newest_price_date=str(stats['newest_price_date']) if stats['newest_price_date'] else None,
    )

