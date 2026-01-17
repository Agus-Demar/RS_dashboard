#!/usr/bin/env python3
"""
Update Stock Info from yfinance

Fetches stock names and market caps from yfinance for stocks that are missing this data.

Usage:
    python -m scripts.update_stock_info
    python -m scripts.update_stock_info --limit 100
    python -m scripts.update_stock_info --dry-run
"""
import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yfinance as yf
from sqlalchemy.orm import Session
from src.models.base import SessionLocal
from src.models import Stock

logger = logging.getLogger(__name__)


def fetch_stock_info(ticker: str) -> Optional[Dict[str, Any]]:
    """Fetch stock info from yfinance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or info.get('regularMarketPrice') is None:
            # Try to get basic info from fast_info
            try:
                fast = stock.fast_info
                return {
                    'name': ticker,
                    'market_cap': getattr(fast, 'market_cap', None),
                }
            except:
                return None
        
        return {
            'name': info.get('shortName') or info.get('longName') or ticker,
            'market_cap': info.get('marketCap'),
        }
    except Exception as e:
        logger.debug(f"Could not fetch info for {ticker}: {e}")
        return None


def update_stocks(
    db: Session,
    limit: Optional[int] = None,
    dry_run: bool = False,
    batch_size: int = 50
) -> Dict[str, int]:
    """
    Update stock info from yfinance.
    
    Args:
        db: Database session
        limit: Max number of stocks to update
        dry_run: If True, don't save changes
        batch_size: Number of stocks to commit at once
        
    Returns:
        Dictionary with update statistics
    """
    # Find stocks where name equals ticker (not yet updated)
    query = db.query(Stock).filter(Stock.name == Stock.ticker)
    
    if limit:
        query = query.limit(limit)
    
    stocks = query.all()
    total = len(stocks)
    
    logger.info(f"Found {total} stocks to update")
    
    stats = {
        'total': total,
        'updated': 0,
        'failed': 0,
        'skipped': 0,
    }
    
    for i, stock in enumerate(stocks):
        if i % 10 == 0:
            logger.info(f"Progress: {i}/{total} ({stats['updated']} updated, {stats['failed']} failed)")
        
        info = fetch_stock_info(stock.ticker)
        
        if info:
            if not dry_run:
                stock.name = info.get('name', stock.ticker)
                if info.get('market_cap'):
                    stock.market_cap = info['market_cap']
            stats['updated'] += 1
            logger.debug(f"Updated {stock.ticker}: {info.get('name')}")
        else:
            stats['failed'] += 1
            logger.debug(f"Failed to get info for {stock.ticker}")
        
        # Commit in batches
        if not dry_run and (i + 1) % batch_size == 0:
            db.commit()
            logger.info(f"  Committed batch {(i + 1) // batch_size}")
        
        # Rate limit (yfinance can be rate limited)
        time.sleep(0.15)
    
    # Final commit
    if not dry_run:
        db.commit()
    
    return stats


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Reduce noise
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('peewee').setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser(description="Update stock info from yfinance")
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Maximum number of stocks to update"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't save changes to database"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for commits"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    db = SessionLocal()
    
    try:
        logger.info("Updating stock info from yfinance...")
        
        stats = update_stocks(
            db,
            limit=args.limit,
            dry_run=args.dry_run,
            batch_size=args.batch_size,
        )
        
        logger.info("")
        logger.info("=" * 50)
        logger.info("Update Summary:")
        logger.info(f"  Total stocks processed: {stats['total']}")
        logger.info(f"  Successfully updated:   {stats['updated']}")
        logger.info(f"  Failed (no data):       {stats['failed']}")
        logger.info("=" * 50)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
