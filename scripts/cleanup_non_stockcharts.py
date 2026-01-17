#!/usr/bin/env python3
"""
Cleanup Non-StockCharts Stocks

Removes stocks from the database that are not present in the StockCharts
scraped data, along with all their related data (prices, etc.).

Usage:
    python -m scripts.cleanup_non_stockcharts --dry-run
    python -m scripts.cleanup_non_stockcharts
"""
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Set, Dict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import func
from src.models.base import SessionLocal
from src.models import Stock, StockPrice, RSWeekly

logger = logging.getLogger(__name__)


def get_stockcharts_tickers(input_path: Path) -> Set[str]:
    """Load all tickers from the StockCharts scraped data."""
    with open(input_path) as f:
        data = json.load(f)
    
    tickers = set()
    for sector in data.get("sectors", []):
        for industry in sector.get("industries", []):
            for ticker in industry.get("tickers", []):
                tickers.add(ticker.upper().strip())
    
    return tickers


def cleanup_stocks(
    input_path: Path,
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Remove stocks not in StockCharts data.
    
    Args:
        input_path: Path to stockcharts_tickers.json
        dry_run: If True, don't actually delete
        
    Returns:
        Dictionary with cleanup statistics
    """
    # Load StockCharts tickers
    stockcharts_tickers = get_stockcharts_tickers(input_path)
    logger.info(f"Loaded {len(stockcharts_tickers)} tickers from StockCharts")
    
    db = SessionLocal()
    
    try:
        # Get all stocks currently in database
        all_stocks = db.query(Stock.ticker).all()
        all_db_tickers = {s[0].upper() for s in all_stocks}
        
        logger.info(f"Found {len(all_db_tickers)} stocks in database")
        
        # Find tickers to remove (in DB but not in StockCharts)
        tickers_to_remove = all_db_tickers - stockcharts_tickers
        tickers_to_keep = all_db_tickers & stockcharts_tickers
        
        logger.info(f"Stocks to keep: {len(tickers_to_keep)}")
        logger.info(f"Stocks to remove: {len(tickers_to_remove)}")
        
        stats = {
            'stockcharts_tickers': len(stockcharts_tickers),
            'db_stocks_before': len(all_db_tickers),
            'stocks_to_keep': len(tickers_to_keep),
            'stocks_removed': 0,
            'prices_removed': 0,
        }
        
        if not tickers_to_remove:
            logger.info("No stocks to remove!")
            return stats
        
        # Show sample of tickers being removed
        sample = list(tickers_to_remove)[:20]
        logger.info(f"Sample of tickers to remove: {sample}")
        
        if dry_run:
            logger.info("[DRY RUN] Would remove the following:")
            logger.info(f"  - {len(tickers_to_remove)} stocks")
            
            # Count prices that would be removed
            price_count = db.query(func.count(StockPrice.id)).filter(
                StockPrice.ticker.in_(tickers_to_remove)
            ).scalar()
            logger.info(f"  - {price_count:,} price records")
            stats['prices_removed'] = price_count
            stats['stocks_removed'] = len(tickers_to_remove)
            
        else:
            # Delete in batches to avoid memory issues
            batch_size = 100
            tickers_list = list(tickers_to_remove)
            
            total_prices_deleted = 0
            
            for i in range(0, len(tickers_list), batch_size):
                batch = tickers_list[i:i + batch_size]
                
                # Delete prices for these tickers
                prices_deleted = db.query(StockPrice).filter(
                    StockPrice.ticker.in_(batch)
                ).delete(synchronize_session=False)
                total_prices_deleted += prices_deleted
                
                # Delete stocks
                db.query(Stock).filter(
                    Stock.ticker.in_(batch)
                ).delete(synchronize_session=False)
                
                db.commit()
                
                logger.info(f"Processed batch {i // batch_size + 1}/{(len(tickers_list) + batch_size - 1) // batch_size}")
            
            stats['stocks_removed'] = len(tickers_to_remove)
            stats['prices_removed'] = total_prices_deleted
            
            logger.info(f"Removed {stats['stocks_removed']} stocks")
            logger.info(f"Removed {stats['prices_removed']:,} price records")
        
        return stats
        
    finally:
        db.close()


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser(description="Remove non-StockCharts stocks")
    parser.add_argument(
        "--input", "-i",
        default="data/stockcharts_tickers.json",
        help="Input JSON file from scraper"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually delete, just report what would be removed"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("Cleanup Non-StockCharts Stocks")
    logger.info("=" * 60)
    
    stats = cleanup_stocks(input_path, dry_run=args.dry_run)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Cleanup Summary:")
    logger.info(f"  StockCharts tickers:  {stats['stockcharts_tickers']}")
    logger.info(f"  DB stocks before:     {stats['db_stocks_before']}")
    logger.info(f"  Stocks kept:          {stats['stocks_to_keep']}")
    logger.info(f"  Stocks removed:       {stats['stocks_removed']}")
    logger.info(f"  Prices removed:       {stats['prices_removed']:,}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
