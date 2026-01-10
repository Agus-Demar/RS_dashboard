"""
Price refresh job.

Fetches price data for all tracked stocks to fill any gaps.
Can be run standalone or as part of the weekly data update.
"""
import logging
from datetime import datetime, date, timedelta, timezone
from typing import Optional

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


# Backwards compatibility alias
def run_daily_prices_job() -> dict:
    """Legacy function name for backwards compatibility."""
    return run_price_refresh_job(days_back=7)

