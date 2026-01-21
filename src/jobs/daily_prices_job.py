"""
Price refresh job.

Fetches price data for all tracked stocks to fill any gaps.
Can be run standalone or as part of the weekly data update.

Supports two modes:
1. Smart mode (default): Detects missing dates and only fetches those
2. Days back mode: Fetches a fixed number of days back (legacy)
"""
import logging
from datetime import datetime, date, timedelta, timezone
from typing import Optional, List, Set

from sqlalchemy import func

from src.config import settings
from src.models import SessionLocal, Stock, StockPrice, JobLog, JobStatus
from src.ingestion.sources.yfinance_source import yfinance_source

logger = logging.getLogger(__name__)

# Sector ETFs for sector-level RS calculation
SECTOR_ETF_TICKERS = ["XLE", "XLB", "XLI", "XLY", "XLP", "XLV", "XLF", "XLK", "XLC", "XLU", "XLRE"]

# Sector ETF details (ticker -> (sector_code, sector_name, etf_name))
SECTOR_ETFS = {
    "XLE": ("10", "Energy", "Energy Select Sector SPDR Fund"),
    "XLB": ("15", "Materials", "Materials Select Sector SPDR Fund"),
    "XLI": ("20", "Industrials", "Industrial Select Sector SPDR Fund"),
    "XLY": ("25", "Consumer Discretionary", "Consumer Discretionary Select Sector SPDR Fund"),
    "XLP": ("30", "Consumer Staples", "Consumer Staples Select Sector SPDR Fund"),
    "XLV": ("35", "Health Care", "Health Care Select Sector SPDR Fund"),
    "XLF": ("40", "Financials", "Financial Select Sector SPDR Fund"),
    "XLK": ("45", "Information Technology", "Technology Select Sector SPDR Fund"),
    "XLC": ("50", "Communication Services", "Communication Services Select Sector SPDR Fund"),
    "XLU": ("55", "Utilities", "Utilities Select Sector SPDR Fund"),
    "XLRE": ("60", "Real Estate", "Real Estate Select Sector SPDR Fund"),
}


def _get_expected_trading_days(start_date: date, end_date: date) -> Set[date]:
    """
    Get expected US market trading days between start and end dates.
    
    Excludes weekends. Major holidays are not excluded here since yfinance
    will simply return no data for those days.
    
    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
    
    Returns:
        Set of expected trading dates (weekdays only)
    """
    trading_days = set()
    current = start_date
    while current <= end_date:
        # Exclude weekends (Saturday=5, Sunday=6)
        if current.weekday() < 5:
            trading_days.add(current)
        current += timedelta(days=1)
    return trading_days


def _get_latest_price_date(db, ticker: str) -> Optional[date]:
    """Get the most recent price date for a ticker."""
    result = db.query(func.max(StockPrice.date)).filter(
        StockPrice.ticker == ticker
    ).scalar()
    return result


def _get_missing_dates(db, tickers: List[str], end_date: date, lookback_days: int = 14) -> dict:
    """
    Detect missing price dates for each ticker.
    
    Uses the benchmark (SPY) as reference for expected trading days.
    
    Args:
        db: Database session
        tickers: List of ticker symbols to check
        end_date: End date to check up to
        lookback_days: Number of days to look back for missing data
    
    Returns:
        Dict mapping ticker to (start_date, end_date) tuple for missing range,
        or None if no missing dates
    """
    start_date = end_date - timedelta(days=lookback_days)
    
    # Get expected trading days (weekdays)
    expected_days = _get_expected_trading_days(start_date, end_date)
    
    if not expected_days:
        return {}
    
    missing_ranges = {}
    
    for ticker in tickers:
        # Get existing dates for this ticker in the range
        existing_dates = db.query(StockPrice.date).filter(
            StockPrice.ticker == ticker,
            StockPrice.date >= start_date,
            StockPrice.date <= end_date
        ).all()
        existing_set = {d[0] for d in existing_dates}
        
        # Find missing dates
        missing = expected_days - existing_set
        
        if missing:
            # Return the range of missing dates
            missing_start = min(missing)
            missing_end = max(missing)
            missing_ranges[ticker] = (missing_start, missing_end)
    
    return missing_ranges


