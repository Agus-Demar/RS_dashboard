"""
Data service layer for dashboard queries.

Provides functions to retrieve RS data formatted for the dashboard.
"""
import logging
from datetime import date, timedelta
from typing import List, Optional

import pandas as pd
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.config import settings
from src.models import RSWeekly, GICSSubIndustry, Stock
from src.services.aggregator import get_last_friday, get_week_ranges

logger = logging.getLogger(__name__)


def get_rs_matrix_data(
    db: Session,
    num_weeks: int = None,
    sectors: Optional[List[str]] = None,
    sort_by: str = "latest"
) -> pd.DataFrame:
    """
    Get RS data formatted as a matrix for the heatmap.
    
    Args:
        db: Database session
        num_weeks: Number of weeks to include (default from settings)
        sectors: Optional list of sector names to filter by
        sort_by: Sort method - 'latest', 'change', 'sector', or 'alpha'
    
    Returns:
        DataFrame with columns:
        - subindustry_code
        - subindustry_name
        - sector_name
        - week_label
        - week_end_date
        - mansfield_rs
        - rs_percentile
    """
    if num_weeks is None:
        num_weeks = settings.DEFAULT_WEEKS_DISPLAY
    
    # Get week ranges
    week_ranges = get_week_ranges(months_back=num_weeks / 4.33)[:num_weeks]
    
    if not week_ranges:
        return pd.DataFrame()
    
    # Get date range
    oldest_week = week_ranges[-1]['week_end']
    newest_week = week_ranges[0]['week_end']
    
    # Build query
    query = db.query(
        RSWeekly.subindustry_code,
        RSWeekly.week_end_date,
        RSWeekly.mansfield_rs,
        RSWeekly.rs_percentile,
        RSWeekly.constituents_count,
        GICSSubIndustry.name.label('subindustry_name'),
        GICSSubIndustry.sector_name,
        GICSSubIndustry.sector_code,
    ).join(
        GICSSubIndustry,
        RSWeekly.subindustry_code == GICSSubIndustry.code
    ).filter(
        RSWeekly.week_end_date >= oldest_week,
        RSWeekly.week_end_date <= newest_week
    )
    
    # Apply sector filter
    if sectors:
        query = query.filter(GICSSubIndustry.sector_name.in_(sectors))
    
    # Execute query
    results = query.all()
    
    if not results:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=[
        'subindustry_code',
        'week_end_date',
        'mansfield_rs',
        'rs_percentile',
        'constituents_count',
        'subindustry_name',
        'sector_name',
        'sector_code',
    ])
    
    # Create week labels
    week_label_map = {w['week_end']: w['label'] for w in week_ranges}
    df['week_label'] = df['week_end_date'].map(week_label_map)
    
    # Sort subindustries
    df = _sort_subindustries(df, sort_by)
    
    return df


