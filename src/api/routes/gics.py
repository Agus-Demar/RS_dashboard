"""
GICS (Global Industry Classification Standard) API endpoints.

Provides access to GICS sectors, sub-industries, and their constituents.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.models import GICSSubIndustry, Stock
from src.services.data_service import get_available_sectors, get_subindustry_stocks

router = APIRouter(prefix="/gics", tags=["GICS Classification"])


class SectorResponse(BaseModel):
    """GICS Sector."""
    code: str
    name: str


class SubIndustryResponse(BaseModel):
    """GICS Sub-Industry details."""
    code: str
    name: str
    industry_code: str
    industry_name: str
    industry_group_code: str
    industry_group_name: str
    sector_code: str
    sector_name: str
    stock_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class StockResponse(BaseModel):
    """Stock in a sub-industry."""
    ticker: str
    name: str
    market_cap: Optional[float]
    
    class Config:
        from_attributes = True


@router.get("/sectors", response_model=List[str])
def list_sectors(db: Session = Depends(get_db)):
    """
    Get list of all available GICS sectors.
    
    Returns a list of sector names.
    """
    sectors = get_available_sectors(db)
    return sectors


@router.get("/subindustries", response_model=List[SubIndustryResponse])
def list_subindustries(
    sector: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of all GICS sub-industries.
    
    Optionally filter by sector name.
    
    - **sector**: Optional sector name to filter by
    """
    query = db.query(GICSSubIndustry)
    
    if sector:
        query = query.filter(GICSSubIndustry.sector_name == sector)
    
    subindustries = query.order_by(GICSSubIndustry.sector_name, GICSSubIndustry.name).all()
    
    # Add stock count
    result = []
    for sub in subindustries:
        stock_count = db.query(Stock).filter(
            Stock.gics_subindustry_code == sub.code,
            Stock.is_active == True
        ).count()
        
        result.append(SubIndustryResponse(
            code=sub.code,
            name=sub.name,
            industry_code=sub.industry_code,
            industry_name=sub.industry_name,
            industry_group_code=sub.industry_group_code,
            industry_group_name=sub.industry_group_name,
            sector_code=sub.sector_code,
            sector_name=sub.sector_name,
            stock_count=stock_count
        ))
    
    return result


@router.get("/subindustry/{code}", response_model=SubIndustryResponse)
def get_subindustry(code: str, db: Session = Depends(get_db)):
    """
    Get details for a specific sub-industry.
    
    - **code**: 8-digit GICS sub-industry code
    """
    subindustry = db.query(GICSSubIndustry).filter(
        GICSSubIndustry.code == code
    ).first()
    
    if not subindustry:
        raise HTTPException(status_code=404, detail=f"Sub-industry {code} not found")
    
    stock_count = db.query(Stock).filter(
        Stock.gics_subindustry_code == code,
        Stock.is_active == True
    ).count()
    
    return SubIndustryResponse(
        code=subindustry.code,
        name=subindustry.name,
        industry_code=subindustry.industry_code,
        industry_name=subindustry.industry_name,
        industry_group_code=subindustry.industry_group_code,
        industry_group_name=subindustry.industry_group_name,
        sector_code=subindustry.sector_code,
        sector_name=subindustry.sector_name,
        stock_count=stock_count
    )


@router.get("/subindustry/{code}/stocks", response_model=List[StockResponse])
def get_stocks_in_subindustry(code: str, db: Session = Depends(get_db)):
    """
    Get stocks belonging to a sub-industry.
    
    Returns stocks sorted by market cap (descending).
    
    - **code**: 8-digit GICS sub-industry code
    """
    # Verify sub-industry exists
    subindustry = db.query(GICSSubIndustry).filter(
        GICSSubIndustry.code == code
    ).first()
    
    if not subindustry:
        raise HTTPException(status_code=404, detail=f"Sub-industry {code} not found")
    
    stocks = get_subindustry_stocks(db, code)
    return stocks