def _ensure_sector_etfs_exist(db):
    """
    Ensure Stock records exist for all sector ETFs.
    
    Creates missing Stock records so their prices can be stored.
    """
    from src.models import GICSSubIndustry
    
    for ticker, (sector_code, sector_name, etf_name) in SECTOR_ETFS.items():
        existing = db.query(Stock).filter(Stock.ticker == ticker).first()
        if existing:
            continue
        
        # Find a sub-industry in this sector
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.sector_code == sector_code
        ).first()
        
        if not subindustry:
            logger.warning(f"No sub-industry found for sector {sector_code}, cannot create {ticker}")
            continue
        
        stock = Stock(
            ticker=ticker,
            name=etf_name,
            gics_subindustry_code=subindustry.code,
            is_active=True,
        )
        db.add(stock)
        logger.info(f"Created sector ETF record: {ticker}")
    
    db.commit()


def run_price_refresh_job(days_back: int = 7, db_session=None) -> dict:
    """
    Price data refresh job.
    
    Fetches prices for the specified number of days back
    to fill any gaps in the data.
    
    Args:
        days_back: Number of days to look back for price data (default 7)
        db_session: Optional existing database session (for use in combined jobs)
    
    Returns:
        Dict with job results
    """
    logger.info("=" * 50)
    logger.info(f"Starting price refresh job (looking back {days_back} days)")
    logger.info("=" * 50)
    
    # Use provided session or create new one
    own_session = db_session is None
    db = db_session if db_session else SessionLocal()
    
    # Create job log entry
    job_log = JobLog(
        job_name="price_refresh",
        started_at=datetime.now(timezone.utc),
        status=JobStatus.STARTED
    )
    db.add(job_log)
    db.commit()
    
    result = {
        'success': False,
        'stocks_updated': 0,
        'prices_added': 0,
        'error': None
    }
    
    try:
        # Get all active stocks
        stocks = db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in stocks]
        
        # Ensure sector ETFs are included - create Stock records if missing
        _ensure_sector_etfs_exist(db)
        for etf in SECTOR_ETF_TICKERS:
            if etf not in tickers:
                tickers.append(etf)
        
        logger.info(f"Refreshing prices for {len(tickers)} stocks (including {len(SECTOR_ETF_TICKERS)} sector ETFs)")
        
        # Fetch prices for the specified number of days back
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        
        # Batch fetch prices
        all_prices = yfinance_source.fetch_multiple_prices(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            batch_size=50
        )
        
        # Also fetch benchmark
        benchmark_ticker = settings.BENCHMARK_TICKER
        if benchmark_ticker not in all_prices:
            benchmark_prices = yfinance_source.fetch_price_history(
                benchmark_ticker, start_date, end_date
            )
            if not benchmark_prices.empty:
                all_prices[benchmark_ticker] = benchmark_prices
        
        # Store prices
        prices_added = 0
        stocks_updated = 0
        
        for ticker, df in all_prices.items():
            if df.empty:
                continue
            
            added_for_ticker = 0
            for _, row in df.iterrows():
                # Check if already exists
                existing = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
                try:
                    price = StockPrice(
                        ticker=ticker,
                        date=row['date'],
                        open=row.get('open'),
                        high=row.get('high'),
                        low=row.get('low'),
                        close=row['close'],
                        adj_close=row.get('adj_close', row['close']),
                        volume=int(row['volume']) if 'volume' in row and row['volume'] else None,
                    )
                    db.add(price)
                    added_for_ticker += 1
                except Exception as e:
                    logger.warning(f"Error adding price for {ticker}: {e}")
            
            if added_for_ticker > 0:
                stocks_updated += 1
                prices_added += added_for_ticker
        
        db.commit()
        
        # Update job log
        job_log.status = JobStatus.SUCCESS
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.records_processed = prices_added
        db.commit()
        
        result['success'] = True
        result['stocks_updated'] = stocks_updated
        result['prices_added'] = prices_added
        
        logger.info(f"Updated {stocks_updated} stocks with {prices_added} new price records")
        
    except Exception as e:
        logger.exception(f"Price refresh job failed: {e}")
        
        job_log.status = JobStatus.FAILED
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.error_message = str(e)
        db.commit()
        
        result['error'] = str(e)
        
    finally:
        # Only close session if we created it
        if own_session:
            db.close()
    
    logger.info("=" * 50)
    logger.info("Price refresh job completed")
    logger.info("=" * 50)
    
    return result


