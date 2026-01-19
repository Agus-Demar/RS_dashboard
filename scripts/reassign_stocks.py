#!/usr/bin/env python3
"""
Reassign Stocks to Correct Industries

Reassigns stocks to the correct StockCharts industry based on the 
scraped tickers data. This ensures stocks are in the same industries
as on StockCharts.com.

Usage:
    python -m scripts.reassign_stocks --dry-run
    python -m scripts.reassign_stocks
"""
import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models import SessionLocal, init_db, Stock, GICSSubIndustry
from scripts.import_stockcharts_tickers import INDUSTRY_NAME_TO_CODE

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def build_ticker_to_industry_map() -> dict:
    """Build mapping from ticker to StockCharts industry code."""
    data_file = project_root / "data" / "stockcharts_tickers.json"
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    ticker_to_industry = {}
    for sector in data['sectors']:
        for ind in sector['industries']:
            name_lower = ind['name'].lower()
            code = INDUSTRY_NAME_TO_CODE.get(name_lower)
            if code:
                for ticker in ind['tickers']:
                    ticker_to_industry[ticker] = code
    
    return ticker_to_industry


def run_reassignment(dry_run: bool = False):
    """Reassign stocks to correct industries."""
    logger.info("=" * 60)
    logger.info("Stock Reassignment Script")
    logger.info("=" * 60)
    
    if dry_run:
        logger.info("DRY RUN MODE - No changes will be made")
    
    # Build ticker -> industry mapping
    ticker_to_industry = build_ticker_to_industry_map()
    logger.info(f"Loaded {len(ticker_to_industry)} ticker mappings from scraped data")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Get valid industry codes
        valid_codes = {ind.code for ind in db.query(GICSSubIndustry).all()}
        logger.info(f"Valid industry codes in database: {len(valid_codes)}")
        
        # Get all stocks
        stocks = db.query(Stock).all()
        logger.info(f"Total stocks in database: {len(stocks)}")
        
        # Track reassignments
        reassigned = 0
        skipped_no_mapping = 0
        skipped_invalid_code = 0
        already_correct = 0
        
        for stock in stocks:
            correct_code = ticker_to_industry.get(stock.ticker)
            
            if not correct_code:
                skipped_no_mapping += 1
                continue
            
            if correct_code not in valid_codes:
                skipped_invalid_code += 1
                continue
            
            if stock.gics_subindustry_code == correct_code:
                already_correct += 1
                continue
            
            # Reassign stock
            old_code = stock.gics_subindustry_code
            if not dry_run:
                stock.gics_subindustry_code = correct_code
            reassigned += 1
            
            if reassigned <= 20:  # Only log first 20
                logger.debug(f"  {stock.ticker}: {old_code} -> {correct_code}")
        
        if reassigned > 20:
            logger.debug(f"  ... and {reassigned - 20} more")
        
        if not dry_run:
            db.commit()
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("Reassignment Complete!" if not dry_run else "Dry Run Complete!")
        logger.info(f"  Reassigned: {reassigned}")
        logger.info(f"  Already correct: {already_correct}")
        logger.info(f"  Skipped (no mapping): {skipped_no_mapping}")
        logger.info(f"  Skipped (invalid code): {skipped_invalid_code}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.exception(f"Reassignment failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reassign stocks to correct StockCharts industries"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    
    run_reassignment(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
