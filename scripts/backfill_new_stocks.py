#!/usr/bin/env python3
"""
Backfill price data and RS calculations for new stocks.

This script:
1. Fetches price history for stocks that don't have price data
2. Recalculates RS values for all sub-industries

Usage:
    python scripts/backfill_new_stocks.py
"""
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import func

from src.config import settings
from src.models import SessionLocal, Stock, StockPrice, init_db
from src.ingestion.sources.yfinance_source import yfinance_source
from src.jobs.weekly_rs_job import backfill_rs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Reduce noise from other loggers
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('yfinance').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def get_stocks_without_prices(db) -> list:
    """Get list of active stocks that don't have price data."""
    stocks_with_prices = db.query(func.distinct(StockPrice.ticker)).subquery()
    
    missing = db.query(Stock.ticker).filter(
        Stock.is_active == True,
        ~Stock.ticker.in_(stocks_with_prices)
    ).all()
    
    return [s[0] for s in missing]


def fetch_and_store_prices(db, tickers: list, batch_size: int = 50) -> int:
    """Fetch and store price history for given tickers."""
    if not tickers:
        return 0
    
    # Calculate date range (2 years + buffer)
    end_date = date.today()
    start_date = end_date - timedelta(days=settings.PRICE_HISTORY_YEARS * 365 + 30)
    
    logger.info(f"Fetching prices for {len(tickers)} stocks...")
    logger.info(f"Date range: {start_date} to {end_date}")
    
    # Fetch prices in batch
    all_prices = yfinance_source.fetch_multiple_prices(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        batch_size=batch_size
    )
    
    # Store prices in database
    total_records = 0
    successful_tickers = 0
    
    for ticker, df in all_prices.items():
        if df.empty:
            continue
        
        ticker_records = 0
        for _, row in df.iterrows():
            try:
                # Skip if already exists
                existing = db.query(StockPrice).filter(
                    StockPrice.ticker == ticker,
                    StockPrice.date == row['date']
                ).first()
                
                if existing:
                    continue
                
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
                ticker_records += 1
                total_records += 1
                
            except Exception as e:
                logger.warning(f"Error storing price for {ticker}: {e}")
        
        if ticker_records > 0:
            successful_tickers += 1
        
        # Commit periodically
        if total_records > 0 and total_records % 5000 == 0:
            db.commit()
            logger.info(f"  Stored {total_records:,} price records...")
    
    if total_records > 0:
        db.commit()
    
    logger.info(f"Stored {total_records:,} price records for {successful_tickers} stocks")
    return total_records


def main():
    logger.info("=" * 60)
    logger.info("Backfill New Stocks - Price Data & RS Calculations")
    logger.info("=" * 60)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Step 1: Find stocks without prices
        logger.info("\nStep 1: Finding stocks without price data...")
        missing_tickers = get_stocks_without_prices(db)
        
        if not missing_tickers:
            logger.info("All stocks have price data!")
        else:
            logger.info(f"Found {len(missing_tickers)} stocks without price data")
            
            # Step 2: Fetch prices
            logger.info("\nStep 2: Fetching price history...")
            records = fetch_and_store_prices(db, missing_tickers)
            logger.info(f"Total price records added: {records:,}")
        
        # Step 3: Recalculate RS
        logger.info("\nStep 3: Recalculating RS values...")
        logger.info("This will recalculate RS for all sub-industries with the new stocks...")
        
        rs_results = backfill_rs(weeks=17)
        
        logger.info(f"\nRS Calculation complete:")
        logger.info(f"  Weeks processed: {rs_results['weeks_processed']}")
        logger.info(f"  Total RS records: {rs_results['total_records']}")
        if rs_results.get('errors'):
            logger.warning(f"  Errors: {len(rs_results['errors'])}")
        
        logger.info("\n" + "=" * 60)
        logger.info("Backfill complete!")
        logger.info("=" * 60)
        logger.info("\nYou can now start the app with:")
        logger.info("  uvicorn src.main:app --reload")
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user. Progress has been saved.")
    except Exception as e:
        logger.exception(f"Error: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

