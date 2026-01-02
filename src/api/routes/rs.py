"""
RS (Relative Strength) API endpoints.

Provides access to RS matrix data, sub-industry history, and week summaries.
"""
from datetime import date
from typing import List, Optional

import numpy as np
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.services.data_service import (
    get_rs_matrix_data,
    get_subindustry_rs_history,
    get_week_rs_summary,
    get_latest_available_week,
)
from src.services.aggregator import get_last_friday

router = APIRouter(prefix="/rs", tags=["Relative Strength"])


# Pydantic models for response schemas
class RSMatrixItem(BaseModel):
    """Single cell in the RS matrix."""
    subindustry_code: str
    subindustry_name: str
    sector_name: str
    week_label: str
    week_end_date: date
    mansfield_rs: Optional[float]
    rs_percentile: Optional[int]
    
    class Config:
        from_attributes = True


class RSHistoryItem(BaseModel):
    """Historical RS record for a sub-industry."""
    week_end_date: date
    week_start_date: date
    rs_line: float
    rs_line_sma_52w: Optional[float]
    mansfield_rs: Optional[float]
    rs_percentile: Optional[int]
    constituents_count: int
    
    class Config:
        from_attributes = True


class RSWeekSummary(BaseModel):
    """RS summary for all sub-industries in a specific week."""
    subindustry_code: str
    subindustry_name: str
    sector_name: str
    mansfield_rs: Optional[float]
    rs_percentile: Optional[int]
    constituents_count: int
    
    class Config:
        from_attributes = True


@router.get("/matrix", response_model=List[RSMatrixItem])
def get_matrix(
    weeks: int = Query(default=17, ge=4, le=52, description="Number of weeks to include"),
    sectors: Optional[List[str]] = Query(default=None, description="Filter by sector names"),
    sort_by: str = Query(default="latest", regex="^(latest|change|sector|alpha)$"),
    db: Session = Depends(get_db)
):
    """
    Get RS matrix data for the heatmap.
    
    Returns RS percentile data for all sub-industries across specified weeks.
    
    - **weeks**: Number of weeks to include (4-52, default 17)
    - **sectors**: Optional list of sector names to filter by
    - **sort_by**: Sort method (latest, change, sector, alpha)
    """
    df = get_rs_matrix_data(
        db=db,
        num_weeks=weeks,
        sectors=sectors,
        sort_by=sort_by
    )
    
    if df.empty:
        return []
    
    # Replace NaN with None for JSON serialization
    df = df.replace({np.nan: None})
    
    # Convert to list of dicts
    records = df.to_dict(orient='records')
    return records


@router.get("/subindustry/{code}", response_model=List[RSHistoryItem])
def get_subindustry_history(
    code: str,
    weeks: int = Query(default=52, ge=4, le=104, description="Weeks of history"),
    db: Session = Depends(get_db)
):
    """
    Get RS history for a specific sub-industry.
    
    Returns weekly RS values for the specified number of weeks.
    
    - **code**: 8-digit GICS sub-industry code
    - **weeks**: Number of weeks of history (4-104, default 52)
    """
    df = get_subindustry_rs_history(db=db, subindustry_code=code, num_weeks=weeks)
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Sub-industry {code} not found or no data")
    
    records = df.to_dict(orient='records')
    return records


@router.get("/week/{week_date}", response_model=List[RSWeekSummary])
def get_week_summary(
    week_date: date,
    db: Session = Depends(get_db)
):
    """
    Get RS summary for all sub-industries for a specific week.
    
    - **week_date**: Week end date (Friday) in YYYY-MM-DD format
    """
    df = get_week_rs_summary(db=db, week_end_date=week_date)
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data for week ending {week_date}")
    
    records = df.to_dict(orient='records')
    return records


@router.get("/latest-week")
def get_latest_week(db: Session = Depends(get_db)):
    """
    Get the most recent week with available RS data.
    
    Returns:
        - latest_week: Date of the most recent week with data
        - current_week: Date of the current complete week
    """
    latest = get_latest_available_week(db)
    current = get_last_friday()
    
    return {
        "latest_week": latest,
        "current_week": current,
        "up_to_date": latest == current if latest else False
    }

