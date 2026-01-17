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
    
    # Get actual available week_end_dates from the database (most recent first)
    available_weeks = db.query(RSWeekly.week_end_date).distinct().order_by(
        desc(RSWeekly.week_end_date)
    ).limit(num_weeks).all()
    
    if not available_weeks:
        return pd.DataFrame()
    
    # Extract dates and determine range
    week_dates = [w[0] for w in available_weeks]
    newest_week = week_dates[0]
    oldest_week = week_dates[-1]
    
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
    
    # Create week labels from actual data (format: DD/MM/YY)
    df['week_label'] = df['week_end_date'].apply(lambda d: d.strftime("%d/%m/%y"))
    
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


def get_sector_rs_matrix_data(
    db: Session,
    num_weeks: int = None,
    sort_by: str = "latest"
) -> pd.DataFrame:
    """
    Get sector-level RS data calculated from sector ETFs (XL* series) for the sector heatmap.
    
    Calculates Mansfield RS for each sector ETF (XLE, XLB, XLI, etc.) vs SPY benchmark,
    then ranks them as percentiles across all sectors for each week.
    
    Args:
        db: Database session
        num_weeks: Number of weeks to include (default from settings)
        sort_by: Sort method - 'latest', 'change', or 'alpha'
    
    Returns:
        DataFrame with columns:
        - sector_code
        - sector_name
        - week_label
        - week_end_date
        - rs_percentile (from sector ETF Mansfield RS)
        - subindustry_count (set to 0 for ETF-based calculation)
    """
    from src.config import settings
    from src.models import StockPrice
    from src.services.rs_calculator import MansfieldRSCalculator
    import numpy as np
    
    if num_weeks is None:
        num_weeks = settings.DEFAULT_WEEKS_DISPLAY
    
    # Sector ETF mapping (sector_name -> ETF ticker)
    SECTOR_ETFS = {
        "Energy": ("10", "XLE"),
        "Materials": ("15", "XLB"),
        "Industrials": ("20", "XLI"),
        "Consumer Discretionary": ("25", "XLY"),
        "Consumer Staples": ("30", "XLP"),
        "Health Care": ("35", "XLV"),
        "Financials": ("40", "XLF"),
        "Information Technology": ("45", "XLK"),
        "Communication Services": ("50", "XLC"),
        "Utilities": ("55", "XLU"),
        "Real Estate": ("60", "XLRE"),
    }
    
    # Calculate date range - use latest complete week from RS data for consistency
    latest_rs_week = get_latest_available_week(db)
    if not latest_rs_week:
        logger.warning("No RS data available in database")
        return pd.DataFrame()
    
    end_date = latest_rs_week
    # Need at least 52 weeks of history for Mansfield RS calculation
    start_date = end_date - timedelta(weeks=num_weeks + 60)
    
    # Get benchmark prices (SPY)
    benchmark_ticker = settings.BENCHMARK_TICKER
    benchmark_prices_query = db.query(StockPrice).filter(
        StockPrice.ticker == benchmark_ticker,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not benchmark_prices_query:
        logger.warning(f"No benchmark prices found for {benchmark_ticker}")
        return pd.DataFrame()
    
    benchmark_prices = pd.Series(
        {p.date: p.adj_close for p in benchmark_prices_query}
    ).sort_index()
    
    # Get week end dates (Fridays) for the requested period
    # Generate week end dates directly instead of using get_week_ranges
    # (which expects months_back and may not give exact num_weeks)
    week_end_dates = []
    current_friday = end_date
    for i in range(num_weeks):
        week_end_dates.append(current_friday - timedelta(weeks=i))
    week_end_dates.reverse()  # Oldest first for consistent ordering
    
    # Initialize RS calculator
    rs_calc = MansfieldRSCalculator()
    
    # Calculate Mansfield RS for each sector ETF
    sector_rs_data = []
    
    for sector_name, (sector_code, etf_ticker) in SECTOR_ETFS.items():
        # Get ETF prices
        etf_prices_query = db.query(StockPrice).filter(
            StockPrice.ticker == etf_ticker,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        if not etf_prices_query:
            logger.warning(f"No prices found for sector ETF {etf_ticker} ({sector_name})")
            continue
        
        etf_prices = pd.Series(
            {p.date: p.adj_close for p in etf_prices_query}
        ).sort_index()
        
        # Calculate full Mansfield RS history
        rs_result = rs_calc.calculate_full(etf_prices, benchmark_prices)
        
        if rs_result.empty:
            logger.warning(f"Could not calculate RS for {etf_ticker} ({sector_name})")
            continue
        
        # Extract Mansfield RS for each week end date
        for week_end in week_end_dates:
            # Find the closest date <= week_end in the RS result
            valid_dates = rs_result.index[rs_result.index <= week_end]
            if len(valid_dates) == 0:
                continue
            
            closest_date = valid_dates[-1]
            mansfield_rs = rs_result.loc[closest_date, 'mansfield_rs']
            
            if pd.notna(mansfield_rs):
                sector_rs_data.append({
                    'sector_code': sector_code,
                    'sector_name': sector_name,
                    'week_end_date': week_end,
                    'mansfield_rs': mansfield_rs,
                    'etf_ticker': etf_ticker,
                })
    
    if not sector_rs_data:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(sector_rs_data)
    
    # Calculate percentile ranks within each week using transform
    # rank(pct=True) gives values from 0 to 1, multiply by 100 for percentile
    df['rs_percentile'] = df.groupby('week_end_date')['mansfield_rs'].transform(
        lambda x: x.rank(pct=True) * 100
    ).round().astype(int)
    
    # Add subindustry_count (0 for ETF-based calculation)
    df['subindustry_count'] = 0
    
    # Create week labels from actual data (format: DD/MM/YY)
    df['week_label'] = df['week_end_date'].apply(lambda d: d.strftime("%d/%m/%y"))
    
    # Drop the intermediate mansfield_rs column (keep only percentile for heatmap)
    df = df.drop(columns=['mansfield_rs', 'etf_ticker'])
    
    # Sort sectors
    df = _sort_sectors(df, sort_by)
    
    return df


def _sort_sectors(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """Sort sector DataFrame by specified method."""
    if df.empty:
        return df
    
    # Get all unique sectors upfront
    all_sectors = list(df['sector_code'].unique())
    
    if sort_by == "latest":
        # Sort by most recent week's RS percentile
        latest_week = df['week_end_date'].max()
        latest_data = df[df['week_end_date'] == latest_week].copy()
        
        # Get one entry per sector with the mean RS percentile
        sector_rs = latest_data.groupby('sector_code')['rs_percentile'].mean().sort_values(ascending=False)
        sort_order = list(sector_rs.index)
        
        # Add any missing sectors to the end
        seen = set(sort_order)
        for s in all_sectors:
            if s not in seen:
                sort_order.append(s)
                seen.add(s)
        
        # Ensure uniqueness
        sort_order = list(dict.fromkeys(sort_order))
        
        # Create category type for sorting
        df['sort_key'] = pd.Categorical(
            df['sector_code'],
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
            
            # Get mean RS per sector for newest and oldest weeks
            newest_data = df[df['week_end_date'] == newest].groupby('sector_code')['rs_percentile'].mean()
            oldest_data = df[df['week_end_date'] == oldest].groupby('sector_code')['rs_percentile'].mean()
            
            # Only calculate change for sectors present in both weeks
            common_sectors = newest_data.index.intersection(oldest_data.index)
            if len(common_sectors) > 0:
                change = newest_data.loc[common_sectors] - oldest_data.loc[common_sectors]
                sort_order = list(change.sort_values(ascending=False).index)
                
                # Add any missing sectors to the end
                seen = set(sort_order)
                for s in all_sectors:
                    if s not in seen:
                        sort_order.append(s)
                        seen.add(s)
                
                # Ensure uniqueness
                sort_order = list(dict.fromkeys(sort_order))
                
                df['sort_key'] = pd.Categorical(
                    df['sector_code'],
                    categories=sort_order,
                    ordered=True
                )
                df = df.sort_values('sort_key').drop('sort_key', axis=1)
            else:
                # Fallback to alphabetical if no common sectors
                df = df.sort_values('sector_name')
        else:
            # Not enough weeks, fallback to alphabetical
            df = df.sort_values('sector_name')
    
    else:  # 'alpha' or 'sector' or default
        # Alphabetical by sector name
        df = df.sort_values('sector_name')
    
    return df


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


def get_subindustry_info(db: Session, subindustry_code: str) -> Optional[dict]:
    """
    Get information about a specific sub-industry.
    
    Args:
        db: Database session
        subindustry_code: GICS sub-industry code
    
    Returns:
        Dict with sub-industry info or None if not found
    """
    subindustry = db.query(GICSSubIndustry).filter(
        GICSSubIndustry.code == subindustry_code
    ).first()
    
    if not subindustry:
        return None
    
    return {
        'code': subindustry.code,
        'name': subindustry.name,
        'sector_name': subindustry.sector_name,
        'industry_name': subindustry.industry_name,
    }


def get_stock_rs_matrix_data(
    db: Session,
    subindustry_code: str,
    num_weeks: int = None,
    sort_by: str = "latest"
) -> pd.DataFrame:
    """
    Calculate individual stock RS data on-the-fly for a sub-industry.
    
    Args:
        db: Database session
        subindustry_code: GICS sub-industry code
        num_weeks: Number of weeks to include (default from settings)
        sort_by: Sort method - 'latest', 'change', or 'alpha'
    
    Returns:
        DataFrame with columns:
        - ticker
        - stock_name
        - week_label
        - week_end_date
        - mansfield_rs
        - rs_percentile
    """
    from src.models import StockPrice
    from src.services.rs_calculator import MansfieldRSCalculator, calculate_percentile_ranks
    from src.config import settings
    
    if num_weeks is None:
        num_weeks = settings.DEFAULT_WEEKS_DISPLAY
    
    # Get actual available week_end_dates from the RSWeekly table (same as sub-industry heatmap)
    # This ensures stock heatmap shows the exact same dates as other heatmaps
    available_weeks = db.query(RSWeekly.week_end_date).distinct().order_by(
        desc(RSWeekly.week_end_date)
    ).limit(num_weeks).all()
    
    if not available_weeks:
        return pd.DataFrame()
    
    # Extract dates - these are the exact week dates to display
    week_dates = [w[0] for w in available_weeks]
    
    # Create week_ranges structure compatible with rest of the function
    week_ranges = [
        {'week_end': wd, 'label': wd.strftime("%d/%m/%y")}
        for wd in week_dates
    ]
    
    # Get date range for price queries
    # Need 60+ weeks BEFORE the oldest week we want to display for SMA calculation
    end_date = week_dates[0]  # Most recent week
    oldest_display_week = week_dates[-1]  # Oldest week to display
    start_date = oldest_display_week - timedelta(weeks=60)  # 52 weeks for SMA + buffer
    
    # Get stocks in sub-industry
    stocks = get_subindustry_stocks(db, subindustry_code)
    
    if not stocks:
        return pd.DataFrame()
    
    # Get benchmark prices
    benchmark_prices = db.query(StockPrice).filter(
        StockPrice.ticker == settings.BENCHMARK_TICKER,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not benchmark_prices:
        return pd.DataFrame()
    
    benchmark_series = pd.Series(
        {p.date: p.adj_close for p in benchmark_prices}
    ).sort_index()
    
    # Calculate RS for each stock
    calculator = MansfieldRSCalculator()
    all_results = []
    
    for stock in stocks:
        # Get stock prices
        stock_prices = db.query(StockPrice).filter(
            StockPrice.ticker == stock['ticker'],
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).order_by(StockPrice.date).all()
        
        if not stock_prices:
            continue
        
        stock_series = pd.Series(
            {p.date: p.adj_close for p in stock_prices}
        ).sort_index()
        
        # Calculate full RS history
        try:
            rs_result = calculator.calculate_full(stock_series, benchmark_series)
            
            if rs_result.empty:
                continue
            
            # Sample at week end dates
            for week in week_ranges:
                week_end = week['week_end']
                week_label = week['label']
                
                # Find the closest date <= week_end
                valid_dates = [d for d in rs_result.index if d <= week_end]
                if not valid_dates:
                    continue
                
                closest_date = max(valid_dates)
                row = rs_result.loc[closest_date]
                
                mansfield_rs = row['mansfield_rs']
                if pd.isna(mansfield_rs):
                    mansfield_rs = None
                
                all_results.append({
                    'ticker': stock['ticker'],
                    'stock_name': stock['name'],
                    'week_end_date': week_end,
                    'week_label': week_label,
                    'mansfield_rs': mansfield_rs,
                    'rs_percentile': None,  # Will be calculated below
                })
        except Exception as e:
            logger.warning(f"Error calculating RS for {stock['ticker']}: {e}")
            continue
    
    if not all_results:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_results)
    
    # Calculate percentile ranks per week
    for week_end in df['week_end_date'].unique():
        week_mask = df['week_end_date'] == week_end
        week_rs = df.loc[week_mask, 'mansfield_rs'].dropna()
        
        if not week_rs.empty:
            percentiles = calculate_percentile_ranks(week_rs)
            for idx in percentiles.index:
                df.loc[idx, 'rs_percentile'] = int(percentiles[idx])
    
    # Sort stocks
    df = _sort_stocks(df, sort_by)
    
    return df


def get_stock_price_with_rs(
    db: Session,
    ticker: str,
    num_weeks: int = 52
) -> pd.DataFrame:
    """
    Get stock price history with RS indicator and Cardwell RSI data for charting.
    
    Calculates:
    - RS Line = Close / Benchmark Close (like Pine Script: close/comparativeSymbol)
    - RS EMA 13 = 13-period EMA of RS Line
    - RS EMA 52 = 52-period EMA of RS Line
    - RSI 14 = 14-period RSI
    - RSI SMA 9 = 9-period SMA of RSI
    - RSI EMA 45 = 45-period EMA of RSI
    
    Args:
        db: Database session
        ticker: Stock ticker symbol
        num_weeks: Number of weeks of history to return
    
    Returns:
        DataFrame with columns:
        - date, open, high, low, close, adj_close, volume
        - rs_line, rs_ema_13, rs_ema_52
        - rsi_14, rsi_sma_9, rsi_ema_45
    """
    from src.models import StockPrice
    from src.config import settings
    
    # Get actual latest date from stock's price data (not just last Friday)
    latest_price = db.query(StockPrice.date).filter(
        StockPrice.ticker == ticker
    ).order_by(desc(StockPrice.date)).first()
    
    if not latest_price:
        return pd.DataFrame()
    
    end_date = latest_price[0]
    # Need ~65 weeks of data to have enough for 52-week EMA calculation
    start_date = end_date - timedelta(weeks=num_weeks + 60)
    
    # Get stock prices
    stock_prices = db.query(StockPrice).filter(
        StockPrice.ticker == ticker,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not stock_prices:
        return pd.DataFrame()
    
    # Get benchmark prices
    benchmark_prices = db.query(StockPrice).filter(
        StockPrice.ticker == settings.BENCHMARK_TICKER,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not benchmark_prices:
        return pd.DataFrame()
    
    # Create DataFrames
    stock_df = pd.DataFrame([{
        'date': p.date,
        'open': p.open,
        'high': p.high,
        'low': p.low,
        'close': p.close,
        'adj_close': p.adj_close,
        'volume': p.volume,
    } for p in stock_prices]).set_index('date')
    
    benchmark_df = pd.DataFrame([{
        'date': p.date,
        'benchmark_close': p.adj_close,
    } for p in benchmark_prices]).set_index('date')
    
    # Merge on date (inner join to only keep common dates)
    df = stock_df.join(benchmark_df, how='inner')
    
    if df.empty:
        return pd.DataFrame()
    
    # Calculate RS Line (like Pine Script: close/comparativeSymbol)
    df['rs_line'] = df['adj_close'] / df['benchmark_close']
    
    # Calculate EMAs (like Pine Script: ema(net, lenghtMA))
    df['rs_ema_13'] = df['rs_line'].ewm(span=13, adjust=False).mean()
    df['rs_ema_52'] = df['rs_line'].ewm(span=52, adjust=False).mean()
    
    # Calculate Price EMAs for weekly chart analysis (10-week and 30-week)
    df['ema_10'] = df['adj_close'].ewm(span=10, adjust=False).mean()
    df['ema_30'] = df['adj_close'].ewm(span=30, adjust=False).mean()
    
    # Calculate Cardwell RSI (14-period RSI)
    df['rsi_14'] = _calculate_rsi(df['adj_close'], period=14)
    
    # Calculate RSI moving averages
    df['rsi_sma_9'] = df['rsi_14'].rolling(window=9).mean()
    df['rsi_ema_45'] = df['rsi_14'].ewm(span=45, adjust=False).mean()
    
    # Reset index and filter to requested weeks
    df = df.reset_index()
    cutoff_date = end_date - timedelta(weeks=num_weeks)
    df = df[df['date'] >= cutoff_date]
    
    # Drop the benchmark column (no longer needed)
    df = df.drop(columns=['benchmark_close'])
    
    return df


def get_stock_price_with_rs_weekly(
    db: Session,
    ticker: str,
    num_weeks: int = 104
) -> pd.DataFrame:
    """
    Get weekly OHLC with RS indicator and Cardwell RSI data for charting.
    
    Resamples daily data into weekly OHLC bars (Mon-Fri):
    - Open: First day's open
    - High: Max of week
    - Low: Min of week
    - Close: Last day's close
    - Volume: Sum of week
    
    Then recalculates RS and RSI indicators using the same numeric periods
    as daily (EMA 13, EMA 52 for RS; RSI 14, SMA 9, EMA 45 for RSI).
    
    Args:
        db: Database session
        ticker: Stock ticker symbol
        num_weeks: Number of weeks of history to return
    
    Returns:
        DataFrame with columns:
        - date, open, high, low, close, adj_close, volume
        - rs_line, rs_ema_13, rs_ema_52
        - ema_10, ema_30
        - rsi_14, rsi_sma_9, rsi_ema_45
    """
    from src.models import StockPrice
    from src.config import settings
    
    # Get actual latest date from stock's price data
    latest_price = db.query(StockPrice.date).filter(
        StockPrice.ticker == ticker
    ).order_by(desc(StockPrice.date)).first()
    
    if not latest_price:
        return pd.DataFrame()
    
    end_date = latest_price[0]
    # Need extra history for indicator warm-up (52 weeks for EMA + buffer)
    start_date = end_date - timedelta(weeks=num_weeks + 60)
    
    # Get stock prices
    stock_prices = db.query(StockPrice).filter(
        StockPrice.ticker == ticker,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not stock_prices:
        return pd.DataFrame()
    
    # Get benchmark prices
    benchmark_prices = db.query(StockPrice).filter(
        StockPrice.ticker == settings.BENCHMARK_TICKER,
        StockPrice.date >= start_date,
        StockPrice.date <= end_date
    ).order_by(StockPrice.date).all()
    
    if not benchmark_prices:
        return pd.DataFrame()
    
    # Create daily DataFrames
    stock_df = pd.DataFrame([{
        'date': p.date,
        'open': p.open,
        'high': p.high,
        'low': p.low,
        'close': p.close,
        'adj_close': p.adj_close,
        'volume': p.volume,
    } for p in stock_prices])
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df = stock_df.set_index('date')
    
    benchmark_df = pd.DataFrame([{
        'date': p.date,
        'benchmark_close': p.adj_close,
    } for p in benchmark_prices])
    benchmark_df['date'] = pd.to_datetime(benchmark_df['date'])
    benchmark_df = benchmark_df.set_index('date')
    
    # Resample stock data to weekly (week ending Friday)
    weekly_stock = stock_df.resample('W-FRI').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'adj_close': 'last',
        'volume': 'sum',
    }).dropna()
    
    # Resample benchmark data to weekly
    weekly_benchmark = benchmark_df.resample('W-FRI').agg({
        'benchmark_close': 'last',
    }).dropna()
    
    # Merge on date (inner join to only keep common dates)
    df = weekly_stock.join(weekly_benchmark, how='inner')
    
    if df.empty:
        return pd.DataFrame()
    
    # Calculate RS Line on weekly data
    df['rs_line'] = df['adj_close'] / df['benchmark_close']
    
    # Calculate RS EMAs on weekly data (same numeric periods)
    df['rs_ema_13'] = df['rs_line'].ewm(span=13, adjust=False).mean()
    df['rs_ema_52'] = df['rs_line'].ewm(span=52, adjust=False).mean()
    
    # Calculate Price EMAs on weekly data
    df['ema_10'] = df['adj_close'].ewm(span=10, adjust=False).mean()
    df['ema_30'] = df['adj_close'].ewm(span=30, adjust=False).mean()
    
    # Calculate Cardwell RSI on weekly data (14-period)
    df['rsi_14'] = _calculate_rsi(df['adj_close'], period=14)
    
    # Calculate RSI moving averages on weekly data
    df['rsi_sma_9'] = df['rsi_14'].rolling(window=9).mean()
    df['rsi_ema_45'] = df['rsi_14'].ewm(span=45, adjust=False).mean()
    
    # Reset index and filter to requested weeks
    df = df.reset_index()
    df = df.tail(num_weeks)
    
    # Drop the benchmark column
    df = df.drop(columns=['benchmark_close'])
    
    return df


def _calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index) using Wilder's smoothing method.
    
    This matches TradingView's RSI calculation.
    
    Args:
        prices: Series of closing prices
        period: RSI period (default 14)
    
    Returns:
        Series of RSI values (0-100)
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0.0)
    losses = (-delta).where(delta < 0, 0.0)
    
    # Calculate initial average gain/loss using SMA for first period
    first_avg_gain = gains.iloc[:period].mean()
    first_avg_loss = losses.iloc[:period].mean()
    
    # Use Wilder's smoothing (exponential moving average with alpha = 1/period)
    # This is equivalent to: avg = (prev_avg * (period-1) + current) / period
    avg_gains = gains.copy()
    avg_losses = losses.copy()
    
    avg_gains.iloc[:period] = None
    avg_losses.iloc[:period] = None
    avg_gains.iloc[period] = first_avg_gain
    avg_losses.iloc[period] = first_avg_loss
    
    # Apply Wilder's smoothing for remaining values
    for i in range(period + 1, len(prices)):
        avg_gains.iloc[i] = (avg_gains.iloc[i-1] * (period - 1) + gains.iloc[i]) / period
        avg_losses.iloc[i] = (avg_losses.iloc[i-1] * (period - 1) + losses.iloc[i]) / period
    
    # Calculate RS and RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def _sort_stocks(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """Sort stock DataFrame by specified method."""
    if df.empty:
        return df
    
    if sort_by == "latest":
        # Sort by most recent week's RS percentile
        latest_week = df['week_end_date'].max()
        latest_data = df[df['week_end_date'] == latest_week].set_index('ticker')
        
        # Handle NaN percentiles - put them at the end
        latest_data['sort_val'] = latest_data['rs_percentile'].fillna(-999)
        sort_order = latest_data['sort_val'].sort_values(ascending=False).index.tolist()
        
        df['sort_key'] = pd.Categorical(
            df['ticker'],
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
            
            newest_data = df[df['week_end_date'] == newest].set_index('ticker')
            oldest_data = df[df['week_end_date'] == oldest].set_index('ticker')
            
            # Calculate change, handling NaN
            common_tickers = newest_data.index.intersection(oldest_data.index)
            if len(common_tickers) > 0:
                change = (newest_data.loc[common_tickers, 'rs_percentile'] - 
                         oldest_data.loc[common_tickers, 'rs_percentile'])
                sort_order = change.sort_values(ascending=False).index.tolist()
                
                # Add tickers not in both weeks at the end
                all_tickers = df['ticker'].unique().tolist()
                for t in all_tickers:
                    if t not in sort_order:
                        sort_order.append(t)
                
                df['sort_key'] = pd.Categorical(
                    df['ticker'],
                    categories=sort_order,
                    ordered=True
                )
                df = df.sort_values('sort_key').drop('sort_key', axis=1)
            
    else:  # 'alpha' or default
        # Alphabetical by stock name
        df = df.sort_values('stock_name')
    
    return df