def _sort_subindustries(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """Sort DataFrame by specified method."""
    if df.empty:
        return df
    
    if sort_by == "latest":
        # Sort by most recent week's RS percentile
        latest_week = df['week_end_date'].max()
        latest_data = df[df['week_end_date'] == latest_week].set_index('subindustry_code')
        sort_order = latest_data['rs_percentile'].sort_values(ascending=False).index.tolist()
        
        # Create category type for sorting
        df['sort_key'] = pd.Categorical(
            df['subindustry_code'],
            categories=sort_order,
            ordered=True
        )
        df = df.sort_values('sort_key').drop('sort_key', axis=1)
        
    elif sort_by == "change":
        # Sort by 4-week RS change
        weeks = sorted(df['week_end_date'].unique(), reverse=True)
        if len(weeks) >= 4:
            newest = weeks[0]
            oldest = weeks[3]
            
            newest_data = df[df['week_end_date'] == newest].set_index('subindustry_code')
            oldest_data = df[df['week_end_date'] == oldest].set_index('subindustry_code')
            
            change = newest_data['rs_percentile'] - oldest_data['rs_percentile']
            sort_order = change.sort_values(ascending=False).index.tolist()
            
            df['sort_key'] = pd.Categorical(
                df['subindustry_code'],
                categories=sort_order,
                ordered=True
            )
            df = df.sort_values('sort_key').drop('sort_key', axis=1)
            
    elif sort_by == "sector":
        # Group by sector, then alphabetical within sector
        df = df.sort_values(['sector_name', 'subindustry_name'])
        
    else:  # 'alpha' or default
        # Alphabetical by sub-industry name
        df = df.sort_values('subindustry_name')
    
    return df


def get_subindustry_rs_history(
    db: Session,
    subindustry_code: str,
    num_weeks: int = 52
) -> pd.DataFrame:
    """
    Get RS history for a specific sub-industry.
    
    Args:
        db: Database session
        subindustry_code: GICS sub-industry code
        num_weeks: Number of weeks of history
    
    Returns:
        DataFrame with weekly RS data
    """
    # Get subindustry info
    subindustry = db.query(GICSSubIndustry).filter(
        GICSSubIndustry.code == subindustry_code
    ).first()
    
    if not subindustry:
        return pd.DataFrame()
    
    # Calculate date range
    end_date = get_last_friday()
    start_date = end_date - timedelta(weeks=num_weeks)
    
    # Query RS data
    results = db.query(RSWeekly).filter(
        RSWeekly.subindustry_code == subindustry_code,
        RSWeekly.week_end_date >= start_date,
        RSWeekly.week_end_date <= end_date
    ).order_by(desc(RSWeekly.week_end_date)).all()
    
    if not results:
        return pd.DataFrame()
    
    # Convert to DataFrame
    data = [{
        'week_end_date': r.week_end_date,
        'week_start_date': r.week_start_date,
        'rs_line': r.rs_line,
        'rs_line_sma_52w': r.rs_line_sma_52w,
        'mansfield_rs': r.mansfield_rs,
        'rs_percentile': r.rs_percentile,
        'constituents_count': r.constituents_count,
        'subindustry_name': subindustry.name,
        'sector_name': subindustry.sector_name,
    } for r in results]
    
    return pd.DataFrame(data)


def get_week_rs_summary(
    db: Session,
    week_end_date: date
) -> pd.DataFrame:
    """
    Get RS summary for all sub-industries for a specific week.
    
    Args:
        db: Database session
        week_end_date: Friday of the target week
    
    Returns:
        DataFrame with RS data for all sub-industries
    """
    results = db.query(
        RSWeekly,
        GICSSubIndustry.name.label('subindustry_name'),
        GICSSubIndustry.sector_name,
    ).join(
        GICSSubIndustry,
        RSWeekly.subindustry_code == GICSSubIndustry.code
    ).filter(
        RSWeekly.week_end_date == week_end_date
    ).order_by(desc(RSWeekly.rs_percentile)).all()
    
    if not results:
        return pd.DataFrame()
    
    data = [{
        'subindustry_code': r.RSWeekly.subindustry_code,
        'subindustry_name': r.subindustry_name,
        'sector_name': r.sector_name,
        'mansfield_rs': r.RSWeekly.mansfield_rs,
        'rs_percentile': r.RSWeekly.rs_percentile,
        'constituents_count': r.RSWeekly.constituents_count,
    } for r in results]
    
    return pd.DataFrame(data)


def get_available_sectors(db: Session) -> List[str]:
    """
    Get list of available GICS sectors.
    
    Args:
        db: Database session
    
    Returns:
        List of sector names
    """
    sectors = db.query(GICSSubIndustry.sector_name).distinct().order_by(
        GICSSubIndustry.sector_name
    ).all()
    
    return [s[0] for s in sectors]


def get_subindustry_stocks(
    db: Session,
    subindustry_code: str
) -> List[dict]:
    """
    Get stocks belonging to a sub-industry.
    
    Args:
        db: Database session
        subindustry_code: GICS sub-industry code
    
    Returns:
        List of stock dicts with ticker, name, market_cap
    """
    stocks = db.query(Stock).filter(
        Stock.gics_subindustry_code == subindustry_code,
        Stock.is_active == True
    ).order_by(desc(Stock.market_cap)).all()
    
    return [{
        'ticker': s.ticker,
        'name': s.name,
        'market_cap': s.market_cap,
    } for s in stocks]


def get_latest_available_week(db: Session) -> Optional[date]:
    """
    Get the most recent week with RS data.
    
    Args:
        db: Database session
    
    Returns:
        Date of the most recent week_end_date with data
    """
    result = db.query(RSWeekly.week_end_date).order_by(
        desc(RSWeekly.week_end_date)
    ).first()
    
    return result[0] if result else None


def get_data_stats(db: Session) -> dict:
    """
    Get statistics about available data.
    
    Args:
        db: Database session
    
    Returns:
        Dict with counts and dates
    """
    from src.models import StockPrice
    
    subindustry_count = db.query(GICSSubIndustry).count()
    stock_count = db.query(Stock).filter(Stock.is_active == True).count()
    price_count = db.query(StockPrice).count()
    rs_count = db.query(RSWeekly).count()
    
    latest_week = get_latest_available_week(db)
    
    # Get date range of prices
    oldest_price = db.query(StockPrice.date).order_by(StockPrice.date).first()
    newest_price = db.query(StockPrice.date).order_by(desc(StockPrice.date)).first()
    
    return {
        'subindustry_count': subindustry_count,
        'stock_count': stock_count,
        'price_count': price_count,
        'rs_record_count': rs_count,
        'latest_rs_week': latest_week,
        'oldest_price_date': oldest_price[0] if oldest_price else None,
        'newest_price_date': newest_price[0] if newest_price else None,
    }

