#!/usr/bin/env python3
"""
Script to add additional stocks to the database.

This script adds stocks from S&P 400 MidCap and S&P 600 SmallCap indices
to an existing database that may only have S&P 500 stocks.

Usage:
    python scripts/add_stocks.py [--sp400] [--sp600] [--all] [--with-prices] [--dry-run]

Options:
    --sp400       Add S&P 400 MidCap stocks only
    --sp600       Add S&P 600 SmallCap stocks only
    --all         Add all new stocks (S&P 400 + S&P 600) [default if no option]
    --with-prices Also fetch price history for new stocks
    --dry-run     Show what would be added without making changes
"""
import argparse
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from src.config import settings
from src.models import GICSSubIndustry, Stock, StockPrice, SessionLocal, init_db
from src.ingestion.sources.wikipedia_source import wikipedia_source
from src.ingestion.sources.yfinance_source import yfinance_source
from src.ingestion.mappers.gics_mapper import gics_mapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_existing_tickers(db: Session) -> set:
    """Get all existing tickers in the database."""
    stocks = db.query(Stock.ticker).all()
    return {s.ticker for s in stocks}


def add_subindustries_if_missing(db: Session, dry_run: bool = False) -> int:
    """Add any missing GICS sub-industries to the database."""
    logger.info("Checking for missing GICS sub-industries...")
    
    # Get all unique sub-industries from all indices
    subindustries_df = gics_mapper.get_all_subindustries()
    
    # Track codes we've already processed to avoid duplicates
    processed_codes = set()
    count = 0
    
    for _, row in subindustries_df.iterrows():
        code = row['code']
        
        # Skip if we've already processed this code in this batch
        if code in processed_codes:
            continue
        processed_codes.add(code)
        
        # Check if already exists in database
        existing = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.code == code
        ).first()
        
        if existing:
            continue
        
        if dry_run:
            logger.info(f"  [DRY-RUN] Would add sub-industry: {row['sub_industry']} ({code})")
        else:
            subindustry = GICSSubIndustry(
                code=code,
                name=row['sub_industry'],
                industry_code=row['industry_code'],
                industry_name=row['sub_industry'],
                industry_group_code=row['industry_group_code'],
                industry_group_name=row['sub_industry'].split(' - ')[0],
                sector_code=row['sector_code'],
                sector_name=row['sector'],
            )
            db.add(subindustry)
        count += 1
    
    if not dry_run and count > 0:
        db.commit()
    
    logger.info(f"{'Would add' if dry_run else 'Added'} {count} new GICS sub-industries")
    return count


def add_stocks_from_index(
    db: Session,
    index_name: str,
    existing_tickers: set,
    dry_run: bool = False
) -> tuple[int, list]:
    """
    Add stocks from a specific index.
    
    Returns:
        Tuple of (count added, list of new tickers)
    """
    logger.info(f"Fetching {index_name} constituents...")
    
    if index_name == 'SP400':
        stocks_df = wikipedia_source.fetch_sp400_constituents()
    elif index_name == 'SP600':
        stocks_df = wikipedia_source.fetch_sp600_constituents()
    else:
        raise ValueError(f"Unknown index: {index_name}")
    
    logger.info(f"Processing {len(stocks_df)} stocks from {index_name}...")
    
    count = 0
    new_tickers = []
    
    for _, row in stocks_df.iterrows():
        ticker = row['ticker']
        
        # Skip if already exists
        if ticker in existing_tickers:
            continue
        
        # Get GICS mapping
        mapping = gics_mapper.map_ticker(ticker)
        if not mapping:
            logger.debug(f"No GICS mapping for {ticker}, skipping")
            continue
        
        # Verify sub-industry exists
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.code == mapping['subindustry_code']
        ).first()
        
        if not subindustry:
            logger.debug(f"Sub-industry {mapping['subindustry_code']} not found for {ticker}")
            continue
        
        if dry_run:
            logger.info(f"  [DRY-RUN] Would add: {ticker} ({row.get('name', 'N/A')}) - {mapping['subindustry_name']}")
        else:
            stock = Stock(
                ticker=ticker,
                name=row.get('name', ticker),
                gics_subindustry_code=mapping['subindustry_code'],
                is_active=True,
            )
            db.add(stock)
        
        count += 1
        new_tickers.append(ticker)
        existing_tickers.add(ticker)  # Prevent duplicates
    
    if not dry_run and count > 0:
        db.commit()
    
    logger.info(f"{'Would add' if dry_run else 'Added'} {count} new stocks from {index_name}")
    return count, new_tickers


