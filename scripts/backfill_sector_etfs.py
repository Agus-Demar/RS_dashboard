#!/usr/bin/env python3
"""
Backfill sector ETF prices.

This script adds the sector ETFs (XLE, XLB, XLI, etc.) to the database
and fetches their historical prices. This is needed for the new sector RS
calculation logic that uses actual ETF prices instead of aggregated
sub-industry RS values.

Usage:
    python scripts/backfill_sector_etfs.py
"""
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.models import SessionLocal, Stock, StockPrice, GICSSubIndustry
from src.ingestion.sources.yfinance_source import yfinance_source

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Sector ETFs for sector-level RS calculation
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


def create_sector_etf_records(db) -> int:
    """
    Create Stock records for sector ETFs.
    
    Returns:
        Number of records created
    """
    count = 0
    
    for ticker, (sector_code, sector_name, etf_name) in SECTOR_ETFS.items():
        existing = db.query(Stock).filter(Stock.ticker == ticker).first()
        if existing:
            logger.info(f"Sector ETF {ticker} already exists")
            continue
        
        # Find a sub-industry in this sector
        subindustry = db.query(GICSSubIndustry).filter(
            GICSSubIndustry.sector_code == sector_code
        ).first()
        
        if not subindustry:
            logger.warning(f"No sub-industry found for sector {sector_code} ({sector_name}), skipping {ticker}")
            continue
        
        stock = Stock(
            ticker=ticker,
            name=etf_name,
            gics_subindustry_code=subindustry.code,
            is_active=True,
        )
        db.add(stock)
        count += 1
        logger.info(f"Created sector ETF record: {ticker} ({etf_name})")
    
    db.commit()
    return count


def fetch_sector_etf_prices(db) -> int:
    """
    Fetch historical prices for all sector ETFs.
    
    Returns:
        Number of price records added
    """
    # Calculate date range - need 2+ years for 52-week SMA calculation
    end_date = date.today()
    start_date = end_date - timedelta(days=settings.PRICE_HISTORY_YEARS * 365 + 60)
    
    logger.info(f"Fetching prices from {start_date} to {end_date}")
    
    tickers = list(SECTOR_ETFS.keys())
    
    # Batch fetch prices
    all_prices = yfinance_source.fetch_multiple_prices(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        batch_size=len(tickers)  # Small batch, fetch all at once
    )
    
    # Store prices
    total_records = 0
    
    for ticker, df in all_prices.items():
        if df.empty:
            logger.warning(f"No prices returned for {ticker}")
            continue
        
        added = 0
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
                added += 1
            except Exception as e:
                logger.warning(f"Error adding price for {ticker} on {row.get('date')}: {e}")
        
        if added > 0:
            db.commit()
            total_records += added
            logger.info(f"Added {added} price records for {ticker}")
    
    return total_records


def main():
    """Run the sector ETF backfill."""
    logger.info("=" * 60)
    logger.info("Sector ETF Backfill Script")
    logger.info("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Step 1: Create Stock records for sector ETFs
        logger.info("\nStep 1: Creating sector ETF stock records...")
        etfs_created = create_sector_etf_records(db)
        logger.info(f"Created {etfs_created} sector ETF records")
        
        # Step 2: Fetch historical prices
        logger.info("\nStep 2: Fetching historical prices...")
        prices_added = fetch_sector_etf_prices(db)
        logger.info(f"Added {prices_added} price records")
        
        logger.info("\n" + "=" * 60)
        logger.info("Backfill complete!")
        logger.info(f"  Sector ETFs created: {etfs_created}")
        logger.info(f"  Price records added: {prices_added}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.exception(f"Backfill failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

