"""
Script to identify and deactivate stale stocks that have no recent price data.

These are typically:
- Delisted stocks
- Tickers that have changed
- Stocks that yfinance can no longer find

Stocks are marked as is_active=False rather than deleted, preserving historical data.
"""
import sys
sys.path.insert(0, '.')

import logging
from datetime import date, timedelta
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.models import Stock, StockPrice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_stale_stocks(db, days_threshold: int = 14):
    """
    Find stocks that haven't had price data updated recently.
    
    Args:
        db: Database session
        days_threshold: Number of days without data to consider stale
    
    Returns:
        List of (ticker, name, last_price_date) tuples
    """
    # Get benchmark's latest date as reference
    benchmark_latest = db.query(func.max(StockPrice.date)).filter(
        StockPrice.ticker == settings.BENCHMARK_TICKER
    ).scalar()
    
    if not benchmark_latest:
        logger.error("No benchmark data found!")
        return []
    
    cutoff_date = benchmark_latest - timedelta(days=days_threshold)
    logger.info(f"Benchmark latest: {benchmark_latest}, cutoff: {cutoff_date}")
    
    # Find active stocks with no recent price data
    stale_stocks = []
    
    # Get all active stocks
    active_stocks = db.query(Stock).filter(Stock.is_active == True).all()
    logger.info(f"Checking {len(active_stocks)} active stocks...")
    
    for stock in active_stocks:
        # Get the latest price date for this stock
        latest_price = db.query(func.max(StockPrice.date)).filter(
            StockPrice.ticker == stock.ticker
        ).scalar()
        
        if latest_price is None:
            # No price data at all
            stale_stocks.append((stock.ticker, stock.name, None, "no_data"))
        elif latest_price < cutoff_date:
            # Has data but it's stale
            stale_stocks.append((stock.ticker, stock.name, latest_price, "stale"))
    
    return stale_stocks


def deactivate_stocks(db, tickers: list):
    """Mark stocks as inactive."""
    count = 0
    for ticker in tickers:
        stock = db.query(Stock).filter(Stock.ticker == ticker).first()
        if stock and stock.is_active:
            stock.is_active = False
            count += 1
            logger.info(f"Deactivated: {ticker}")
    
    db.commit()
    return count


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Find and deactivate stale stocks")
    parser.add_argument("--days", type=int, default=14, 
                       help="Days threshold for stale data (default: 14)")
    parser.add_argument("--deactivate", action="store_true",
                       help="Actually deactivate the stocks (default: dry run)")
    parser.add_argument("--delete-prices", action="store_true",
                       help="Also delete price records for stale stocks")
    
    args = parser.parse_args()
    
    # Connect to database
    engine = create_engine(settings.db_url)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print(f"\n{'='*60}")
        print("Cleanup Stale Stocks Script")
        print(f"{'='*60}")
        print(f"Days threshold: {args.days}")
        print(f"Mode: {'DEACTIVATE' if args.deactivate else 'DRY RUN'}")
        
        # Find stale stocks
        stale_stocks = find_stale_stocks(db, args.days)
        
        if not stale_stocks:
            print("\nNo stale stocks found!")
            return
        
        # Separate by type
        no_data = [(t, n, d, r) for t, n, d, r in stale_stocks if r == "no_data"]
        stale = [(t, n, d, r) for t, n, d, r in stale_stocks if r == "stale"]
        
        print(f"\n{'='*60}")
        print("Results")
        print(f"{'='*60}")
        print(f"Total stale stocks: {len(stale_stocks)}")
        print(f"  - No price data: {len(no_data)}")
        print(f"  - Stale data: {len(stale)}")
        
        if no_data:
            print(f"\n--- Stocks with NO price data ({len(no_data)}) ---")
            for ticker, name, last_date, reason in sorted(no_data):
                print(f"  {ticker}: {name}")
        
        if stale:
            print(f"\n--- Stocks with STALE data ({len(stale)}) ---")
            for ticker, name, last_date, reason in sorted(stale, key=lambda x: x[2] or date.min):
                print(f"  {ticker}: {name} (last: {last_date})")
        
        if args.deactivate:
            print(f"\n{'='*60}")
            print("Deactivating stocks...")
            print(f"{'='*60}")
            
            tickers = [t for t, n, d, r in stale_stocks]
            deactivated = deactivate_stocks(db, tickers)
            print(f"Deactivated {deactivated} stocks")
            
            if args.delete_prices:
                print("\nDeleting price records...")
                total_deleted = 0
                for ticker in tickers:
                    count = db.query(StockPrice).filter(
                        StockPrice.ticker == ticker
                    ).delete()
                    total_deleted += count
                db.commit()
                print(f"Deleted {total_deleted} price records")
        else:
            print(f"\n[DRY RUN] Run with --deactivate to actually deactivate these stocks")
            print(f"Tickers to deactivate: {', '.join(sorted([t for t, n, d, r in stale_stocks]))}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