def fetch_prices_for_stocks(
    db: Session,
    tickers: list,
    dry_run: bool = False
) -> int:
    """Fetch historical prices for new stocks."""
    if dry_run:
        logger.info(f"[DRY-RUN] Would fetch prices for {len(tickers)} stocks")
        return 0
    
    if not tickers:
        return 0
    
    logger.info(f"Fetching price history for {len(tickers)} new stocks...")
    
    # Calculate date range (2 years + buffer)
    end_date = date.today()
    start_date = end_date - timedelta(days=settings.PRICE_HISTORY_YEARS * 365 + 30)
    
    # Fetch prices in batch
    all_prices = yfinance_source.fetch_multiple_prices(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        batch_size=50
    )
    
    # Store prices in database
    total_records = 0
    for ticker, df in all_prices.items():
        if df.empty:
            continue
        
        for _, row in df.iterrows():
            try:
                # Check for existing record
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
                total_records += 1
                
            except Exception as e:
                logger.warning(f"Error storing price for {ticker} on {row.get('date')}: {e}")
        
        # Commit in batches
        if total_records > 0 and total_records % 5000 == 0:
            db.commit()
            logger.info(f"  Stored {total_records} price records...")
    
    if total_records > 0:
        db.commit()
    
    logger.info(f"Stored {total_records} price records for new stocks")
    return total_records


def main():
    parser = argparse.ArgumentParser(
        description='Add additional stocks to the RS Dashboard database'
    )
    parser.add_argument(
        '--sp400', action='store_true',
        help='Add S&P 400 MidCap stocks only'
    )
    parser.add_argument(
        '--sp600', action='store_true',
        help='Add S&P 600 SmallCap stocks only'
    )
    parser.add_argument(
        '--all', action='store_true',
        help='Add all new stocks (S&P 400 + S&P 600)'
    )
    parser.add_argument(
        '--with-prices', action='store_true',
        help='Also fetch price history for new stocks'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be added without making changes'
    )
    
    args = parser.parse_args()
    
    # Default to --all if no specific index is selected
    if not (args.sp400 or args.sp600 or args.all):
        args.all = True
    
    logger.info("=" * 60)
    logger.info("RS Dashboard - Add Additional Stocks")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("*** DRY RUN MODE - No changes will be made ***")
    
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Get existing tickers
        existing_tickers = get_existing_tickers(db)
        logger.info(f"Found {len(existing_tickers)} existing stocks in database")
        
        # Add missing sub-industries first
        add_subindustries_if_missing(db, dry_run=args.dry_run)
        
        # Track new tickers for price fetching
        all_new_tickers = []
        total_added = 0
        
        # Add stocks from selected indices
        if args.all or args.sp400:
            count, new_tickers = add_stocks_from_index(
                db, 'SP400', existing_tickers, dry_run=args.dry_run
            )
            total_added += count
            all_new_tickers.extend(new_tickers)
        
        if args.all or args.sp600:
            count, new_tickers = add_stocks_from_index(
                db, 'SP600', existing_tickers, dry_run=args.dry_run
            )
            total_added += count
            all_new_tickers.extend(new_tickers)
        
        # Fetch prices if requested
        if args.with_prices and all_new_tickers and not args.dry_run:
            fetch_prices_for_stocks(db, all_new_tickers, dry_run=args.dry_run)
        elif args.with_prices and args.dry_run:
            logger.info(f"[DRY-RUN] Would fetch prices for {len(all_new_tickers)} new stocks")
        
        logger.info("=" * 60)
        logger.info("Summary:")
        logger.info(f"  Total new stocks {'would be' if args.dry_run else ''} added: {total_added}")
        logger.info(f"  Total stocks in database: {len(existing_tickers) + (0 if args.dry_run else total_added)}")
        logger.info("=" * 60)
    finally:
        db.close()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