def run_missing_prices_job(lookback_days: int = 14, db_session=None) -> dict:
    """
    Smart price refresh job that only fetches missing dates.
    
    Detects which dates are missing for each stock and only fetches those,
    making it efficient for daily runs where typically only 1 day is missing.
    
    Args:
        lookback_days: Number of days to look back for missing data (default 14)
        db_session: Optional existing database session
    
    Returns:
        Dict with job results
    """
    logger.info("=" * 50)
    logger.info(f"Starting smart price refresh (checking last {lookback_days} days for gaps)")
    logger.info("=" * 50)
    
    # Use provided session or create new one
    own_session = db_session is None
    db = db_session if db_session else SessionLocal()
    
    # Create job log entry
    job_log = JobLog(
        job_name="daily_prices",
        started_at=datetime.now(timezone.utc),
        status=JobStatus.STARTED
    )
    db.add(job_log)
    db.commit()
    
    result = {
        'success': False,
        'stocks_updated': 0,
        'prices_added': 0,
        'tickers_with_gaps': 0,
        'error': None
    }
    
    try:
        # Get all active stocks
        stocks = db.query(Stock).filter(Stock.is_active == True).all()
        tickers = [s.ticker for s in stocks]
        
        # Ensure sector ETFs are included
        _ensure_sector_etfs_exist(db)
        for etf in SECTOR_ETF_TICKERS:
            if etf not in tickers:
                tickers.append(etf)
        
        # Add benchmark if not in list
        benchmark_ticker = settings.BENCHMARK_TICKER
        if benchmark_ticker not in tickers:
            tickers.append(benchmark_ticker)
        
        # Determine end date (today, or yesterday if market hasn't closed yet)
        end_date = date.today()
        
        # Detect missing dates for each ticker
        logger.info(f"Checking {len(tickers)} tickers for missing dates...")
        missing_ranges = _get_missing_dates(db, tickers, end_date, lookback_days)
        
        if not missing_ranges:
            logger.info("No missing dates detected - all data is up to date!")
            job_log.status = JobStatus.SUCCESS
            job_log.completed_at = datetime.now(timezone.utc)
            job_log.records_processed = 0
            db.commit()
            result['success'] = True
            if own_session:
                db.close()
            return result
        
        result['tickers_with_gaps'] = len(missing_ranges)
        logger.info(f"Found {len(missing_ranges)} tickers with missing dates")
        
        # Group tickers by their missing date range to batch efficiently
        # Find the overall range needed
        all_missing_starts = [r[0] for r in missing_ranges.values()]
        all_missing_ends = [r[1] for r in missing_ranges.values()]
        overall_start = min(all_missing_starts)
        overall_end = max(all_missing_ends)
        
        logger.info(f"Fetching prices from {overall_start} to {overall_end}")
        
        # Get tickers that have missing data
        tickers_to_fetch = list(missing_ranges.keys())
        
        # Batch fetch prices for all tickers with missing data
        all_prices = yfinance_source.fetch_multiple_prices(
            tickers=tickers_to_fetch,
            start_date=overall_start,
            end_date=overall_end,
            batch_size=50
        )
        
        # Store prices (only for dates that are actually missing)
        prices_added = 0
        stocks_updated = 0
        
        for ticker, df in all_prices.items():
            if df.empty:
                continue
            
            added_for_ticker = 0
            for _, row in df.iterrows():
                # Check if already exists (shouldn't, but be safe)
                existing = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
                try:
                    price = StockPrice(
                        ticker=ticker,
                        date=row['date'],
                        open=row.get('open'),
                        high=row.get('high'),
                        low=row.get('low'),
                        close=row['close'],
                        adj_close=row.get('adj_close', row['close']),
                        volume=int(row['volume']) if 'volume' in row and row['volume'] else None,
                    )
                    db.add(price)
                    added_for_ticker += 1
                except Exception as e:
                    logger.warning(f"Error adding price for {ticker}: {e}")
            
            if added_for_ticker > 0:
                stocks_updated += 1
                prices_added += added_for_ticker
        
        db.commit()
        
        # Update job log
        job_log.status = JobStatus.SUCCESS
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.records_processed = prices_added
        db.commit()
        
        result['success'] = True
        result['stocks_updated'] = stocks_updated
        result['prices_added'] = prices_added
        
        logger.info(f"Updated {stocks_updated} stocks with {prices_added} new price records")
        
    except Exception as e:
        logger.exception(f"Smart price refresh job failed: {e}")
        
        job_log.status = JobStatus.FAILED
        job_log.completed_at = datetime.now(timezone.utc)
        job_log.error_message = str(e)
        db.commit()
        
        result['error'] = str(e)
        
    finally:
        if own_session:
            db.close()
    
    logger.info("=" * 50)
    logger.info("Smart price refresh job completed")
    logger.info("=" * 50)
    
    return result


# Backwards compatibility alias
def run_daily_prices_job() -> dict:
    """
    Daily price update job - runs after market close.
    
    Uses smart detection to only fetch missing dates.
    """
    return run_missing_prices_job(lookback_days=14)

