"""
Script to download price data for missing ETFs needed for SCTR calculations.

Downloads historical price data from Yahoo Finance for all ETFs in the 
GICS sub-industry mapping that don't have data in the database.
"""
import sys
sys.path.insert(0, '.')

import logging
import time
from datetime import datetime, timedelta
from typing import List, Set

import yfinance as yf
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.models import StockPrice
from src.data.stockcharts_industry_mapping import INDUSTRY_ETF_MAP, SECTOR_ETFS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ETF tickers that are invalid or not available on Yahoo Finance
INVALID_TICKERS = {
    # Delisted or renamed ETFs
    'XPRO',  # Already in DB
}


def get_missing_etfs(db) -> Set[str]:
    """Get list of ETFs that need price data."""
    # Get all unique ETFs from the StockCharts industry mapping
    all_etfs = set()
    for code, mapping in INDUSTRY_ETF_MAP.items():
        if mapping.primary_etf not in INVALID_TICKERS:
            all_etfs.add(mapping.primary_etf)
    
    # Add sector ETFs
    for etf in SECTOR_ETFS.values():
        all_etfs.add(etf)
    
    # Check which ETFs are missing
    missing = set()
    for etf in all_etfs:
        count = db.query(func.count(StockPrice.id)).filter(
            StockPrice.ticker == etf
        ).scalar()
        if count == 0:
            missing.add(etf)
    
    return missing


def download_etf_prices(db, etf_ticker: str, years_back: int = 3) -> int:
    """Download price data for an ETF from Yahoo Finance.
    
    Note: ETFs are stored directly in StockPrice table without requiring 
    a Stock table entry (same as sector ETFs like XLE, XLK, etc.)
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years_back * 365)
        
        logger.info(f"Downloading {etf_ticker}...")
        
        ticker = yf.Ticker(etf_ticker)
        df = ticker.history(start=start_date, end=end_date, auto_adjust=False)
        
        if df.empty:
            logger.warning(f"No data returned for {etf_ticker}")
            return 0
        
        # Insert price records directly (no Stock table entry needed for ETFs)
        records_added = 0
        for date_idx, row in df.iterrows():
            price_date = date_idx.date() if hasattr(date_idx, 'date') else date_idx
            
            # Check if record exists
            existing = db.query(StockPrice).filter(
                StockPrice.ticker == etf_ticker,
                StockPrice.date == price_date
            ).first()
            
            if existing:
                continue
            
            # Handle potential NaN values
            adj_close = row.get('Adj Close', row.get('Close'))
            if adj_close is None or (hasattr(adj_close, '__float__') and str(adj_close) == 'nan'):
                adj_close = row.get('Close')
            
            price = StockPrice(
                ticker=etf_ticker,
                date=price_date,
                open=float(row['Open']) if row['Open'] and str(row['Open']) != 'nan' else None,
                high=float(row['High']) if row['High'] and str(row['High']) != 'nan' else None,
                low=float(row['Low']) if row['Low'] and str(row['Low']) != 'nan' else None,
                close=float(row['Close']) if row['Close'] and str(row['Close']) != 'nan' else None,
                adj_close=float(adj_close) if adj_close and str(adj_close) != 'nan' else None,
                volume=int(row['Volume']) if row['Volume'] and str(row['Volume']) != 'nan' else 0,
            )
            db.add(price)
            records_added += 1
        
        db.commit()
        logger.info(f"Added {records_added} price records for {etf_ticker}")
        return records_added
        
    except Exception as e:
        logger.error(f"Error downloading {etf_ticker}: {e}")
        db.rollback()
        return 0


def main():
    """Main function to download all missing ETFs."""
    # Connect to database
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Get missing ETFs
        missing_etfs = get_missing_etfs(db)
        
        print(f"\n{'='*60}")
        print(f"ETF Download Script")
        print(f"{'='*60}")
        print(f"Missing ETFs to download: {len(missing_etfs)}")
        print(f"{'='*60}\n")
        
        if not missing_etfs:
            print("All ETFs already have price data!")
            return
        
        # Download each ETF
        success_count = 0
        failed_etfs = []
        
        for i, etf in enumerate(sorted(missing_etfs), 1):
            print(f"[{i}/{len(missing_etfs)}] ", end="")
            records = download_etf_prices(db, etf)
            
            if records > 0:
                success_count += 1
            else:
                failed_etfs.append(etf)
            
            # Rate limiting - be nice to Yahoo Finance
            time.sleep(0.5)
        
        print(f"\n{'='*60}")
        print(f"Download Complete")
        print(f"{'='*60}")
        print(f"Successfully downloaded: {success_count}/{len(missing_etfs)}")
        
        if failed_etfs:
            print(f"\nFailed ETFs ({len(failed_etfs)}):")
            for etf in failed_etfs:
                print(f"  - {etf}")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
